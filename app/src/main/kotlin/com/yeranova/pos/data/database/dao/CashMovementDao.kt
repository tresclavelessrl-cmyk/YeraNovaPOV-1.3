package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.CashMovement
import com.yeranova.pos.data.model.MovementType

@Dao
interface CashMovementDao {
    @Insert
    suspend fun insert(movement: CashMovement): Long

    @Update
    suspend fun update(movement: CashMovement)

    @Delete
    suspend fun delete(movement: CashMovement)

    @Query("SELECT * FROM cash_movements WHERE cashRegisterId = :registerId ORDER BY timestamp DESC")
    suspend fun getMovementsByRegister(registerId: Long): List<CashMovement>

    @Query("SELECT * FROM cash_movements WHERE cashRegisterId = :registerId AND type = :type")
    suspend fun getMovementsByType(registerId: Long, type: MovementType): List<CashMovement>
}
