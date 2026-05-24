# explore/07-ldr — Baca Intensitas Cahaya via ROS2

## Tujuan

Belajar **Publisher sensor analog** — membaca LDR dan mengirim intensitas cahaya ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/cahaya` |
| Tipe | `std_msgs/Int32` |
| Data | 0 (gelap) — 100 (terang) |
| Frekuensi | 10 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `ldr.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /cahaya
# data: 80  → terang
# data: 10  → gelap
```

## Coba Ini

1. **Tutup LDR dengan tangan** — nilai turun drastis
2. **Sorot senter ke LDR** — nilai naik
3. **Integrasi LED (explore/01):** Buat lampu otomatis — nyala saat gelap (< 30), mati saat terang


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

