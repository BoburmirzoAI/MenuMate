import 'package:equatable/equatable.dart';

/// Backend'dagi User modeli (Dart tomondan).
class User extends Equatable {
  const User({
    required this.id,
    required this.email,
    this.phoneNumber,
    this.firstName = '',
    this.lastName = '',
    this.fullName = '',
    this.birthDate,
    this.gender,
    this.avatar,
    this.language = 'uz',
    this.timezone = 'Asia/Tashkent',
    this.isPushEnabled = true,
    this.isEmailVerified = false,
    this.emailVerifiedAt,
    this.isActive = true,
    this.isOnboarded = false,
    this.referralCode,
    this.createdAt,
  });

  final int id;
  final String email;
  final String? phoneNumber;
  final String firstName;
  final String lastName;
  final String fullName;
  final DateTime? birthDate;
  final String? gender;
  final int? avatar;
  final String language;
  final String timezone;
  final bool isPushEnabled;
  final bool isEmailVerified;
  final DateTime? emailVerifiedAt;
  final bool isActive;
  final bool isOnboarded;
  final String? referralCode;
  final DateTime? createdAt;

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      phoneNumber: json['phone_number'] as String?,
      firstName: (json['first_name'] as String?) ?? '',
      lastName: (json['last_name'] as String?) ?? '',
      fullName: (json['full_name'] as String?) ?? '',
      birthDate: json['birth_date'] != null
          ? DateTime.tryParse(json['birth_date'] as String)
          : null,
      gender: json['gender'] as String?,
      avatar: json['avatar'] as int?,
      language: (json['language'] as String?) ?? 'uz',
      timezone: (json['timezone'] as String?) ?? 'Asia/Tashkent',
      isPushEnabled: (json['is_push_enabled'] as bool?) ?? true,
      isEmailVerified: (json['is_email_verified'] as bool?) ?? false,
      emailVerifiedAt: json['email_verified_at'] != null
          ? DateTime.tryParse(json['email_verified_at'] as String)
          : null,
      isActive: (json['is_active'] as bool?) ?? true,
      isOnboarded: (json['is_onboarded'] as bool?) ?? false,
      referralCode: json['referral_code'] as String?,
      createdAt: json['created_at'] != null
          ? DateTime.tryParse(json['created_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'email': email,
        'phone_number': phoneNumber,
        'first_name': firstName,
        'last_name': lastName,
        'birth_date': birthDate?.toIso8601String().split('T').first,
        'gender': gender,
        'language': language,
        'timezone': timezone,
        'is_push_enabled': isPushEnabled,
      };

  @override
  List<Object?> get props => [
        id, email, phoneNumber, firstName, lastName,
        language, isEmailVerified, isOnboarded,
      ];
}

/// JWT tokenlar juftligi.
class AuthTokens extends Equatable {
  const AuthTokens({required this.access, required this.refresh});

  final String access;
  final String refresh;

  factory AuthTokens.fromJson(Map<String, dynamic> json) {
    return AuthTokens(
      access: json['access'] as String,
      refresh: json['refresh'] as String,
    );
  }

  @override
  List<Object?> get props => [access, refresh];
}
