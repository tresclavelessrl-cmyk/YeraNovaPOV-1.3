package com.yeranova.pos.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.time.LocalDateTime

enum class UserRole {
    ADMIN,
    MANAGER,
    VENDOR
}

@Entity(tableName = "users")
data class User(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val username: String,
    val passwordHash: String,
    val fullName: String,
    val email: String,
    val role: UserRole,
    val isActive: Boolean = true,
    val createdAt: LocalDateTime,
    val updatedAt: LocalDateTime,
    val lastLogin: LocalDateTime? = null
)
