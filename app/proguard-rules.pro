# This is a configuration file for R8, the new code shrinker from Google.
# See https://developer.android.com/studio/build/shrink-code for more details.

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# -keepclassmembers class fqcn.of.javascript.interface.for.webview {
#    public *;
# }

# Preserve line numbers for debugging stack traces
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-keepclassmembers class * extends androidx.room.RoomDatabase {
    public *;
}

# Hilt
-keep class dagger.hilt.** { *; }
-keep class * implements dagger.hilt.internal.RootComponentHolder

# Kotlin
-keepclassmembers class kotlin.Metadata {
    public <methods>;
}

# BCrypt (password hashing)
-keep class org.mindrot.** { *; }
