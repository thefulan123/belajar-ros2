# explore/25-fingerprint — Baca Sidik Jari via ROS2

## Tujuan

Belajar **Publisher sensor biometrik** — mendeteksi sidik jari dan kirim ID ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/sidikjari` |
| Tipe | `std_msgs/Int32` |
| Data | ID sidik jari (1-127) jika cocok, -1 jika tidak dikenali |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "Adafruit Fingerprint Sensor Library" → Install

### 2. Upload ke Arduino
Buka `fingerprint.ino` di Arduino IDE, upload ke board.

### 3. Daftarkan sidik jari
Sebelum dipakai, daftarkan sidik jari dulu via Serial Monitor:
- Buka Serial Monitor (115200 baud)
- Lihat: "Fingerprint sensor ready"
- Tempelkan jari → ID akan muncul di topic /sidikjari

Jika baru pertama kali, **enroll** dulu via contoh sketch "enroll" dari Arduino → File → Examples → Adafruit Fingerprint Sensor Library → enroll

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek data
```bash
ros2 topic echo /sidikjari
# Tempelkan jari yang sudah didaftarkan
# data: 1  → ID sidik jari = 1
```

## Coba Ini

1. **Daftarkan beberapa jari** — ibu jari = ID 1, telunjuk = ID 2, dst
2. **Access control:** Integrasi dengan solenoid (explore/16) — buka kunci jika sidik jari cocok
3. **Absensi:** Simpan ID + timestamp ke file CSV


---

## Modul Terkait

- [Dasar ROS2 Modul 03 — Node](../../Dasar%20ROS2/modul/03-node.md) — konsep node ROS2
- [Dasar ROS2 Modul 04 — Topic](../../Dasar%20ROS2/modul/04-topic-pub-sub.md) — komunikasi pub/sub
- [Dasar ROS2 Modul 10 — Callback & Timer](../../Dasar%20ROS2/modul/10-callback-timer.md) — callback & timer periodik
- [Dasar ROS2 Modul 11 — micro-ROS](../../Dasar%20ROS2/modul/11-micro-ros.md) — ROS2 di Arduino/ESP32
- [KORELASI.md](../../Dasar%20ROS2/docs/KORELASI.md) — mapping lengkap modul ↔ komponen

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

