import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:logger/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/l10n/language_provider.dart';
import 'core/notifications/fcm_service.dart';
import 'core/notifications/notification_router.dart';
import 'core/router/app_router.dart';
import 'core/storage/preferences.dart';
import 'core/theme/app_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();


  // Firebase background handler — top-level bo'lishi shart (isolate cheklovi).
  FirebaseMessaging.onBackgroundMessage(firebaseBackgroundHandler);

  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // intl locale data
  await initializeDateFormatting('uz', null);
  await initializeDateFormatting('ru', null);
  await initializeDateFormatting('en', null);

  final prefs = await SharedPreferences.getInstance();

  // FCM'ni tayyorlaymiz. Xato bo'lsa ilova baribir ochilaveradi
  // (Firebase konfigi yo'q bo'lsa ham).
  final fcmService = FcmService(Logger());
  await fcmService.initialize();

  runApp(
    ProviderScope(
      overrides: [
        sharedPreferencesProvider.overrideWithValue(prefs),
        fcmServiceProvider.overrideWithValue(fcmService),
      ],
      child: const MenuMateApp(),
    ),
  );
}

class MenuMateApp extends ConsumerStatefulWidget {
  const MenuMateApp({super.key});

  @override
  ConsumerState<MenuMateApp> createState() => _MenuMateAppState();
}

class _MenuMateAppState extends ConsumerState<MenuMateApp> {
  @override
  void initState() {
    super.initState();
    // Notification tap bo'lganda deep-link amalga oshiruvchi.
    // Router yaratilgach uni ulash uchun `addPostFrameCallback` ishlatamiz.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final router = ref.read(routerProvider);
      final fcm = ref.read(fcmServiceProvider);
      NotificationRouter(router).attach(fcm.onNotificationTap);
    });
  }

  @override
  Widget build(BuildContext context) {
    final router = ref.watch(routerProvider);
    ref.watch(languageProvider);

    return MaterialApp.router(
      title: 'Menu-Mate',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: router,
    );
  }
}

