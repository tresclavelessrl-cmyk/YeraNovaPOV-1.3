package com.yeranova.pos.data.repository

import com.yeranova.pos.data.database.dao.SaleDao
import com.yeranova.pos.data.database.dao.SaleItemDao
import com.yeranova.pos.data.model.Sale
import com.yeranova.pos.data.model.SaleItem
import com.yeranova.pos.data.model.SaleStatus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.LocalDateTime
import java.math.BigDecimal

class SaleRepository(
    private val saleDao: SaleDao,
    private val saleItemDao: SaleItemDao
) {
    suspend fun createSale(
        userId: Long,
        cashRegisterId: Long,
        items: List<SaleItem>,
        discount: BigDecimal = BigDecimal.ZERO,
        tax: BigDecimal = BigDecimal.ZERO
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (items.isEmpty()) {
                return@withContext Result.failure(IllegalArgumentException("Sale must have at least one item"))
            }

            val subtotal = items.fold(BigDecimal.ZERO) { acc, item -> acc + item.subtotal }
            val total = subtotal + tax - discount

            if (total < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Sale total cannot be negative"))
            }

            val now = LocalDateTime.now()
            val sale = Sale(
                userId = userId,
                cashRegisterId = cashRegisterId,
                subtotal = subtotal,
                discount = discount,
                tax = tax,
                total = total,
                status = SaleStatus.COMPLETED,
                saleDate = now,
                createdAt = now,
                updatedAt = now
            )
            val saleId = saleDao.insert(sale)

            // Insert sale items
            items.forEach { item ->
                saleItemDao.insert(item.copy(saleId = saleId))
            }

            Result.success(saleId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getSaleById(id: Long): Result<Sale?> = withContext(Dispatchers.IO) {
        try {
            val sale = saleDao.getSaleById(id)
            Result.success(sale)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getSalesByDateRange(
        startDate: LocalDateTime,
        endDate: LocalDateTime
    ): Result<List<Sale>> = withContext(Dispatchers.IO) {
        try {
            val sales = saleDao.getSalesByDateRange(startDate, endDate)
            Result.success(sales)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getSaleItemsBySale(saleId: Long): Result<List<SaleItem>> =
        withContext(Dispatchers.IO) {
            try {
                val items = saleItemDao.getItemsBySale(saleId)
                Result.success(items)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
}
