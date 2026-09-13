import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/api/api_exception.dart';
import '../../../../core/storage/secure_storage.dart';
import '../../data/auth_repository.dart';
import '../../domain/user.dart';

/// Auth holati — 4 xil bo'lishi mumkin
sealed class AuthState {
  const AuthState();
}

/// Boshlanish (storage'dan token qidiryapmiz)
class AuthLoading extends AuthState {
  const AuthLoading();
}

/// Login qilingan
class AuthAuthenticated extends AuthState {
  const AuthAuthenticated(this.user);
  final User user;
}

/// Login qilinmagan
class AuthUnauthenticated extends AuthState {
  const AuthUnauthenticated();
}

/// Xato
class AuthError extends AuthState {
  const AuthError(this.exception);
  final ApiException exception;
}

/// AuthNotifier — login, register, logout, me flow'lari.
class AuthNotifier extends AsyncNotifier<AuthState> {
  @override
  Future<AuthState> build() async {
    final storage = ref.read(secureStorageProvider);

    String? token;
    try {
      token = await storage
          .getAccessToken()
          .timeout(const Duration(seconds: 3));
    } catch (_) {
      // iOS Simulator keychain xato bersa yoki timeout — Unauthenticated
      return const AuthUnauthenticated();
    }

    if (token == null) return const AuthUnauthenticated();

    try {
      final repo = ref.read(authRepositoryProvider);
      final user = await repo.me();
      return AuthAuthenticated(user);
    } catch (_) {
      // Token yaroqsiz yoki tarmoq xatosi — login sahifasiga o'tamiz
      try {
        await storage.clear();
      } catch (_) {}
      return const AuthUnauthenticated();
    }
  }

  Future<void> login({required String email, required String password}) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repo = ref.read(authRepositoryProvider);
      final (user, _) = await repo.login(email: email, password: password);
      return AuthAuthenticated(user);
    });
  }

  Future<void> register({
    required String email,
    required String password,
    required String passwordConfirm,
    String? firstName,
    String? lastName,
    String? language,
    String? referralCode,
  }) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final repo = ref.read(authRepositoryProvider);
      final (user, _) = await repo.register(
        email: email,
        password: password,
        passwordConfirm: passwordConfirm,
        firstName: firstName,
        lastName: lastName,
        language: language,
        referralCode: referralCode,
      );
      return AuthAuthenticated(user);
    });
  }

  Future<void> logout() async {
    final repo = ref.read(authRepositoryProvider);
    await repo.logout();
    state = const AsyncValue.data(AuthUnauthenticated());
  }

  Future<void> deleteAccount({required String password}) async {
    final repo = ref.read(authRepositoryProvider);
    await repo.deleteAccount(password: password);
    state = const AsyncValue.data(AuthUnauthenticated());
  }

  Future<void> refresh() async {
    final repo = ref.read(authRepositoryProvider);
    state = await AsyncValue.guard(() async {
      final user = await repo.me();
      return AuthAuthenticated(user);
    });
  }
}

final authProvider = AsyncNotifierProvider<AuthNotifier, AuthState>(
  AuthNotifier.new,
);
