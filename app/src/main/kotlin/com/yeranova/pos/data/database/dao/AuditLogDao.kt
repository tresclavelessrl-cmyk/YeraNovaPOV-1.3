package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.AuditLog
import com.yeranova.pos.data.model.AuditAction

@Dao
interface AuditLogDao {
    @Insert
    suspend fun insert(log: AuditLog): Long

    @Query("SELECT * FROM audit_logs WHERE userId = :userId ORDER BY timestamp DESC")
    suspend fun getLogsByUser(userId: Long): List<AuditLog>

    @Query("SELECT * FROM audit_logs WHERE action = :action ORDER BY timestamp DESC")
    suspend fun getLogsByAction(action: AuditAction): List<AuditLog>

    @Query("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT :limit")
    suspend fun getRecentLogs(limit: Int = 100): List<AuditLog>
}
