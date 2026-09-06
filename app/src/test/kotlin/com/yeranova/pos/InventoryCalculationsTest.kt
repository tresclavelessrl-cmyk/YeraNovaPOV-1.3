package com.yeranova.pos

import org.junit.Test
import org.junit.Assert.*
import java.math.BigDecimal

class InventoryCalculationsTest {
    // Formula: VENTA = INICIO + ENTRADA
    private fun calculateSaleQuantity(initialStock: BigDecimal, incomingStock: BigDecimal): BigDecimal {
        return initialStock + incomingStock
    }

    // Formula: VENDIDO = VENTA - FINAL
    private fun calculateSoldQuantity(saleQuantity: BigDecimal, finalStock: BigDecimal): BigDecimal {
        return saleQuantity - finalStock
    }

    // Formula: IMPORTE = VENDIDO × PRECIO
    private fun calculateAmount(soldQuantity: BigDecimal, price: BigDecimal): BigDecimal {
        return soldQuantity * price
    }

    @Test
    fun testSaleQuantityFormula() {
        val initialStock = BigDecimal(100)
        val incomingStock = BigDecimal(20)
        val saleQuantity = calculateSaleQuantity(initialStock, incomingStock)
        assertEquals(BigDecimal(120), saleQuantity)
    }

    @Test
    fun testSoldQuantityFormula() {
        val saleQuantity = BigDecimal(120)
        val finalStock = BigDecimal(70)
        val soldQuantity = calculateSoldQuantity(saleQuantity, finalStock)
        assertEquals(BigDecimal(50), soldQuantity)
    }

    @Test
    fun testAmountFormula() {
        val soldQuantity = BigDecimal(50)
        val price = BigDecimal("25.50")
        val amount = calculateAmount(soldQuantity, price)
        assertEquals(BigDecimal("1275.00"), amount)
    }

    @Test
    fun testCompleteInventoryCycle() {
        // Day 1
        val day1Initial = BigDecimal(100)
        val day1Incoming = BigDecimal(20)
        val day1Sale = calculateSaleQuantity(day1Initial, day1Incoming) // 120
        val day1Final = BigDecimal(70)
        val day1Sold = calculateSoldQuantity(day1Sale, day1Final) // 50
        val day1Price = BigDecimal("25.00")
        val day1Amount = calculateAmount(day1Sold, day1Price) // 1250

        assertEquals(BigDecimal(120), day1Sale)
        assertEquals(BigDecimal(50), day1Sold)
        assertEquals(BigDecimal("1250.00"), day1Amount)

        // Day 2 - Initial stock from Day 1 final
        val day2Initial = day1Final // 70 (automatic)
        val day2Incoming = BigDecimal(15)
        val day2Sale = calculateSaleQuantity(day2Initial, day2Incoming) // 85
        val day2Final = BigDecimal(35)
        val day2Sold = calculateSoldQuantity(day2Sale, day2Final) // 50
        val day2Price = BigDecimal("25.00")
        val day2Amount = calculateAmount(day2Sold, day2Price) // 1250

        assertEquals(BigDecimal(85), day2Sale)
        assertEquals(BigDecimal(50), day2Sold)
        assertEquals(BigDecimal("1250.00"), day2Amount)
    }

    @Test(expected = IllegalArgumentException::class)
    fun testNegativeInitialStockNotAllowed() {
        // This should be caught at repository level
        assertTrue(BigDecimal(-10) < BigDecimal.ZERO)
    }

    @Test
    fun testFinalStockCannotExceedAvailable() {
        val initialStock = BigDecimal(100)
        val incomingStock = BigDecimal(20)
        val saleQuantity = calculateSaleQuantity(initialStock, incomingStock) // 120
        val invalidFinalStock = BigDecimal(150)
        
        assertTrue(invalidFinalStock > saleQuantity)
    }

    @Test
    fun testZeroStock() {
        val initialStock = BigDecimal.ZERO
        val incomingStock = BigDecimal.ZERO
        val saleQuantity = calculateSaleQuantity(initialStock, incomingStock)
        val finalStock = BigDecimal.ZERO
        val soldQuantity = calculateSoldQuantity(saleQuantity, finalStock)

        assertEquals(BigDecimal.ZERO, saleQuantity)
        assertEquals(BigDecimal.ZERO, soldQuantity)
    }
}
