package com.yeranova.pos.data.repository

import com.yeranova.pos.data.database.dao.InventoryEntryDao
import com.yeranova.pos.data.model.InventoryEntry
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.LocalDate
import java.time.LocalDateTime
import java.math.BigDecimal

class InventoryRepository(private val inventoryEntryDao: InventoryEntryDao) {
    // Formula: VENTA = INICIO + ENTRADA
    private fun calculateSaleQuantity(initialStock: BigDecimal, incomingStock: BigDecimal): BigDecimal {
        return initialStock + incomingStock
    }

    // Formula: VENDIDO = VENTA - FINAL
    private fun calculateSoldQuantity(saleQuantity: BigDecimal, finalStock: BigDecimal): BigDecimal {
        return saleQuantity - finalStock
    }

    // Formula: IMPORTE = VENDIDO × PRECIO
    private fun calculateAmount(soldQuantity: BigDecimal, price: BigDecimal): BigDecimal {
        return soldQuantity * price
    }

    suspend fun createInventoryEntry(
        productId: Long,
        date: LocalDate,
        initialStock: BigDecimal,
        incomingStock: BigDecimal = BigDecimal.ZERO,
        finalStock: BigDecimal = BigDecimal.ZERO,
        price: BigDecimal
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (initialStock < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Initial stock cannot be negative"))
            }
            if (incomingStock < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Incoming stock cannot be negative"))
            }
            if (price < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Price cannot be negative"))
            }

            val saleQuantity = calculateSaleQuantity(initialStock, incomingStock)
            if (finalStock > saleQuantity) {
                return@withContext Result.failure(IllegalArgumentException("Final stock cannot exceed available quantity"))
            }

            val now = LocalDateTime.now()
            val entry = InventoryEntry(
                productId = productId,
                date = date,
                initialStock = initialStock,
                incomingStock = incomingStock,
                saleQuantity = saleQuantity,
                finalStock = finalStock,
                price = price,
                createdAt = now,
                updatedAt = now
            )
            val entryId = inventoryEntryDao.insert(entry)
            Result.success(entryId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateInventoryEntry(entry: InventoryEntry): Result<Unit> =
        withContext(Dispatchers.IO) {
            try {
                // Validate formulas
                val saleQuantity = calculateSaleQuantity(entry.initialStock, entry.incomingStock)
                if (entry.finalStock > saleQuantity) {
                    return@withContext Result.failure(IllegalArgumentException("Final stock cannot exceed available quantity"))
                }
                if (entry.finalStock < BigDecimal.ZERO) {
                    return@withContext Result.failure(IllegalArgumentException("Final stock cannot be negative"))
                }

                inventoryEntryDao.update(entry.copy(updatedAt = LocalDateTime.now()))
                Result.success(Unit)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getEntriesByDate(date: LocalDate): Result<List<InventoryEntry>> =
        withContext(Dispatchers.IO) {
            try {
                val entries = inventoryEntryDao.getEntriesByDate(date)
                Result.success(entries)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getEntriesByDateRange(
        startDate: LocalDate,
        endDate: LocalDate
    ): Result<List<InventoryEntry>> = withContext(Dispatchers.IO) {
        try {
            val entries = inventoryEntryDao.getEntriesByDateRange(startDate, endDate)
            Result.success(entries)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getLatestEntryByProduct(productId: Long): Result<InventoryEntry?> =
        withContext(Dispatchers.IO) {
            try {
                val entry = inventoryEntryDao.getLatestEntryByProduct(productId)
                Result.success(entry)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getNextDayInitialStock(productId: Long, date: LocalDate): Result<BigDecimal> =
        withContext(Dispatchers.IO) {
            try {
                val previousDay = date.minusDays(1)
                val previousEntry = inventoryEntryDao.getEntryByProductAndDate(productId, previousDay)
                val initialStock = previousEntry?.finalStock ?: BigDecimal.ZERO
                Result.success(initialStock)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun calculateDailyTotal(date: LocalDate): Result<BigDecimal> =
        withContext(Dispatchers.IO) {
            try {
                val entries = inventoryEntryDao.getEntriesByDate(date)
                val total = entries.fold(BigDecimal.ZERO) { acc, entry ->
                    val saleQuantity = calculateSaleQuantity(entry.initialStock, entry.incomingStock)
                    val soldQuantity = calculateSoldQuantity(saleQuantity, entry.finalStock)
                    val amount = calculateAmount(soldQuantity, entry.price)
                    acc + amount
                }
                Result.success(total)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }
}
