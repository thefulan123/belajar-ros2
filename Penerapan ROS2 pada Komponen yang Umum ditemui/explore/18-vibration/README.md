# explore/18-vibration — Kontrol Vibration Motor via ROS2

## Tujuan

Belajar **Subscriber PWM** — mengontrol intensitas getaran motor dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/vibrasi` |
| Tipe | `std_msgs/Int32` |
| Data | 0 (mati) — 100 (getaran maksimal) |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `vibration.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Getaran 50%
ros2 topic pub /vibrasi std_msgs/msg/Int32 "data: 50" --once

# Getaran maksimal
ros2 topic pub /vibrasi std_msgs/msg/Int32 "data: 100" --once

# Mati
ros2 topic pub /vibrasi std_msgs/msg/Int32 "data: 0" --once
```

## Coba Ini

1. **Getaran naik-turun:** Kirim 0 → 25 → 50 → 75 → 100 → 75 → ...
2. **Integrasi PIR (explore/11):** Getar saat ada gerakan (notifikasi)
3. **Integrasi ultrasonic (explore/12):** Getar makin kuat makin dekat jarak
4. **Haptic feedback:** Getar 100ms saat push button ditekan
