# explore/02-push-button — Baca Push Button via ROS2

## Tujuan

Belajar **Publisher** di micro-ROS — mengirim status tombol ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/button` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = ditekan, `false` = dilepas |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `push_button.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /button
# data: true  → button ditekan
# data: false → button dilepas
```

## Coba Ini

1. **Integrasi dengan LED** (explore/01): Tekan button nyalakan LED, lepas matikan
2. **Counter:** Ubah code untuk count berapa kali button ditekan, publish sebagai `Int32`
