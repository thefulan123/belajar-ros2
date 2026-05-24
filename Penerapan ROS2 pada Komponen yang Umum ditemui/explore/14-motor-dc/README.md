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
