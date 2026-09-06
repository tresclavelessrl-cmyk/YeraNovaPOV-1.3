package com.yeranova.pos.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import java.time.LocalDateTime
import java.math.BigDecimal

enum class MovementType {
    INCOME,
    EXPENSE,
    SALE,
    REFUND
}

@Entity(
    tableName = "cash_movements",
    foreignKeys = [
        ForeignKey(
            entity = CashRegister::class,
            parentColumns = ["id"],
            childColumns = ["cashRegisterId"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = User::class,
            parentColumns = ["id"],
            childColumns = ["userId"],
            onDelete = ForeignKey.RESTRICT
        )
    ]
)
data class CashMovement(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val cashRegisterId: Long,
    val userId: Long,
    val type: MovementType,
    val amount: BigDecimal,
    val description: String,
    val timestamp: LocalDateTime
)
