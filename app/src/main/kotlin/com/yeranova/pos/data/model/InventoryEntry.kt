package com.yeranova.pos.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import java.time.LocalDate
import java.time.LocalDateTime
import java.math.BigDecimal

@Entity(
    tableName = "inventory_entries",
    foreignKeys = [
        ForeignKey(
            entity = Product::class,
            parentColumns = ["id"],
            childColumns = ["productId"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class InventoryEntry(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val productId: Long,
    val date: LocalDate,
    val initialStock: BigDecimal,
    val incomingStock: BigDecimal = BigDecimal.ZERO,
    val saleQuantity: BigDecimal = BigDecimal.ZERO,
    val finalStock: BigDecimal = BigDecimal.ZERO,
    val price: BigDecimal,
    val createdAt: LocalDateTime,
    val updatedAt: LocalDateTime
)
