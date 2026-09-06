package com.yeranova.pos.data.repository

import com.yeranova.pos.data.database.dao.CategoryDao
import com.yeranova.pos.data.model.Category
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class CategoryRepository(private val categoryDao: CategoryDao) {
    suspend fun createCategory(
        name: String,
        description: String = ""
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (name.isBlank()) {
                return@withContext Result.failure(IllegalArgumentException("Category name cannot be empty"))
            }

            val category = Category(
                name = name,
                description = description.ifBlank { null },
                isActive = true
            )
            val categoryId = categoryDao.insert(category)
            Result.success(categoryId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateCategory(category: Category): Result<Unit> =
        withContext(Dispatchers.IO) {
            try {
                if (category.name.isBlank()) {
                    return@withContext Result.failure(IllegalArgumentException("Category name cannot be empty"))
                }
                categoryDao.update(category)
                Result.success(Unit)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun deactivateCategory(id: Long): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val category = categoryDao.getCategoryById(id)
            if (category != null) {
                categoryDao.update(category.copy(isActive = false))
                Result.success(Unit)
            } else {
                Result.failure(IllegalArgumentException("Category not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getCategoryById(id: Long): Result<Category?> = withContext(Dispatchers.IO) {
        try {
            val category = categoryDao.getCategoryById(id)
            Result.success(category)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getAllActiveCategories(): Result<List<Category>> =
        withContext(Dispatchers.IO) {
            try {
                val categories = categoryDao.getAllActiveCategories()
                Result.success(categories)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getAllCategories(): Result<List<Category>> = withContext(Dispatchers.IO) {
        try {
            val categories = categoryDao.getAllCategories()
            Result.success(categories)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
