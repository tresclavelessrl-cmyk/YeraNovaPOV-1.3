package com.yeranova.pos.data.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.yeranova.pos.data.database.converter.DateConverter
import com.yeranova.pos.data.database.dao.UserDao
import com.yeranova.pos.data.database.dao.ProductDao
import com.yeranova.pos.data.database.dao.InventoryEntryDao
import com.yeranova.pos.data.database.dao.SaleDao
import com.yeranova.pos.data.database.dao.SaleItemDao
import com.yeranova.pos.data.database.dao.CashRegisterDao
import com.yeranova.pos.data.database.dao.CashMovementDao
import com.yeranova.pos.data.database.dao.AuditLogDao
import com.yeranova.pos.data.database.dao.CategoryDao
import com.yeranova.pos.data.model.User
import com.yeranova.pos.data.model.Product
import com.yeranova.pos.data.model.Category
import com.yeranova.pos.data.model.InventoryEntry
import com.yeranova.pos.data.model.Sale
import com.yeranova.pos.data.model.SaleItem
import com.yeranova.pos.data.model.CashRegister
import com.yeranova.pos.data.model.CashMovement
import com.yeranova.pos.data.model.AuditLog

@Database(
    entities = [
        User::class,
        Product::class,
        Category::class,
        InventoryEntry::class,
        Sale::class,
        SaleItem::class,
        CashRegister::class,
        CashMovement::class,
        AuditLog::class
    ],
    version = 1,
    exportSchema = true
)
@TypeConverters(DateConverter::class)
abstract class YeraNovaPOSDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun productDao(): ProductDao
    abstract fun categoryDao(): CategoryDao
    abstract fun inventoryEntryDao(): InventoryEntryDao
    abstract fun saleDao(): SaleDao
    abstract fun saleItemDao(): SaleItemDao
    abstract fun cashRegisterDao(): CashRegisterDao
    abstract fun cashMovementDao(): CashMovementDao
    abstract fun auditLogDao(): AuditLogDao

    companion object {
        @Volatile
        private var instance: YeraNovaPOSDatabase? = null

        fun getInstance(context: Context): YeraNovaPOSDatabase {
            return instance ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    YeraNovaPOSDatabase::class.java,
                    "yeranova_pos.db"
                )
                .addMigrations() // Future migrations go here
                .build()
                .also { instance = it }
            }
        }
    }
}
