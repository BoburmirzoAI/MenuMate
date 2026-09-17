export interface MockDevice {
  id: number;
  user_email: string;
  device_type: 'ANDROID' | 'IOS' | 'WEB';
  device_id: string;
  app_version: string;
  fcm_token_set: boolean;
  last_active: string;
}

export const mockDevices: MockDevice[] = [
  { id: 1, user_email: 'boburmirzo@menumate.uz', device_type: 'IOS', device_id: 'ABC-123-XYZ', app_version: '1.0.0', fcm_token_set: true, last_active: '2026-09-14T02:15:00Z' },
  { id: 2, user_email: 'aziza.karimova@gmail.com', device_type: 'ANDROID', device_id: 'DEF-456-UVW', app_version: '1.0.0', fcm_token_set: true, last_active: '2026-09-13T22:30:00Z' },
  { id: 3, user_email: 'jasur.tashkentli@mail.ru', device_type: 'ANDROID', device_id: 'GHI-789-RST', app_version: '0.9.5', fcm_token_set: false, last_active: '2026-09-12T18:00:00Z' },
  { id: 4, user_email: 'nigora.yusupova@yandex.uz', device_type: 'IOS', device_id: 'JKL-012-OPQ', app_version: '1.0.0', fcm_token_set: true, last_active: '2026-09-11T10:45:00Z' },
  { id: 5, user_email: 'sardor.rakhmatov@gmail.com', device_type: 'WEB', device_id: 'MNO-345-LKI', app_version: '1.0.0', fcm_token_set: false, last_active: '2026-09-14T01:00:00Z' },
];
