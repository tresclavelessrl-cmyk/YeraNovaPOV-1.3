package com.yeranova.pos.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.yeranova.pos.data.model.Category
import com.yeranova.pos.data.repository.CategoryRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class CategoryUiState(
    val categories: List<Category> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val showDialog: Boolean = false,
    val selectedCategory: Category? = null
)

class CategoryViewModel(private val repository: CategoryRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(CategoryUiState())
    val uiState: StateFlow<CategoryUiState> = _uiState.asStateFlow()

    init {
        loadCategories()
    }

    private fun loadCategories() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.getAllActiveCategories()
            result.onSuccess { categories ->
                _uiState.value = _uiState.value.copy(
                    categories = categories,
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

    fun createCategory(name: String, description: String = "") {
        if (name.isBlank()) {
            _uiState.value = _uiState.value.copy(error = "El nombre de la categoría es obligatorio")
            return
        }

        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.createCategory(name, description)
            result.onSuccess {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    showDialog = false,
                    error = null
                )
                loadCategories()
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error al crear categoría"
                )
            }
        }
    }

    fun updateCategory(category: Category) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val result = repository.updateCategory(category)
            result.onSuccess {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    showDialog = false,
                    error = null
                )
                loadCategories()
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = exception.message ?: "Error al actualizar categoría"
                )
            }
        }
    }

    fun deactivateCategory(id: Long) {
        viewModelScope.launch {
            val result = repository.deactivateCategory(id)
            result.onSuccess {
                loadCategories()
            }.onFailure { exception ->
                _uiState.value = _uiState.value.copy(
                    error = exception.message ?: "Error al desactivar categoría"
                )
            }
        }
    }

    fun showDialog() {
        _uiState.value = _uiState.value.copy(showDialog = true, selectedCategory = null)
    }

    fun hideDialog() {
        _uiState.value = _uiState.value.copy(showDialog = false, selectedCategory = null)
    }

    fun selectCategory(category: Category) {
        _uiState.value = _uiState.value.copy(selectedCategory = category, showDialog = true)
    }

    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }
}
