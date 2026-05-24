# explore/28-rain-sensor — Deteksi Hujan via ROS2

## Tujuan

Belajar **Publisher sensor cuaca** — mendeteksi air/hujan dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (digital) |
| Topic | `/hujan` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = hujan/air terdeteksi, `false` = kering |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `rain_sensor.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /hujan
# data: false → kering
# data: true  → air terdeteksi!
```

## Coba Ini

1. **Teteskan air ke sensor** — data berubah ke true
2. **Keringkan dengan tissue** — kembali false
3. **Integrasi buzzer (explore/03):** Alarm jika hujan
4. **Integrasi relay (explore/04):** Tutup jendela otomatis (dengan motor DC)
