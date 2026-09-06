package com.yeranova.pos.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.yeranova.pos.data.model.Product
import com.yeranova.pos.data.repository.ProductRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.math.BigDecimal

data class ProductUiState(
    val products: List<Product> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val showDialog: Boolean = false,
    val selectedProduct: Product? = null,
    val searchQuery: String = ""
)

class ProductViewModel(private val repository: ProductRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(ProductUiState())
    val uiState: StateFlow<ProductUiState> = _uiState.asStateFlow()

    init {
        loadProducts()
    }

    private fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.getAllActiveProducts()
            result.onSuccess { products ->
                _uiState.value = _uiState.value.copy(
                    products = products,
                    isLoading = false,
                    error = null
                )
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error desconocido"
                )
            }
        }
    }

    fun searchProducts(query: String) {
        _uiState.value = _uiState.value.copy(searchQuery = query)
        if (query.isBlank()) {
            loadProducts()
            return
        }

        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.searchProducts(query)
            result.onSuccess { products ->
                _uiState.value = _uiState.value.copy(
                    products = products,
                    isLoading = false,
                    error = null
                )
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error en la búsqueda"
                )
            }
        }
    }

    fun createProduct(
        code: String,
        name: String,
        description: String,
        categoryId: Long,
        price: BigDecimal,
        barcode: String? = null
    ) {
        if (code.isBlank() || name.isBlank()) {
            _uiState.value = _uiState.value.copy(error = "Código y nombre son obligatorios")
            return
        }

        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.createProduct(code, name, description, categoryId, price, barcode)
            result.onSuccess {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    showDialog = false,
                    error = null
                )
                loadProducts()
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error al crear producto"
                )
            }
        }
    }

    fun updateProduct(product: Product) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.updateProduct(product)
            result.onSuccess {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    showDialog = false,
                    error = null
                )
                loadProducts()
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error al actualizar producto"
                )
            }
        }
    }

    fun deactivateProduct(id: Long) {
        viewModelScope.launch {
            val result = repository.deactivateProduct(id)
            result.onSuccess {
                loadProducts()
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    error = exception.message ?: "Error al desactivar producto"
                )
            }
        }
    }

    fun showDialog() {
        _uiState.value = _uiState.value.copy(showDialog = true, selectedProduct = null)
    }

    fun hideDialog() {
        _uiState.value = _uiState.value.copy(showDialog = false, selectedProduct = null)
    }

    fun selectProduct(product: Product) {
        _uiState.value = _uiState.value.copy(selectedProduct = product, showDialog = true)
    }

    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }
}
