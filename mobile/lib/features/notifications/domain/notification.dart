import 'package:equatable/equatable.dart';

class AppNotification extends Equatable {
  const AppNotification({
    required this.id,
    required this.kind,
    required this.title,
    required this.body,
    required this.isRead,
    required this.createdAt,
    this.imageUrl = '',
    this.sentAt,
  });

  final int id;
  final String kind; // HOLIDAY / ALLERGY / MENU / UPDATE / GENERAL
  final String title;
  final String body;
  final String imageUrl;
  final bool isRead;
  final DateTime createdAt;
  final DateTime? sentAt;

  bool get hasImage => imageUrl.isNotEmpty;

  factory AppNotification.fromJson(Map<String, dynamic> json) => AppNotification(
        id: json['id'] as int,
        kind: (json['kind'] as String?) ?? 'GENERAL',
        title: (json['title'] as String?) ?? '',
        body: (json['body'] as String?) ?? '',
        imageUrl: (json['image_url'] as String?) ?? '',
        isRead: (json['is_read'] as bool?) ?? false,
        createdAt: DateTime.parse(json['created_at'] as String),
        sentAt: json['sent_at'] != null
            ? DateTime.tryParse(json['sent_at'] as String)
            : null,
      );

  AppNotification copyWith({bool? isRead}) => AppNotification(
        id: id,
        kind: kind,
        title: title,
        body: body,
        imageUrl: imageUrl,
        isRead: isRead ?? this.isRead,
        createdAt: createdAt,
        sentAt: sentAt,
      );

  @override
  List<Object?> get props => [id, isRead];
}

class UpcomingHoliday extends Equatable {
  const UpcomingHoliday({
    required this.id,
    required this.name,
    required this.upcomingDate,
    required this.daysUntil,
    this.description = '',
  });

  final int id;
  final String name;
  final DateTime upcomingDate;
  final int daysUntil;
  final String description;

  factory UpcomingHoliday.fromJson(Map<String, dynamic> json) => UpcomingHoliday(
        id: json['id'] as int,
        name: (json['name'] as String?) ?? '',
        upcomingDate: DateTime.parse(json['upcoming_date'] as String),
        daysUntil: (json['days_until'] as int?) ?? 0,
        description: (json['description'] as String?) ?? '',
      );

  @override
  List<Object?> get props => [id, upcomingDate];
}
