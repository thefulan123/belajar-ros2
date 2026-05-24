# explore/10-flame-sensor — Deteksi Api via ROS2

## Tujuan

Belajar **Publisher sensor digital** — mendeteksi api (nyala) dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/api` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = api terdeteksi, `false` = aman |
| Frekuensi | 20 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `flame_sensor.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /api
# data: false → tidak ada api
# data: true  → api terdeteksi
```

## Coba Ini

1. **Dekatkan korek api (dinyalakan) dari jarak 20-30 cm** — sensor mendeteksi
2. **Integrasi buzzer (explore/03):** Alarm kebakaran
3. **Integrasi relay (explore/04):** Nyalakan pompa air pemadam
