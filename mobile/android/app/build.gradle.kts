import java.util.Properties
import java.io.FileInputStream

plugins {
    id("com.android.application")
    // Firebase — google-services.json'ni Gradle build'ga bog'laydi.
    id("com.google.gms.google-services")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

/**
 * Release keystore ma'lumotlari `android/key.properties`da saqlanadi.
 * Bu fayl `.gitignore`da — hech qachon git'ga tushmaydi.
 *
 * key.properties fayl formati:
 *   storePassword=...
 *   keyPassword=...
 *   keyAlias=menumate
 *   storeFile=/Users/boburmirzo/menu-mate-release.jks
 */
val keystoreProperties = Properties().apply {
    val keystorePropertiesFile = rootProject.file("key.properties")
    if (keystorePropertiesFile.exists()) {
        load(FileInputStream(keystorePropertiesFile))
    }
}

android {
    namespace = "uz.menumate.menu_mate"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    defaultConfig {
        applicationId = "uz.menumate.menu_mate"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        create("release") {
            val storeFilePath = keystoreProperties["storeFile"] as String?
            if (storeFilePath != null) {
                storeFile = file(storeFilePath)
                storePassword = keystoreProperties["storePassword"] as String
                keyAlias = keystoreProperties["keyAlias"] as String
                keyPassword = keystoreProperties["keyPassword"] as String
            }
        }
    }

    buildTypes {
        release {
            // key.properties mavjud bo'lsa release keystore bilan signing.
            // Aks holda debug keystore (dev qulaylik uchun).
            val hasReleaseKey = keystoreProperties["storeFile"] != null
            signingConfig = if (hasReleaseKey) {
                signingConfigs.getByName("release")
            } else {
                signingConfigs.getByName("debug")
            }
            // Release'da minify o'chirilgan — Flutter release build o'zi
            // Dart code'ni AOT compile qiladi.
            isMinifyEnabled = false
            isShrinkResources = false
        }
    }
}

extensions.configure<com.android.build.api.dsl.ApplicationExtension> {
    compileOptions {
        isCoreLibraryDesugaringEnabled = true
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}

dependencies {
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.5")
}
