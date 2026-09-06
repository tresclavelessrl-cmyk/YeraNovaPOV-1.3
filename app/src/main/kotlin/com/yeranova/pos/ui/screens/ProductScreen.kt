package com.yeranova.pos.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.yeranova.pos.data.model.Product
import com.yeranova.pos.ui.viewmodel.ProductViewModel
import java.math.BigDecimal

@Composable
fun ProductScreen(
    navController: NavController,
    viewModel: ProductViewModel,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsState()
    var searchQuery by remember { mutableStateOf("") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Productos") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Atrás")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { viewModel.showDialog() },
                containerColor = MaterialTheme.colorScheme.primary
            ) {
                Icon(Icons.Filled.Add, contentDescription = "Nuevo producto")
            }
        }
    ) { innerPadding ->
        Box(
            modifier = modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                // Search bar
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = {
                        searchQuery = it
                        viewModel.searchProducts(it)
                    },
                    label = { Text("Buscar producto") },
                    leadingIcon = { Icon(Icons.Filled.Search, contentDescription = null) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp),
                    singleLine = true
                )

                when {
                    uiState.isLoading -> {
                        CircularProgressIndicator(
                            modifier = Modifier.align(Alignment.CenterHorizontally)
                        )
                    }
                    uiState.error != null -> {
                        Column(
                            modifier = Modifier
                                .align(Alignment.CenterHorizontally)
                                .padding(16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "Error: ${uiState.error}",
                                color = MaterialTheme.colorScheme.error
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(onClick = { viewModel.clearError() }) {
                                Text("Reintentar")
                            }
                        }
                    }
                    uiState.products.isEmpty() -> {
                        Column(
                            modifier = Modifier
                                .align(Alignment.CenterHorizontally)
                                .padding(16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "No hay productos",
                                style = MaterialTheme.typography.headlineSmall
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Button(onClick = { viewModel.showDialog() }) {
                                Text("Crear primer producto")
                            }
                        }
                    }
                    else -> {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(8.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(uiState.products) { product ->
                                ProductItemCard(product) {
                                    viewModel.selectProduct(product)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if (uiState.showDialog) {
        ProductDialog(
            product = uiState.selectedProduct,
            onDismiss = { viewModel.hideDialog() },
            onSave = { code, name, description, categoryId, price, barcode ->
                if (uiState.selectedProduct != null) {
                    viewModel.updateProduct(
                        uiState.selectedProduct!!.copy(
                            code = code,
                            name = name,
                            description = description,
                            categoryId = categoryId,
                            price = price,
                            barcode = barcode
                        )
                    )
                } else {
                    viewModel.createProduct(code, name, description, categoryId, price, barcode)
                }
            },
            onDelete = { id ->
                viewModel.deactivateProduct(id)
                viewModel.hideDialog()
            }
        )
    }
}

@Composable
fun ProductItemCard(
    product: Product,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .height(100.dp),
        onClick = onClick
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = product.name,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = "Código: ${product.code}",
                    style = MaterialTheme.typography.bodySmall
                )
                Text(
                    text = "Precio: \$${product.price}",
                    style = MaterialTheme.typography.bodySmall,
                    fontWeight = FontWeight.Bold
                )
            }
            if (product.isActive) {
                Icon(
                    Icons.Filled.CheckCircle,
                    contentDescription = "Activo",
                    tint = MaterialTheme.colorScheme.primary
                )
            } else {
                Icon(
                    Icons.Filled.Cancel,
                    contentDescription = "Inactivo",
                    tint = MaterialTheme.colorScheme.error
                )
            }
        }
    }
}

@Composable
fun ProductDialog(
    product: Product?,
    onDismiss: () -> Unit,
    onSave: (String, String, String, Long, BigDecimal, String?) -> Unit,
    onDelete: (Long) -> Unit,
    modifier: Modifier = Modifier
) {
    var code by remember { mutableStateOf(product?.code ?: "") }
    var name by remember { mutableStateOf(product?.name ?: "") }
    var description by remember { mutableStateOf(product?.description ?: "") }
    var categoryId by remember { mutableStateOf(product?.categoryId ?: 1L) }
    var priceStr by remember { mutableStateOf(product?.price?.toString() ?: "") }
    var barcode by remember { mutableStateOf(product?.barcode ?: "") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(if (product == null) "Nuevo Producto" else "Editar Producto")
        },
        text = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = code,
                    onValueChange = { code = it },
                    label = { Text("Código") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Nombre") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = description,
                    onValueChange = { description = it },
                    label = { Text("Descripción") },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(60.dp),
                    maxLines = 2
                )
                OutlinedTextField(
                    value = priceStr,
                    onValueChange = { priceStr = it },
                    label = { Text("Precio") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = barcode,
                    onValueChange = { barcode = it },
                    label = { Text("Código de barras") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val price = priceStr.toBigDecimalOrNull() ?: BigDecimal.ZERO
                    onSave(code, name, description, categoryId, price, barcode.ifBlank { null })
                },
                enabled = code.isNotBlank() && name.isNotBlank() && priceStr.isNotBlank()
            ) {
                Text("Guardar")
            }
        },
        dismissButton = {
            if (product != null) {
                Button(
                    onClick = { onDelete(product.id) },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.error
                    )
                ) {
                    Text("Desactivar")
                }
            }
            TextButton(onClick = onDismiss) {
                Text("Cancelar")
            }
        }
    )
}
