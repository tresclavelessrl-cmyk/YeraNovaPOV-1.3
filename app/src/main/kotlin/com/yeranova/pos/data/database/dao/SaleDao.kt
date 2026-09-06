package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.Sale
import com.yeranova.pos.data.model.SaleStatus
import java.time.LocalDateTime

@Dao
interface SaleDao {
    @Insert
    suspend fun insert(sale: Sale): Long

    @Update
    suspend fun update(sale: Sale)

    @Delete
    suspend fun delete(sale: Sale)

    @Query("SELECT * FROM sales WHERE id = :id")
    suspend fun getSaleById(id: Long): Sale?

    @Query("SELECT * FROM sales WHERE status = :status ORDER BY saleDate DESC")
    suspend fun getSalesByStatus(status: SaleStatus): List<Sale>

    @Query("SELECT * FROM sales WHERE saleDate BETWEEN :startDate AND :endDate ORDER BY saleDate DESC")
    suspend fun getSalesByDateRange(startDate: LocalDateTime, endDate: LocalDateTime): List<Sale>

    @Query("SELECT * FROM sales WHERE userId = :userId AND saleDate BETWEEN :startDate AND :endDate ORDER BY saleDate DESC")
    suspend fun getSalesByUserAndDateRange(userId: Long, startDate: LocalDateTime, endDate: LocalDateTime): List<Sale>
}
