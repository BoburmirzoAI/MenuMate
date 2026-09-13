import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/l10n/language_provider.dart';
import 'core/router/app_router.dart';
import 'core/storage/preferences.dart';
import 'core/theme/app_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Portrait rejim
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // intl locale data (DateFormat uz/ru/en uchun)
  await initializeDateFormatting('uz', null);
  await initializeDateFormatting('ru', null);
  await initializeDateFormatting('en', null);

  // SharedPreferences'ni asinxron olib main'da override qilamiz
  final prefs = await SharedPreferences.getInstance();

  runApp(
    ProviderScope(
      overrides: [
        sharedPreferencesProvider.overrideWithValue(prefs),
      ],
      child: const MenuMateApp(),
    ),
  );
}

class MenuMateApp extends ConsumerWidget {
  const MenuMateApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    // Til o'zgarganda MaterialApp qayta chizilishi uchun watch
    ref.watch(languageProvider);

    return MaterialApp.router(
      title: 'Menu Mate',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: router,
    );
  }
}
