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
