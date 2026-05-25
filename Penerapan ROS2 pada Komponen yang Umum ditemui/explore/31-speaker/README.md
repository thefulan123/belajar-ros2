# explore/31-speaker — Putar Audio via ROS2 (DFPlayer Mini)

## Tujuan

Belajar **Subscriber audio playback** — memutar file MP3 dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/speaker` |
| Tipe | `std_msgs/Int32` |
| Data | 0 = stop, 1-9999 = nomor track, -1 = next, -2 = previous, -3 = volume up, -4 = volume down |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "DFRobotDFPlayerMini" → Install

### 2. Siapkan microSD
- Format FAT32
- Buat folder `mp3`
- Copy file: `mp3/0001.mp3`, `mp3/0002.mp3`, ...

### 3. Upload ke Arduino
Buka `speaker.ino` di Arduino IDE, upload ke board.

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Kirim perintah
```bash
# Putar track 1
ros2 topic pub /speaker std_msgs/msg/Int32 "data: 1" --once

# Stop
ros2 topic pub /speaker std_msgs/msg/Int32 "data: 0" --once

# Next track
ros2 topic pub /speaker std_msgs/msg/Int32 "data: -1" --once

# Volume naik
ros2 topic pub /speaker std_msgs/msg/Int32 "data: -3" --once

# Volume turun
ros2 topic pub /speaker std_msgs/msg/Int32 "data: -4" --once
```

## Coba Ini

1. **Alarm suara:** Putar track alarm jika PIR (explore/11) deteksi gerakan
2. **Welcome message:** Putar salam jika RFID (explore/24) terdaftar
3. **Parking sensor:** Integrasi ultrasonic (explore/12) dengan suara beep


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

