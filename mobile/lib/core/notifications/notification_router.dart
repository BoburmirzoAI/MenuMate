import 'dart:async';

import 'package:go_router/go_router.dart';

import '../router/app_routes.dart';

/// ═════════════════════════════════════════════════════════════════════════
///  NotificationRouter — push payload'ni deep-link'ga aylantiruvchi
/// ═════════════════════════════════════════════════════════════════════════
///
/// Backend `data` payload'ida `kind` maydoni bo'lishi ta'minlanadi:
///   - HOLIDAY   — bayramlar ro'yxatiga
///   - MENU      — menyu ro'yxatiga (menu_id bo'lsa detail'ga)
///   - ALLERGY   — retseptlar ro'yxatiga
///   - GENERAL   — bildirishnomalar ekraniga
///
/// Foydalanuvchi ilova ochilmagan bo'lsa `getInitialMessage`dan, ochilgan bo'lsa
/// `onMessageOpenedApp`dan keladi. Ikkisini FcmService birlashtiradi.
class NotificationRouter {
  NotificationRouter(this._router);

  final GoRouter _router;
  StreamSubscription<Map<String, dynamic>>? _sub;

  void attach(Stream<Map<String, dynamic>> stream) {
    _sub?.cancel();
    _sub = stream.listen(_handle);
  }

  void detach() {
    _sub?.cancel();
    _sub = null;
  }

  void _handle(Map<String, dynamic> payload) {
    final kind = (payload['kind'] as String?)?.toUpperCase();
    switch (kind) {
      case 'HOLIDAY':
        _router.go(AppRoutes.notifications);
        break;
      case 'MENU':
        final menuId = payload['menu_id']?.toString();
        if (menuId != null && menuId.isNotEmpty) {
          _router.go('/menu/$menuId');
        } else {
          _router.go(AppRoutes.menuList);
        }
        break;
      case 'ALLERGY':
        _router.go(AppRoutes.recipes);
        break;
      case 'RECIPE':
        final recipeId = payload['recipe_id']?.toString();
        if (recipeId != null && recipeId.isNotEmpty) {
          _router.go('/recipes/$recipeId');
        }
        break;
      default:
        _router.go(AppRoutes.notifications);
    }
  }
}
