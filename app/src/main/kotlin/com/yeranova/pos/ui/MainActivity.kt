package com.yeranova.pos.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Surface
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.yeranova.pos.ui.navigation.Screen
import com.yeranova.pos.ui.screens.LoginScreen
import com.yeranova.pos.ui.screens.DashboardScreen
import com.yeranova.pos.ui.theme.YeraNovaPOSTheme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            YeraNovaPOSApp()
        }
    }
}

@Composable
fun YeraNovaPOSApp() {
    YeraNovaPOSTheme {
        Surface(
            modifier = Modifier,
            color = MaterialTheme.colorScheme.background
        ) {
            val navController = rememberNavController()
            NavHost(
                navController = navController,
                startDestination = Screen.Login.route
            ) {
                composable(Screen.Login.route) {
                    LoginScreen(navController = navController)
                }
                composable(Screen.Dashboard.route) {
                    DashboardScreen(navController = navController)
                }
            }
        }
    }
}
