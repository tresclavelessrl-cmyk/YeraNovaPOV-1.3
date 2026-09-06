package com.yeranova.pos.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.yeranova.pos.data.model.InventoryEntry
import com.yeranova.pos.data.model.Product
import com.yeranova.pos.data.repository.InventoryRepository
import com.yeranova.pos.data.repository.ProductRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.math.BigDecimal

data class InventoryUiState(
    val date: LocalDate = LocalDate.now(),
    val entries: List<InventoryEntry> = emptyList(),
    val products: List<Product> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val showDialog: Boolean = false,
    val selectedEntry: InventoryEntry? = null,
    val dailyTotal: BigDecimal = BigDecimal.ZERO
)

class InventoryViewModel(
    private val inventoryRepository: InventoryRepository,
    private val productRepository: ProductRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(InventoryUiState())
    val uiState: StateFlow<InventoryUiState> = _uiState.asStateFlow()

    init {
        loadInventoryForToday()
        loadProducts()
    }

    private fun loadInventoryForToday() {
        val today = LocalDate.now()
        loadInventoryForDate(today)
    }

    private fun loadInventoryForDate(date: LocalDate) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, date = date)
            val result = inventoryRepository.getEntriesByDate(date)
            result.onSuccess { entries ->
                viewModelScope.launch {
                    val totalResult = inventoryRepository.calculateDailyTotal(date)
                    val total = totalResult.getOrNull() ?: BigDecimal.ZERO
                    _uiState.value = _uiState.value.copy(
                        entries = entries,
                        isLoading = false,
                        error = null,
                        dailyTotal = total
                    )
                }
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error desconocido"
                )
            }
        }
    }

    private fun loadProducts() {
        viewModelScope.launch {
            val result = productRepository.getAllActiveProducts()
            result.onSuccess { products ->
                _uiState.value = _uiState.value.copy(products = products)
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    error = exception.message ?: "Error al cargar productos"
                )
            }
        }
    }

    fun createInventoryEntry(
        productId: Long,
        initialStock: BigDecimal,
        incomingStock: BigDecimal,
        finalStock: BigDecimal,
        price: BigDecimal
    ) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = inventoryRepository.createInventoryEntry(
                productId = productId,
                date = _uiState.value.date,
                initialStock = initialStock,
                incomingStock = incomingStock,
                finalStock = finalStock,
                price = price
            )
            result.onSuccess {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    showDialog = false,
                    error = null
                )
                loadInventoryForDate(_uiState.value.date)
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error al crear entrada de inventario"
                )
            }
        }
    }

    fun updateInventoryEntry(entry: InventoryEntry) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = inventoryRepository.updateInventoryEntry(entry)
            result.onSuccess {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    showDialog = false,
                    error = null
                )
                loadInventoryForDate(_uiState.value.date)
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error al actualizar entrada de inventario"
                )
            }
        }
    }

    fun changeDate(date: LocalDate) {
        loadInventoryForDate(date)
    }

    fun showDialog() {
        _uiState.value = _uiState.value.copy(showDialog = true, selectedEntry = null)
    }

    fun hideDialog() {
        _uiState.value = _uiState.value.copy(showDialog = false, selectedEntry = null)
    }

    fun selectEntry(entry: InventoryEntry) {
        _uiState.value = _uiState.value.copy(selectedEntry = entry, showDialog = true)
    }

    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }
}
