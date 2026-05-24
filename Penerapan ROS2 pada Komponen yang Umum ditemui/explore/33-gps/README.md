# explore/33-gps — Baca GPS via ROS2

## Tujuan

Belajar **Publisher data lokasi** — membaca koordinat GPS dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (4 topic) |
| Topic | `/gps_lat`, `/gps_lng` (Float64), `/gps_alt` (Float64), `/gps_sats` (Int32) |
| Tipe | `std_msgs/Float64`, `std_msgs/Int32` |
| Data | Latitude, Longitude, Altitude (meter), Satellites |
| Frekuensi | 1 Hz |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "TinyGPSPlus" → Install

### 2. Upload ke Arduino
Buka `gps.ino` di Arduino IDE, upload ke board.

### 3. Bawa ke luar ruangan
GPS tidak akan fix di dalam ruangan — bawa ke tempat dengan view langit.

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek data
```bash
ros2 topic echo /gps_lat
# data: -6.2088  → latitude Jakarta

ros2 topic echo /gps_sats
# data: 8 → 8 satelit terlihat
```

## Coba Ini

1. **Bawa jalan-jalan keluar** — lihat koordinat berubah
2. **Logging route:** Simpan lat/lng ke CSV, visualisasi di Google Maps
3. **Geofencing:** Alarm jika posisi keluar area tertentu
4. **Integrasi buzzer (explore/03):** Beep jika mendekati waypoint


---

## 🔄 ROS2 vs Arduino Biasa

Sensor ini bisa dibaca dengan Arduino biasa via `Serial.print()`. Tapi bedanya:

### Arduino Biasa (Serial Monitor):
```cpp
void loop() {
  int nilai = analogRead(PIN_SENSOR);
  Serial.println(nilai);  // Cuma angka di monitor
  delay(500);
}
```
- Kamu lihat angkanya di Serial Monitor
- Nggak bisa dipake program lain
- Kalau mau kontrol sesuatu, harus tulis semua logic di 1 sketch

### Arduino + micro-ROS (Topic Publisher):
```cpp
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  msg.data = analogRead(PIN_SENSOR);
  rcl_publish(&publisher, &msg, NULL);
}
```
- Data otomatis masuk ke sistem ROS2
- Bisa dibaca node lain (PC, motor, LED, dll)
- Bisa di-log, dianalisis, digabung sensor lain

### Perbandingan Langsung

| Aspek | Arduino + micro-ROS | Arduino Standalone |
|-------|--------------------|--------------------|
| Data sampai ke | Seluruh sistem ROS2 (PC + board lain) | Hanya Serial Monitor |
| Integrasi | 1 baris `rcl_publish()` — langsung nyambung | Tulis ulang kode parsing |
| Expandability | Tinggal tambah subscriber di node lain | Ubah sketch + upload ulang |
| Debug | `ros2 topic echo /topic` | Serial Monitor |
| Cocok | Robot multi-sensor, sistem terdistribusi | Belajar 1 sensor, cek data cepat |

