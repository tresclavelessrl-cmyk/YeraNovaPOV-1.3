package com.yeranova.pos

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class YeraNovaPOSApp : Application() {
    override fun onCreate() {
        super.onCreate()
    }
}
