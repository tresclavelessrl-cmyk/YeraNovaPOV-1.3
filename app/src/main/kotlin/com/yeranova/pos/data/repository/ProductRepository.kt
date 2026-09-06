package com.yeranova.pos.data.repository

import com.yeranova.pos.data.database.dao.ProductDao
import com.yeranova.pos.data.model.Product
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.time.LocalDateTime
import java.math.BigDecimal

class ProductRepository(private val productDao: ProductDao) {
    suspend fun createProduct(
        code: String,
        name: String,
        description: String,
        categoryId: Long,
        price: BigDecimal,
        barcode: String? = null
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (code.isBlank() || name.isBlank()) {
                return@withContext Result.failure(IllegalArgumentException("Code and name cannot be empty"))
            }

            if (price < BigDecimal.ZERO) {
                return@withContext Result.failure(IllegalArgumentException("Price cannot be negative"))
            }

            val now = LocalDateTime.now()
            val product = Product(
                code = code,
                name = name,
                description = description,
                categoryId = categoryId,
                price = price,
                barcode = barcode,
                createdAt = now,
                updatedAt = now
            )
            val productId = productDao.insert(product)
            Result.success(productId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getProductById(id: Long): Result<Product?> = withContext(Dispatchers.IO) {
        try {
            val product = productDao.getProductById(id)
            Result.success(product)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getProductByBarcode(barcode: String): Result<Product?> =
        withContext(Dispatchers.IO) {
            try {
                val product = productDao.getProductByBarcode(barcode)
                Result.success(product)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getAllActiveProducts(): Result<List<Product>> = withContext(Dispatchers.IO) {
        try {
            val products = productDao.getAllActiveProducts()
            Result.success(products)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun searchProducts(query: String): Result<List<Product>> =
        withContext(Dispatchers.IO) {
            try {
                val products = productDao.searchProducts(query)
                Result.success(products)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun updateProduct(product: Product): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            productDao.update(product.copy(updatedAt = LocalDateTime.now()))
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deactivateProduct(id: Long): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val product = productDao.getProductById(id)
            if (product != null) {
                productDao.update(product.copy(isActive = false, updatedAt = LocalDateTime.now()))
                Result.success(Unit)
            } else {
                Result.failure(IllegalArgumentException("Product not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
