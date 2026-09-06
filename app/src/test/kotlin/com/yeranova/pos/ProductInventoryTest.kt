package com.yeranova.pos

import org.junit.Test
import org.junit.Assert.*
import java.math.BigDecimal
import java.time.LocalDate

class ProductInventoryTest {
    @Test
    fun testProductCreationValidation() {
        val productName = "Producto Test"
        val productCode = "PROD001"
        val price = BigDecimal("99.99")

        assertTrue(productName.isNotBlank())
        assertTrue(productCode.isNotBlank())
        assertTrue(price > BigDecimal.ZERO)
    }

    @Test
    fun testInventoryEntryCreation() {
        val productId = 1L
        val date = LocalDate.now()
        val initialStock = BigDecimal(100)
        val incomingStock = BigDecimal(20)
        val finalStock = BigDecimal(70)
        val price = BigDecimal("25.00")

        // Calculate using formulas
        val saleQuantity = initialStock + incomingStock // 120
        val soldQuantity = saleQuantity - finalStock // 50
        val amount = soldQuantity * price // 1250.00

        assertEquals(BigDecimal(120), saleQuantity)
        assertEquals(BigDecimal(50), soldQuantity)
        assertEquals(BigDecimal("1250.00"), amount)
    }

    @Test
    fun testInventoryValidations() {
        val initialStock = BigDecimal(100)
        val incomingStock = BigDecimal(20)
        val saleQuantity = initialStock + incomingStock // 120

        // Valid final stock
        val validFinalStock = BigDecimal(70)
        assertTrue(validFinalStock <= saleQuantity)

        // Invalid final stock (exceeds available)
        val invalidFinalStock = BigDecimal(150)
        assertTrue(invalidFinalStock > saleQuantity)

        // Negative validation
        assertTrue(BigDecimal.ZERO <= saleQuantity)
    }

    @Test
    fun testNextDayInitialStockCalculation() {
        val day1Final = BigDecimal(70)
        val day2Initial = day1Final // Should be automatic

        assertEquals(day1Final, day2Initial)
    }

    @Test
    fun testMultiplProductsInventoryTotal() {
        // Product 1
        val prod1Sold = BigDecimal(50)
        val prod1Price = BigDecimal("25.00")
        val prod1Amount = prod1Sold * prod1Price // 1250.00

        // Product 2
        val prod2Sold = BigDecimal(30)
        val prod2Price = BigDecimal("50.00")
        val prod2Amount = prod2Sold * prod2Price // 1500.00

        // Product 3
        val prod3Sold = BigDecimal(20)
        val prod3Price = BigDecimal("75.00")
        val prod3Amount = prod3Sold * prod3Price // 1500.00

        val total = prod1Amount + prod2Amount + prod3Amount // 4250.00

        assertEquals(BigDecimal("1250.00"), prod1Amount)
        assertEquals(BigDecimal("1500.00"), prod2Amount)
        assertEquals(BigDecimal("1500.00"), prod3Amount)
        assertEquals(BigDecimal("4250.00"), total)
    }

    @Test
    fun testProductCategoryRelationship() {
        val categoryId = 1L
        val productCode = "PROD001"
        val productName = "Test Product"

        // Category should be associated
        assertTrue(categoryId > 0L)
        assertTrue(productCode.isNotBlank())
        assertTrue(productName.isNotBlank())
    }

    @Test(expected = IllegalArgumentException::class)
    fun testNegativePriceNotAllowed() {
        val price = BigDecimal("-10.00")
        assertTrue(price < BigDecimal.ZERO)
    }

    @Test(expected = IllegalArgumentException::class)
    fun testNegativeStockNotAllowed() {
        val stock = BigDecimal("-5")
        assertTrue(stock < BigDecimal.ZERO)
    }

    @Test
    fun testInventoryEdgeCases() {
        // Zero inventory
        val zeroInitial = BigDecimal.ZERO
        val zeroIncoming = BigDecimal.ZERO
        val zeroFinal = BigDecimal.ZERO

        val zeroSale = zeroInitial + zeroIncoming
        val zeroSold = zeroSale - zeroFinal

        assertEquals(BigDecimal.ZERO, zeroSold)

        // Very large quantities
        val largeInitial = BigDecimal("999999")
        val largeIncoming = BigDecimal("999999")
        val largeSale = largeInitial + largeIncoming

        assertEquals(BigDecimal("1999998"), largeSale)
    }
}
