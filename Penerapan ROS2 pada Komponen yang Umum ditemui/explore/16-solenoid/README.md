# explore/16-solenoid — Kontrol Solenoid via ROS2

## Tujuan

Belajar **Subscriber + aktuator** — mengontrol solenoid lock/valve dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/solenoid` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = aktifkan solenoid (door lock ON / valve OPEN) |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `solenoid.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Solenoid ON (door terkunci / valve terbuka)
ros2 topic pub /solenoid std_msgs/msg/Bool "data: true" --once

# Solenoid OFF (door terbuka / valve tertutup)
ros2 topic pub /solenoid std_msgs/msg/Bool "data: false" --once
```

## Coba Ini

1. **Timer:** Kirim `true`, delay 5 detik, kirim `false` (simulasi door lock otomatis)
2. **Integrasi push button (explore/02):** Tekan tombol → unlock selama 3 detik
3. **Integrasi PIR (explore/11):** Deteksi gerakan → unlock door


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

