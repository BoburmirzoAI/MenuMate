import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/api/api_client.dart';
import '../domain/notification.dart';

class NotificationsRepository {
  NotificationsRepository(this._client);
  final ApiClient _client;

  /// GET /notifications/
  Future<List<AppNotification>> list({bool unreadOnly = false}) async {
    final response = await _client.get(
      '/notifications/',
      queryParameters: unreadOnly ? {'unread': 'true'} : null,
    );
    final data = response['data'];
    final list = data is Map ? (data['results'] as List) : (data as List);
    return list
        .map((e) => AppNotification.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// GET /notifications/holidays/upcoming/?days=30
  Future<List<UpcomingHoliday>> upcomingHolidays({int days = 30}) async {
    final response = await _client.get(
      '/notifications/holidays/upcoming/',
      queryParameters: {'days': days},
    );
    final list = response['data'] as List;
    return list
        .map((e) => UpcomingHoliday.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// PATCH /notifications/{id}/read/
  Future<AppNotification> markRead(int id) async {
    final response = await _client.patch('/notifications/$id/read/');
    return AppNotification.fromJson(response['data'] as Map<String, dynamic>);
  }

  /// POST /notifications/mark-all-read/
  Future<int> markAllRead() async {
    final response = await _client.post('/notifications/mark-all-read/');
    final data = response['data'] as Map<String, dynamic>?;
    return (data?['marked_count'] as int?) ?? 0;
  }
}

final notificationsRepositoryProvider = Provider<NotificationsRepository>((ref) {
  return NotificationsRepository(ref.watch(apiClientProvider));
});

final notificationsListProvider =
    FutureProvider.autoDispose<List<AppNotification>>((ref) async {
  return ref.watch(notificationsRepositoryProvider).list();
});

final upcomingHolidaysProvider =
    FutureProvider.autoDispose<List<UpcomingHoliday>>((ref) async {
  return ref.watch(notificationsRepositoryProvider).upcomingHolidays();
});
