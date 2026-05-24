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
