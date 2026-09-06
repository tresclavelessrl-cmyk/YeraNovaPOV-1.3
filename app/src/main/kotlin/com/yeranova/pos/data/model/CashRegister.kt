package com.yeranova.pos.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import java.time.LocalDateTime
import java.math.BigDecimal

enum class CashRegisterStatus {
    OPEN,
    CLOSED
}

@Entity(
    tableName = "cash_registers",
    foreignKeys = [
        ForeignKey(
            entity = User::class,
            parentColumns = ["id"],
            childColumns = ["userId"],
            onDelete = ForeignKey.RESTRICT
        )
    ]
)
data class CashRegister(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val userId: Long,
    val openingBalance: BigDecimal,
    val declaredClosingBalance: BigDecimal? = null,
    val systemClosingBalance: BigDecimal? = null,
    val status: CashRegisterStatus = CashRegisterStatus.OPEN,
    val openedAt: LocalDateTime,
    val closedAt: LocalDateTime? = null
)
