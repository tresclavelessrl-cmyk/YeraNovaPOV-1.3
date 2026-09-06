package com.yeranova.pos.data.repository

import com.yeranova.pos.data.database.dao.UserDao
import com.yeranova.pos.data.model.User
import com.yeranova.pos.data.model.UserRole
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.mindrot.jbcrypt.BCrypt
import java.time.LocalDateTime

class UserRepository(private val userDao: UserDao) {
    suspend fun createUser(
        username: String,
        password: String,
        fullName: String,
        email: String,
        role: UserRole
    ): Result<Long> = withContext(Dispatchers.IO) {
        try {
            if (username.isBlank() || password.isBlank()) {
                return@withContext Result.failure(IllegalArgumentException("Username and password cannot be empty"))
            }

            val existingUser = userDao.getUserByUsername(username)
            if (existingUser != null) {
                return@withContext Result.failure(IllegalArgumentException("Username already exists"))
            }

            val passwordHash = BCrypt.hashpw(password, BCrypt.gensalt())
            val now = LocalDateTime.now()
            val user = User(
                username = username,
                passwordHash = passwordHash,
                fullName = fullName,
                email = email,
                role = role,
                createdAt = now,
                updatedAt = now
            )
            val userId = userDao.insert(user)
            Result.success(userId)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun authenticateUser(username: String, password: String): Result<User> =
        withContext(Dispatchers.IO) {
            try {
                val user = userDao.getUserByUsername(username)
                if (user == null) {
                    return@withContext Result.failure(IllegalArgumentException("User not found"))
                }

                if (!user.isActive) {
                    return@withContext Result.failure(IllegalArgumentException("User is inactive"))
                }

                if (!BCrypt.checkpw(password, user.passwordHash)) {
                    return@withContext Result.failure(IllegalArgumentException("Invalid password"))
                }

                val updatedUser = user.copy(
                    lastLogin = LocalDateTime.now(),
                    updatedAt = LocalDateTime.now()
                )
                userDao.update(updatedUser)
                Result.success(updatedUser)
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    suspend fun getUserById(id: Long): Result<User?> = withContext(Dispatchers.IO) {
        try {
            val user = userDao.getUserById(id)
            Result.success(user)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun getAllActiveUsers(): Result<List<User>> = withContext(Dispatchers.IO) {
        try {
            val users = userDao.getAllActiveUsers()
            Result.success(users)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun updateUser(user: User): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            userDao.update(user.copy(updatedAt = LocalDateTime.now()))
            Result.success(Unit)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun deactivateUser(id: Long): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val user = userDao.getUserById(id)
            if (user != null) {
                userDao.update(user.copy(isActive = false, updatedAt = LocalDateTime.now()))
                Result.success(Unit)
            } else {
                Result.failure(IllegalArgumentException("User not found"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
