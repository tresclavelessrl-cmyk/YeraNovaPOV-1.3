package com.yeranova.pos.ui.screens

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.yeranova.pos.data.model.InventoryEntry
import com.yeranova.pos.ui.viewmodel.InventoryViewModel
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.math.BigDecimal

@Composable
fun InventoryScreen(
    navController: NavController,
    viewModel: InventoryViewModel,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsState()
    val dateFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy")

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Inventario - ${uiState.date.format(dateFormatter)}") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Filled.ArrowBack, contentDescription = "Atrás")
                    }
                },
                actions = {
                    IconButton(onClick = {
                        viewModel.changeDate(uiState.date.minusDays(1))
                    }) {
                        Icon(Icons.Filled.NavigateBefore, contentDescription = "Día anterior")
                    }
                    IconButton(onClick = {
                        viewModel.changeDate(uiState.date.plusDays(1))
                    }) {
                        Icon(Icons.Filled.NavigateNext, contentDescription = "Día siguiente")
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
                Icon(Icons.Filled.Add, contentDescription = "Nuevo registro")
            }
        }
    ) { innerPadding ->
        Box(
            modifier = modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when {
                uiState.isLoading -> {
                    CircularProgressIndicator(
                        modifier = Modifier.align(Alignment.Center)
                    )
                }
                uiState.error != null -> {
                    Column(
                        modifier = Modifier
                            .align(Alignment.Center)
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
                uiState.entries.isEmpty() -> {
                    Column(
                        modifier = Modifier
                            .align(Alignment.Center)
                            .padding(16.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "No hay registros de inventario",
                            style = MaterialTheme.typography.headlineSmall
                        )
                        Text(
                            text = "para ${uiState.date.format(dateFormatter)}",
                            style = MaterialTheme.typography.bodyMedium
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(onClick = { viewModel.showDialog() }) {
                            Text("Crear registro")
                        }
                    }
                }
                else -> {
                    Column(modifier = Modifier.fillMaxSize()) {
                        // Inventory table
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState())
                        ) {
                            Column {
                                // Header row
                                InventoryTableHeader()

                                // Data rows
                                LazyColumn(
                                    modifier = Modifier.fillMaxWidth(),
                                    verticalArrangement = Arrangement.spacedBy(4.dp)
                                ) {
                                    items(uiState.entries) { entry ->
                                        InventoryTableRow(entry) {
                                            viewModel.selectEntry(entry)
                                        }
                                    }
                                }
                            }
                        }

                        // Total footer
                        InventoryTotalFooter(uiState.dailyTotal)
                    }
                }
            }
        }
    }

    if (uiState.showDialog) {
        InventoryDialog(
            entry = uiState.selectedEntry,
            products = uiState.products,
            onDismiss = { viewModel.hideDialog() },
            onSave = { productId, initialStock, incomingStock, finalStock, price ->
                viewModel.createInventoryEntry(productId, initialStock, incomingStock, finalStock, price)
            },
            onUpdate = { entry ->
                viewModel.updateInventoryEntry(entry)
            }
        )
    }
}

@Composable
fun InventoryTableHeader(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.primary)
            .padding(4.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        listOf("PRODUCTO", "INICIO", "ENTRADA", "VENTA", "FINAL", "VENDIDO", "PRECIO", "IMPORTE")
            .forEach { header ->
                Text(
                    text = header,
                    modifier = Modifier
                        .width(100.dp)
                        .padding(4.dp),
                    color = MaterialTheme.colorScheme.onPrimary,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center
                )
            }
    }
}

@Composable
fun InventoryTableRow(
    entry: InventoryEntry,
    onClickEdit: () -> Unit,
    modifier: Modifier = Modifier
) {
    val saleQuantity = entry.initialStock + entry.incomingStock
    val soldQuantity = saleQuantity - entry.finalStock
    val amount = soldQuantity * entry.price

    Row(
        modifier = modifier
            .fillMaxWidth()
            .background(MaterialTheme.colorScheme.surfaceVariant)
            .padding(4.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        // Product name placeholder
        Text(
            text = "Prod ${entry.productId}",
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center
        )
        // INICIO
        Text(
            text = entry.initialStock.toString(),
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center
        )
        // ENTRADA
        Text(
            text = entry.incomingStock.toString(),
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center
        )
        // VENTA
        Text(
            text = saleQuantity.toString(),
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center,
            fontWeight = FontWeight.Bold
        )
        // FINAL
        Text(
            text = entry.finalStock.toString(),
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center
        )
        // VENDIDO
        Text(
            text = soldQuantity.toString(),
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center,
            fontWeight = FontWeight.Bold
        )
        // PRECIO
        Text(
            text = "\$${entry.price}",
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center
        )
        // IMPORTE
        Text(
            text = "\$${amount}",
            modifier = Modifier.width(100.dp).padding(4.dp),
            fontSize = 11.sp,
            textAlign = TextAlign.Center,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
    }
}

@Composable
fun InventoryTotalFooter(
    total: BigDecimal,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "TOTAL DEL DÍA",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = "\$${total}",
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary
            )
        }
    }
}

@Composable
fun InventoryDialog(
    entry: InventoryEntry?,
    products: List<Any>,
    onDismiss: () -> Unit,
    onSave: (Long, BigDecimal, BigDecimal, BigDecimal, BigDecimal) -> Unit,
    onUpdate: (InventoryEntry) -> Unit,
    modifier: Modifier = Modifier
) {
    var productId by remember { mutableStateOf(entry?.productId ?: 1L) }
    var initialStock by remember { mutableStateOf(entry?.initialStock?.toString() ?: "") }
    var incomingStock by remember { mutableStateOf(entry?.incomingStock?.toString() ?: "") }
    var finalStock by remember { mutableStateOf(entry?.finalStock?.toString() ?: "") }
    var price by remember { mutableStateOf(entry?.price?.toString() ?: "") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(if (entry == null) "Nuevo Registro" else "Editar Registro")
        },
        text = {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = initialStock,
                    onValueChange = { initialStock = it },
                    label = { Text("Stock Inicial") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = incomingStock,
                    onValueChange = { incomingStock = it },
                    label = { Text("Stock Entrada") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = finalStock,
                    onValueChange = { finalStock = it },
                    label = { Text("Stock Final") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = price,
                    onValueChange = { price = it },
                    label = { Text("Precio") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    val init = initialStock.toBigDecimalOrNull() ?: BigDecimal.ZERO
                    val incoming = incomingStock.toBigDecimalOrNull() ?: BigDecimal.ZERO
                    val final = finalStock.toBigDecimalOrNull() ?: BigDecimal.ZERO
                    val priceVal = price.toBigDecimalOrNull() ?: BigDecimal.ZERO
                    onSave(productId, init, incoming, final, priceVal)
                },
                enabled = initialStock.isNotBlank() && finalStock.isNotBlank() && price.isNotBlank()
            ) {
                Text("Guardar")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancelar")
            }
        }
    )
}
