# explore/35-bluetooth — Bridge Bluetooth Serial via ROS2

## Tujuan

Belajar **bridge komunikasi** — menghubungkan HC-05 Bluetooth dengan ROS2.

## Konsep

HC-05 sebagai **bridge serial wireless** — data dari ROS2 dikirim via micro-ROS Agent → Arduino → Bluetooth → perangkat lain (HP/PC).

Atau sebaliknya: data dari HP → Bluetooth → Arduino → publish ke ROS2.

## Cara Jalankan

### 1. Upload ke Arduino
Buka `bluetooth.ino` di Arduino IDE, upload ke board.

### 2. Pair Bluetooth
Di PC/HP: cari "HC-05" (atau "HC-06"), pair dengan PIN 1234.
Catat COM port (Windows) atau /dev/rfcomm0 (Linux).

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /bluetooth
# data: "data dari HP" → terima dari Bluetooth
```

## Coba Ini

1. **Kirim teks dari HP via terminal Bluetooth** — tampil di ROS2
2. **Kontrol LED dari HP:** Kirim "LED_ON" → Arduino parse → publish Bool ke /led
3. **Remote control:** HP sebagai remote robot via Bluetooth


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

