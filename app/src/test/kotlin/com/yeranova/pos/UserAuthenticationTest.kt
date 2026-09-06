package com.yeranova.pos

import org.junit.Test
import org.junit.Assert.*
import org.mindrot.jbcrypt.BCrypt

class UserAuthenticationTest {
    @Test
    fun testPasswordHashing() {
        val password = "testPassword123"
        val hash = BCrypt.hashpw(password, BCrypt.gensalt())
        
        assertNotEquals(password, hash)
        assertTrue(BCrypt.checkpw(password, hash))
    }

    @Test
    fun testPasswordVerification() {
        val password = "correctPassword"
        val wrongPassword = "wrongPassword"
        val hash = BCrypt.hashpw(password, BCrypt.gensalt())

        assertTrue(BCrypt.checkpw(password, hash))
        assertFalse(BCrypt.checkpw(wrongPassword, hash))
    }

    @Test
    fun testDifferentHashesSamePassword() {
        val password = "samePassword"
        val hash1 = BCrypt.hashpw(password, BCrypt.gensalt())
        val hash2 = BCrypt.hashpw(password, BCrypt.gensalt())

        assertNotEquals(hash1, hash2)
        assertTrue(BCrypt.checkpw(password, hash1))
        assertTrue(BCrypt.checkpw(password, hash2))
    }
}
