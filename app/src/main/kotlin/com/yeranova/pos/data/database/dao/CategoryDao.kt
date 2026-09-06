package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.Category

@Dao
interface CategoryDao {
    @Insert
    suspend fun insert(category: Category): Long

    @Update
    suspend fun update(category: Category)

    @Delete
    suspend fun delete(category: Category)

    @Query("SELECT * FROM categories WHERE id = :id")
    suspend fun getCategoryById(id: Long): Category?

    @Query("SELECT * FROM categories WHERE isActive = 1 ORDER BY name")
    suspend fun getAllActiveCategories(): List<Category>

    @Query("SELECT * FROM categories ORDER BY name")
    suspend fun getAllCategories(): List<Category>
}
