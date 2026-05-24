# explore/13-servo — Kontrol Servo via ROS2

## Tujuan

Belajar **Subscriber dengan servo** — mengatur sudut servo dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/servo` |
| Tipe | `std_msgs/Int32` |
| Data | 0 — 180 (derajat) |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `servo.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Servo ke 0°
ros2 topic pub /servo std_msgs/msg/Int32 "data: 0" --once

# Servo ke 90°
ros2 topic pub /servo std_msgs/msg/Int32 "data: 90" --once

# Servo ke 180°
ros2 topic pub /servo std_msgs/msg/Int32 "data: 180" --once

# Gerak perlahan (sweep)
ros2 topic pub /servo std_msgs/msg/Int32 "data: 0" -r 1
```

## Coba Ini

1. **Sweep:** Kirim nilai 0 → 180 bertahap (naikkan 10 tiap 0.5 detik)
2. **Integrasi potensiometer (explore/06):** Putar potensio untuk gerakkan servo
3. **Kontrol via keyboard:** Buat Python node — tekan 'a' = kiri, 'd' = kanan


---

---

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

