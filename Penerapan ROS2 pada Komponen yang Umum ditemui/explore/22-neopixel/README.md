# explore/22-neopixel — Kontrol NeoPixel via ROS2

## Tujuan

Belajar **Subscriber dengan NeoPixel** — mengontrol LED RGB addressable dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/neopixel` |
| Tipe | `std_msgs/String` |
| Data | Format `"LED,R,G,B"` — LED index (0-7), Red (0-255), Green (0-255), Blue (0-255) |

Fitur khusus: kirim `"0,255,0,0"` = LED 0 merah, `"all,0,0,255"` = semua LED biru.

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "Adafruit NeoPixel" → Install

### 2. Upload ke Arduino
Buka `neopixel.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Kirim perintah
```bash
# LED 0 = merah
ros2 topic pub /neopixel std_msgs/msg/String "data: '0,255,0,0'" --once

# LED 1 = hijau
ros2 topic pub /neopixel std_msgs/msg/String "data: '1,0,255,0'" --once

# Semua LED = biru
ros2 topic pub /neopixel std_msgs/msg/String "data: 'all,0,0,255'" --once

# Matikan semua
ros2 topic pub /neopixel std_msgs/msg/String "data: 'all,0,0,0'" --once
```

## Coba Ini

1. **Rainbow:** Kirim warna bergantian tiap 0.1 detik untuk efek pelangi
2. **Integrasi PIR (explore/11):** LED merah jika gerakan, hijau jika aman
3. **Integrasi potensiometer (explore/06):** Putar potensio ganti warna


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

