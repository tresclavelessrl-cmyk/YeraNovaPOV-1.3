package com.yeranova.pos.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import java.time.LocalDateTime

enum class AuditAction {
    CREATE,
    READ,
    UPDATE,
    DELETE,
    LOGIN,
    LOGOUT
}

@Entity(
    tableName = "audit_logs",
    foreignKeys = [
        ForeignKey(
            entity = User::class,
            parentColumns = ["id"],
            childColumns = ["userId"],
            onDelete = ForeignKey.SET_NULL
        )
    ]
)
data class AuditLog(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val userId: Long?,
    val action: AuditAction,
    val entityType: String,
    val entityId: Long?,
    val description: String,
    val timestamp: LocalDateTime
)
