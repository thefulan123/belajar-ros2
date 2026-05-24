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
