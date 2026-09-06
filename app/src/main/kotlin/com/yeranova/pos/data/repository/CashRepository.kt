package com.yeranova.pos.data.repository

import com.yeranova.pos.data.database.dao.CashRegisterDao
import com.yeranova.pos.data.database.dao.CashMovementDao
import com.yeranova.pos.data.model.CashRegister
import com.yeranova.pos.data.model.CashMovement
import com.yeranova.pos.data.model.CashRegisterStatus
import com.yeranova.pos.data.model.MovementType
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.LocalDateTime
import java.math.BigDecimal

class CashRepository(
    private val cashRegisterDao: CashRegisterDao,
    private val cashMovementDao: CashMovementDao
) {
    suspend fun openCashRegister(
        userId: Long,
        openingBalance: BigDecimal
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (openingBalance < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Opening balance cannot be negative"))
            }

            val now = LocalDateTime.now()
            val register = CashRegister(
                userId = userId,
                openingBalance = openingBalance,
                status = CashRegisterStatus.OPEN,
                openedAt = now
            )
            val registerId = cashRegisterDao.insert(register)
            Result.success(registerId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun addCashMovement(
        cashRegisterId: Long,
        userId: Long,
        type: MovementType,
        amount: BigDecimal,
        description: String
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (amount < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Amount cannot be negative"))
            }

            val movement = CashMovement(
                cashRegisterId = cashRegisterId,
                userId = userId,
                type = type,
                amount = amount,
                description = description,
                timestamp = LocalDateTime.now()
            )
            val movementId = cashMovementDao.insert(movement)
            Result.success(movementId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun closeCashRegister(
        registerId: Long,
        declaredBalance: BigDecimal
    ): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val register = cashRegisterDao.getRegisterById(registerId)
            if (register == null) {
                return@withContext Result.failure(IllegalArgumentException("Register not found"))
            }

            if (register.status != CashRegisterStatus.OPEN) {
                return@withContext Result.failure(IllegalArgumentException("Register is not open"))
            }

            val movements = cashMovementDao.getMovementsByRegister(registerId)
            val systemTotal = movements.fold(register.openingBalance) { acc, movement ->
                when (movement.type) {
                    MovementType.INCOME, MovementType.SALE -> acc + movement.amount
                    MovementType.EXPENSE, MovementType.REFUND -> acc - movement.amount
                }
            }

            val updatedRegister = register.copy(
                declaredClosingBalance = declaredBalance,
                systemClosingBalance = systemTotal,
                status = CashRegisterStatus.CLOSED,
                closedAt = LocalDateTime.now()
            )
            cashRegisterDao.update(updatedRegister)
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getActiveRegister(userId: Long): Result<CashRegister?> =
        withContext(Dispatchers.IO) {
            try {
                val register = cashRegisterDao.getActiveRegister(CashRegisterStatus.OPEN)
                Result.success(register)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getRegisterMovements(registerId: Long): Result<List<CashMovement>> =
        withContext(Dispatchers.IO) {
            try {
                val movements = cashMovementDao.getMovementsByRegister(registerId)
                Result.success(movements)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
}
