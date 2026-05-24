# explore/21-oled — Tampilkan Data di OLED via ROS2

## Tujuan

Belajar **Subscriber dengan OLED** — menampilkan data ROS2 di layar OLED.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/oled` |
| Tipe | `std_msgs/String` |
| Data | Teks (maks 4 baris, 21 karakter per baris) |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "Adafruit SSD1306" → Install
Cari "Adafruit GFX" → Install

### 2. Upload ke Arduino
Buka `oled.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Kirim teks
```bash
# Tampilkan teks
ros2 topic pub /oled std_msgs/msg/String "data: 'Hello OLED!'" --once

# Multi baris pakai \n
ros2 topic pub /oled std_msgs/msg/String "data: 'Suhu: 28C\nKelemb: 65%\nStatus: OK\nTime: 12:00'" --once
```

## Coba Ini

1. **Dashboard:** Tampilkan suhu + kelembapan + status sistem
2. **Animasi:** Kirim teks bergantian untuk efek scroll
3. **Grafik:** Modifikasi code untuk tampilkan bar chart dari data sensor
