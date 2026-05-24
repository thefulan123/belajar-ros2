# explore/05-dht-sensor — Baca Suhu & Kelembapan via ROS2

## Tujuan

Belajar **Publisher sensor data** — mengirim suhu dan kelembapan ke ROS2 dalam format custom dan Float64.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/suhu` (temperature), `/kelembapan` (humidity) |
| Tipe | `std_msgs/Float64` |
| Frekuensi | 1 Hz |

## Cara Jalankan

### 1. Install library DHT
Di Arduino IDE: Tools → Manage Libraries → Cari "DHT sensor library" by Adafruit → Install

### 2. Upload ke Arduino
Buka `dht_sensor.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /suhu
# data: 28.5

ros2 topic echo /kelembapan
# data: 65.2
```

## Coba Ini

1. **Hembuskan napas ke sensor** — suhu naik, kelembapan naik
2. **Pindahkan ke dekat AC** — suhu turun
3. **Integrasi buzzer** — bunyikan alarm jika suhu > 35°C
4. **Logging data** — buat Python script yang subscribe kedua topic, simpan ke CSV


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

