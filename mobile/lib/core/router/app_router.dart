import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/providers/auth_state.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/screens/password/forgot_password_screen.dart';
import '../../features/auth/presentation/screens/password/reset_password_screen.dart';
import '../../features/auth/presentation/screens/register_screen.dart';
import '../../features/family/presentation/screens/family_create_screen.dart';
import '../../features/family/data/family_repository.dart';
import '../../features/family/presentation/screens/member_add_screen.dart';
import '../../features/family/presentation/screens/member_list_screen.dart';
import '../../features/notifications/presentation/screens/notification_detail_screen.dart';
import '../../features/notifications/presentation/screens/notifications_screen.dart';
import '../../features/menu/presentation/screens/dashboard_screen.dart';
import '../../features/menu/presentation/screens/day_detail_screen.dart';
import '../../features/menu/presentation/screens/menu_list_screen.dart';
import '../../features/onboarding/presentation/screens/language_screen.dart';
import '../../features/onboarding/presentation/screens/onboarding_screen.dart';
import '../../features/onboarding/presentation/screens/splash_screen.dart';
import '../../features/products/presentation/screens/shopping_screen.dart';
import '../../features/profile/presentation/screens/profile_screen.dart';
import '../../features/recipes/presentation/screens/recipe_detail_screen.dart';
import '../../features/recipes/presentation/screens/recipes_list_screen.dart';
import '../../features/settings/presentation/screens/settings_screen.dart';
import 'app_routes.dart';
import 'main_shell.dart';

final _shellNavigatorKey = GlobalKey<NavigatorState>();
final _rootNavigatorKey = GlobalKey<NavigatorState>();

/// go_router uchun refresh trigger — auth o'zgarganida router qayta baholaydi.
class _AuthRefreshNotifier extends ChangeNotifier {
  _AuthRefreshNotifier(this._ref) {
    // authProvider'ni tinglaymiz, o'zgarganda notifyListeners()
    _subscription = _ref.listen<AsyncValue<AuthState>>(
      authProvider,
      (previous, next) => notifyListeners(),
      fireImmediately: false,
    );
  }

  final Ref _ref;
  late final ProviderSubscription<AsyncValue<AuthState>> _subscription;

  @override
  void dispose() {
    _subscription.close();
    super.dispose();
  }
}

final routerProvider = Provider<GoRouter>((ref) {
  final refreshNotifier = _AuthRefreshNotifier(ref);
  ref.onDispose(refreshNotifier.dispose);

  return GoRouter(
    navigatorKey: _rootNavigatorKey,
    initialLocation: AppRoutes.splash,
    debugLogDiagnostics: true,
    refreshListenable: refreshNotifier,
    redirect: (context, state) {
      final loc = state.matchedLocation;
      final auth = ref.read(authProvider);

      final publicRoutes = {
        AppRoutes.splash,
        AppRoutes.onboarding,
        AppRoutes.languageSelect,
        AppRoutes.login,
        AppRoutes.register,
        AppRoutes.forgotPassword,
        AppRoutes.resetPassword,
      };

      // Auth xato bergan bo'lsa — login sahifasiga
      if (auth.hasError) {
        return publicRoutes.contains(loc) ? null : AppRoutes.login;
      }

      // Auth hali yuklanyapti — splash'da qoldiramiz
      if (auth.isLoading || !auth.hasValue) {
        return loc == AppRoutes.splash ? null : AppRoutes.splash;
      }

      final authState = auth.value!;

      switch (authState) {
        case AuthLoading():
          return loc == AppRoutes.splash ? null : AppRoutes.splash;

        case AuthUnauthenticated():
          // Splash'da qolib ketmasin — login'ga o'tsin
          if (loc == AppRoutes.splash) return AppRoutes.login;
          return publicRoutes.contains(loc) ? null : AppRoutes.login;

        case AuthAuthenticated(:final user):
          // Login qilingan, splash yoki auth ekranida bo'lsa → home
          if (loc == AppRoutes.splash ||
              loc == AppRoutes.login ||
              loc == AppRoutes.register ||
              loc == AppRoutes.onboarding ||
              loc == AppRoutes.languageSelect) {
            return user.isOnboarded ? AppRoutes.home : AppRoutes.familyCreate;
          }
          // Onboarding tugamagan bo'lsa faqat family flow'da qolsin
          if (!user.isOnboarded && !loc.startsWith('/family')) {
            return AppRoutes.familyCreate;
          }
          return null;

        case AuthError():
          if (loc == AppRoutes.splash) return AppRoutes.login;
          return publicRoutes.contains(loc) ? null : AppRoutes.login;
      }
    },
    routes: [
      GoRoute(path: AppRoutes.splash, builder: (c, s) => const SplashScreen()),

      // Auth
      GoRoute(path: AppRoutes.onboarding, builder: (c, s) => const OnboardingScreen()),
      GoRoute(path: AppRoutes.languageSelect, builder: (c, s) => const LanguageScreen()),
      GoRoute(path: AppRoutes.login, builder: (c, s) => const LoginScreen()),
      GoRoute(path: AppRoutes.register, builder: (c, s) => const RegisterScreen()),
      GoRoute(
        path: AppRoutes.forgotPassword,
        builder: (c, s) => const ForgotPasswordScreen(),
      ),
      GoRoute(
        path: AppRoutes.resetPassword,
        builder: (c, s) => ResetPasswordScreen(prefilledEmail: s.extra as String?),
      ),

      // Onboarding (post-register)
      GoRoute(path: AppRoutes.familyCreate, builder: (c, s) => const FamilyCreateScreen()),
      GoRoute(path: AppRoutes.memberAdd, builder: (c, s) => const MemberAddScreen()),
      GoRoute(path: AppRoutes.memberList, builder: (c, s) => const MemberListScreen()),
      GoRoute(
        path: '/family/members/:id/edit',
        builder: (c, s) => _MemberEditLoader(id: int.parse(s.pathParameters['id']!)),
      ),

      // Main shell (bottom nav)
      ShellRoute(
        navigatorKey: _shellNavigatorKey,
        builder: (context, state, child) => MainShell(
          currentIndex: MainShell.indexForLocation(state.matchedLocation),
          child: child,
        ),
        routes: [
          GoRoute(path: AppRoutes.home, builder: (c, s) => const DashboardScreen()),
          GoRoute(path: AppRoutes.menuList, builder: (c, s) => const MenuListScreen()),
          GoRoute(path: AppRoutes.shopping, builder: (c, s) => const ShoppingScreen()),
          GoRoute(
            path: AppRoutes.recipes,
            builder: (c, s) => const RecipesListScreen(),
          ),
          GoRoute(
            path: '/menu/:id/day/:dayId',
            builder: (c, s) => DayDetailScreen(
              menuId: int.parse(s.pathParameters['id']!),
              dayId: int.parse(s.pathParameters['dayId']!),
            ),
          ),
        ],
      ),

      // Profil ekrani — bottom nav'siz, dashboard avataridan kiriladi
      GoRoute(
        path: AppRoutes.profile,
        builder: (c, s) => const ProfileScreen(),
      ),

      // Detail routes (root — bottom nav'siz)
      GoRoute(
        path: '/menu/:id/day/:dayId',
        builder: (c, s) => DayDetailScreen(
          menuId: int.parse(s.pathParameters['id']!),
          dayId: int.parse(s.pathParameters['dayId']!),
        ),
      ),
      GoRoute(
        path: '/recipes/:id',
        builder: (c, s) => RecipeDetailScreen(
          recipeId: int.parse(s.pathParameters['id']!),
        ),
      ),
      GoRoute(
        path: AppRoutes.settings,
        builder: (c, s) => const SettingsScreen(),
      ),
      GoRoute(
        path: AppRoutes.notifications,
        builder: (c, s) => const NotificationsScreen(),
      ),
      GoRoute(
        path: '/notifications/:id',
        builder: (c, s) => NotificationDetailScreen(
          id: int.parse(s.pathParameters['id']!),
        ),
      ),
    ],
  );
});

/// A'zoni ID bo'yicha topib, tahrirlash formasini ochadi.
class _MemberEditLoader extends ConsumerWidget {
  const _MemberEditLoader({required this.id});
  final int id;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final async = ref.watch(familyMembersProvider);
    return async.when(
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (err, _) => Scaffold(body: Center(child: Text('$err'))),
      data: (members) {
        final m = members.where((it) => it.id == id).firstOrNull;
        if (m == null) {
          return const Scaffold(body: Center(child: Text('A\'zo topilmadi')));
        }
        return MemberAddScreen(editing: m);
      },
    );
  }
}
