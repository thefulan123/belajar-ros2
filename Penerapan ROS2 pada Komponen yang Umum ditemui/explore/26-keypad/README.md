# explore/26-keypad — Baca Keypad 4x4 via ROS2

## Tujuan

Belajar **Publisher input matrix** — membaca tombol keypad dan kirim karakter ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/keypad` |
| Tipe | `std_msgs/String` |
| Data | Karakter tombol yang ditekan ("1", "A", "*", dll) |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "Keypad" by Mark Stanley → Install

### 2. Upload ke Arduino
Buka `keypad.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /keypad
# Tekan tombol pada keypad
# data: "1"
# data: "5"
# data: "#"
```

## Coba Ini

1. **Password entry:** Buat Python node — subscribe /keypad, jika kode benar ("1234#") → unlock
2. **Kalkulator:** Baca angka + operator via keypad, tampilkan hasil di LCD (explore/20)
3. **Integrasi solenoid (explore/16):** Buka kunci jika password benar
4. **Kombinasi RFID (explore/24):** Kartu + PIN untuk akses ganda


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

