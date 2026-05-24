# explore/15-stepper — Kontrol Stepper Motor via ROS2

## Tujuan

Belajar **Subscriber dengan stepper** — mengontrol posisi motor stepper dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/stepper` |
| Tipe | `std_msgs/Int32` |
| Data | Jumlah step (+ = CW, - = CCW, 0 = stop) |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `stepper.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Putar 512 step CW (searah jarum jam)
ros2 topic pub /stepper std_msgs/msg/Int32 "data: 512" --once

# Putar 512 step CCW
ros2 topic pub /stepper std_msgs/msg/Int32 "data: -512" --once

# Putar penuh 1 revolusi (2048 step)
ros2 topic pub /stepper std_msgs/msg/Int32 "data: 2048" --once
```

## Coba Ini

1. **Kalibrasi:** Kirim 2048 step, ukur apakah tepat 1 putaran
2. **Kecepatan:** Ganti delay di loop stepper untuk kecepatan berbeda
3. **Integrasi push button (explore/02):** 1 step per klik tombol
