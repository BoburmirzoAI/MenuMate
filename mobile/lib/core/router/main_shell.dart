import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../l10n/language_provider.dart';
import '../theme/app_colors.dart';
import 'app_routes.dart';

/// Bottom nav — iOS 18 "Liquid Glass" uslubida floating oval, 4 tab.
class MainShell extends ConsumerWidget {
  const MainShell({super.key, required this.child, required this.currentIndex});

  final Widget child;
  final int currentIndex;

  static const _tabs = [
    (icon: Icons.home_rounded, labelKey: 'nav_home', route: AppRoutes.home),
    (icon: Icons.calendar_month, labelKey: 'nav_menu', route: AppRoutes.menuList),
    (icon: Icons.menu_book, labelKey: 'nav_recipes', route: AppRoutes.recipes),
    (icon: Icons.shopping_cart_outlined, labelKey: 'nav_shopping', route: AppRoutes.shopping),
  ];

  static int indexForLocation(String location) {
    if (location.startsWith(AppRoutes.menuList)) return 1;
    if (location.startsWith(AppRoutes.recipes)) return 2;
    if (location.startsWith(AppRoutes.shopping)) return 3;
    return 0;
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      extendBody: true,
      body: child,
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.fromLTRB(20, 0, 20, 12),
        child: SafeArea(
          top: false,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(32),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
              child: Container(
                height: 66,
                decoration: BoxDecoration(
                  color: AppColors.creamCard.withValues(alpha: 0.82),
                  borderRadius: BorderRadius.circular(32),
                  border: Border.all(
                    color: AppColors.creamAccent.withValues(alpha: 0.6),
                    width: 0.5,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.textDark.withValues(alpha: 0.08),
                      blurRadius: 20,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Row(
                  children: List.generate(_tabs.length, (i) {
                    final tab = _tabs[i];
                    final active = i == currentIndex;
                    return Expanded(
                      child: InkWell(
                        onTap: () => context.go(tab.route),
                        borderRadius: BorderRadius.circular(24),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              tab.icon,
                              size: 24,
                              color: active ? AppColors.terracotta : AppColors.textLight,
                            ),
                            const SizedBox(height: 3),
                            Text(
                              ref.tr(tab.labelKey),
                              style: TextStyle(
                                fontSize: 11,
                                fontWeight: active ? FontWeight.w700 : FontWeight.w500,
                                color: active ? AppColors.terracotta : AppColors.textLight,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
