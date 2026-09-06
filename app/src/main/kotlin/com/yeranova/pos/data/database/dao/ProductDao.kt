package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.Product

@Dao
interface ProductDao {
    @Insert
    suspend fun insert(product: Product): Long

    @Update
    suspend fun update(product: Product)

    @Delete
    suspend fun delete(product: Product)

    @Query("SELECT * FROM products WHERE id = :id")
    suspend fun getProductById(id: Long): Product?

    @Query("SELECT * FROM products WHERE code = :code")
    suspend fun getProductByCode(code: String): Product?

    @Query("SELECT * FROM products WHERE barcode = :barcode")
    suspend fun getProductByBarcode(barcode: String): Product?

    @Query("SELECT * FROM products WHERE isActive = 1 ORDER BY name")
    suspend fun getAllActiveProducts(): List<Product>

    @Query("SELECT * FROM products WHERE categoryId = :categoryId AND isActive = 1 ORDER BY name")
    suspend fun getProductsByCategory(categoryId: Long): List<Product>

    @Query("SELECT * FROM products WHERE name LIKE '%' || :query || '%' AND isActive = 1 ORDER BY name")
    suspend fun searchProducts(query: String): List<Product>
}
