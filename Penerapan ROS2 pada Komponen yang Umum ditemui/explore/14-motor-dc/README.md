# explore/14-motor-dc — Kontrol Motor DC via ROS2

## Tujuan

Belajar **Subscriber + PWM** — mengontrol kecepatan dan arah motor DC.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber (2 topic) |
| Topic | `/motor_kecepatan` (Int32), `/motor_arah` (Bool) |
| Tipe | `std_msgs/Int32`, `std_msgs/Bool` |

Data kecepatan: 0 (stop) — 100 (full speed)
Data arah: `true` = maju, `false` = mundur

## Cara Jalankan

### 1. Upload ke Arduino
Buka `motor_dc.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Motor maju kecepatan 75%
ros2 topic pub /motor_kecepatan std_msgs/msg/Int32 "data: 75" --once
ros2 topic pub /motor_arah std_msgs/msg/Bool "data: true" --once

# Motor mundur kecepatan 50%
ros2 topic pub /motor_kecepatan std_msgs/msg/Int32 "data: 50" --once
ros2 topic pub /motor_arah std_msgs/msg/Bool "data: false" --once

# Stop
ros2 topic pub /motor_kecepatan std_msgs/msg/Int32 "data: 0" --once
```

## Coba Ini

1. **Acceleration ramping:** Naikkan kecepatan perlahan 0 → 100
2. **Integrasi potensiometer (explore/06):** Kecepatan = nilai potensio
3. **Integrasi push button (explore/02):** Button 1 = maju, Button 2 = mundur


---

## Modul Terkait

- [Dasar ROS2 Modul 03 — Node](../../Dasar%20ROS2/modul/03-node.md) — konsep node ROS2
- [Dasar ROS2 Modul 04 — Topic](../../Dasar%20ROS2/modul/04-topic-pub-sub.md) — komunikasi pub/sub
- [Dasar ROS2 Modul 10 — Callback & Timer](../../Dasar%20ROS2/modul/10-callback-timer.md) — callback & timer periodik
- [Dasar ROS2 Modul 11 — micro-ROS](../../Dasar%20ROS2/modul/11-micro-ros.md) — ROS2 di Arduino/ESP32
- [KORELASI.md](../../Dasar%20ROS2/docs/KORELASI.md) — mapping lengkap modul ↔ komponen

## 🔄 ROS2 vs Arduino Biasa

Komponen ini bisa dikontrol dengan Arduino biasa via `digitalWrite()` / `analogWrite()`. Tapi bedanya:

### Arduino Biasa (langsung di sketch):
```cpp
void loop() {
  digitalWrite(PIN, HIGH);
  delay(1000);
  digitalWrite(PIN, LOW);
  delay(1000);
}
```
- Polanya KERAS — harus ditentukan di kode
- Mau rubah? Edit kode, upload ulang
- Nggak bisa dikontrol dari luar (PC, sensor lain)

### Arduino + micro-ROS (Topic Subscriber):
```cpp
void subscription_callback(const void *msgin) {
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;
  digitalWrite(PIN, msg->data);
}
```
- Dikontrol dari MANA SAJA via topic ROS2
- Bisa dari CLI: `ros2 topic pub /topic ...`
- Bisa dari sensor lain: button, suhu, timer
- Tanpa upload ulang!

### Perbandingan Langsung

| Aspek | Arduino + micro-ROS | Arduino Standalone |
|-------|--------------------|--------------------|
| Kontrol dari | PC, sensor lain, timer, CLI | Cuma dari kode yang sudah di-upload |
| Ubah perilaku | `ros2 topic pub` — langsung tanpa upload | Edit sketch → compile → upload |
| Integrasi | Langsung nyambung ke publisher mana pun | Manual — semua kode di 1 sketch |
| Cocok | Robot butuh kontrol dinamis dari banyak sumber | Projekt fixed-function (blink, timer) |

