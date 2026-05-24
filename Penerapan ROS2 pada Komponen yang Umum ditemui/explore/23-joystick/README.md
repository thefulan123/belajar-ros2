# explore/23-joystick — Baca Joystick via ROS2

## Tujuan

Belajar **Publisher multi-axis** — membaca posisi joystick (X, Y, button) dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (3 topic) |
| Topic | `/joystick_x`, `/joystick_y` (Int32), `/joystick_button` (Bool) |
| Tipe | `std_msgs/Int32`, `std_msgs/Bool` |
| Data | X/Y: -100 (kiri/bawah) s/d 100 (kanan/atas), tengah=0 |
| Frekuensi | 20 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `joystick.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /joystick_x
# data: 0   → posisi tengah
# data: 100 → joystick ke kanan
# data: -100 → joystick ke kiri

ros2 topic echo /joystick_button
# data: false → tidak ditekan
# data: true  → ditekan
```

## Coba Ini

1. **Kontrol servo (explore/13):** Joystick X → servo, Y → LED brightness
2. **Kontrol motor DC (explore/14):** X = arah, Y = kecepatan
3. **RC controller simulator:** Joystick sebagai remote control robot
