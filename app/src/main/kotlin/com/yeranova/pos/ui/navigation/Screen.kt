package com.yeranova.pos.ui.navigation

seal class Screen(val route: String) {
    object Login : Screen("login")
    object Dashboard : Screen("dashboard")
    object Inventory : Screen("inventory")
    object Sales : Screen("sales")
    object Products : Screen("products")
    object Cash : Screen("cash")
    object Reports : Screen("reports")
    object Settings : Screen("settings")
}
