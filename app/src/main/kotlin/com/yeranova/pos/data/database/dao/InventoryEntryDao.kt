package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.InventoryEntry
import java.time.LocalDate

@Dao
interface InventoryEntryDao {
    @Insert
    suspend fun insert(entry: InventoryEntry): Long

    @Update
    suspend fun update(entry: InventoryEntry)

    @Delete
    suspend fun delete(entry: InventoryEntry)

    @Query("SELECT * FROM inventory_entries WHERE id = :id")
    suspend fun getEntryById(id: Long): InventoryEntry?

    @Query("SELECT * FROM inventory_entries WHERE productId = :productId AND date = :date")
    suspend fun getEntryByProductAndDate(productId: Long, date: LocalDate): InventoryEntry?

    @Query("SELECT * FROM inventory_entries WHERE date = :date ORDER BY productId")
    suspend fun getEntriesByDate(date: LocalDate): List<InventoryEntry>

    @Query("SELECT * FROM inventory_entries WHERE date BETWEEN :startDate AND :endDate ORDER BY date DESC, productId")
    suspend fun getEntriesByDateRange(startDate: LocalDate, endDate: LocalDate): List<InventoryEntry>

    @Query("SELECT * FROM inventory_entries WHERE productId = :productId ORDER BY date DESC LIMIT 1")
    suspend fun getLatestEntryByProduct(productId: Long): InventoryEntry?
}
