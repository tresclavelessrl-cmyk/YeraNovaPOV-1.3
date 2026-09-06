package com.yeranova.pos.data.database.dao

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.yeranova.pos.data.model.CashRegister
import com.yeranova.pos.data.model.CashRegisterStatus

@Dao
interface CashRegisterDao {
    @Insert
    suspend fun insert(register: CashRegister): Long

    @Update
    suspend fun update(register: CashRegister)

    @Delete
    suspend fun delete(register: CashRegister)

    @Query("SELECT * FROM cash_registers WHERE id = :id")
    suspend fun getRegisterById(id: Long): CashRegister?

    @Query("SELECT * FROM cash_registers WHERE status = :status ORDER BY openedAt DESC LIMIT 1")
    suspend fun getActiveRegister(status: CashRegisterStatus): CashRegister?

    @Query("SELECT * FROM cash_registers WHERE userId = :userId ORDER BY openedAt DESC")
    suspend fun getRegistersByUser(userId: Long): List<CashRegister>
}
