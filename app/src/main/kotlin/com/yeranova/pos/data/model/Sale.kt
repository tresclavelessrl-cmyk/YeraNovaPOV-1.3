package com.yeranova.pos.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import java.time.LocalDateTime
import java.math.BigDecimal

enum class SaleStatus {
    PENDING,
    COMPLETED,
    CANCELLED
}

@Entity(
    tableName = "sales",
    foreignKeys = [
        ForeignKey(
            entity = User::class,
            parentColumns = ["id"],
            childColumns = ["userId"],
            onDelete = ForeignKey.RESTRICT
        ),
        ForeignKey(
            entity = CashRegister::class,
            parentColumns = ["id"],
            childColumns = ["cashRegisterId"],
            onDelete = ForeignKey.RESTRICT
        )
    ]
)
data class Sale(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val userId: Long,
    val cashRegisterId: Long,
    val subtotal: BigDecimal,
    val discount: BigDecimal = BigDecimal.ZERO,
    val tax: BigDecimal = BigDecimal.ZERO,
    val total: BigDecimal,
    val status: SaleStatus = SaleStatus.PENDING,
    val saleDate: LocalDateTime,
    val createdAt: LocalDateTime,
    val updatedAt: LocalDateTime
)
