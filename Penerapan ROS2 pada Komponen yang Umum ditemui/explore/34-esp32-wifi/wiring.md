# Wiring: ESP32 WiFi

## Koneksi

| Komponen | ESP32 |
|----------|-------|
| Power | USB / Power bank 5V |
| WiFi | Bawaan ESP32 (tidak perlu kabel tambahan) |

## Catatan

- ESP32 sudah memiliki WiFi + Bluetooth built-in — tidak perlu modul tambahan
- Pastikan ESP32 terhubung ke **jaringan WiFi yang sama** dengan PC tempat ROS2 agent berjalan
- Tidak ada pin khusus yang perlu dihubungkan untuk komunikasi WiFi
- Untuk power mobile, gunakan power bank 5V via kabel USB

## Perbedaan dengan Arduino UNO

| Aspek | Arduino UNO (Serial) | ESP32 (WiFi) |
|-------|---------------------|--------------|
| Transport | Kabel USB | Wireless |
| Jarak | 2-3 meter | ~30 meter (WiFi) |
| Agent | `serial --dev /dev/ttyACM0` | `udp --port 8888` |
| Power | Dari USB | Baterai / Power bank |
| Board support | UNO only | ESP32 only (tidak support UNO) |
