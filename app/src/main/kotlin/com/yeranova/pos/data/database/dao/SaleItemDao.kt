package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.SaleItem

@Dao
interface SaleItemDao {
    @Insert
    suspend fun insert(item: SaleItem): Long

    @Update
    suspend fun update(item: SaleItem)

    @Delete
    suspend fun delete(item: SaleItem)

    @Query("SELECT * FROM sale_items WHERE saleId = :saleId")
    suspend fun getItemsBySale(saleId: Long): List<SaleItem>

    @Query("SELECT * FROM sale_items WHERE id = :id")
    suspend fun getItemById(id: Long): SaleItem?
}
