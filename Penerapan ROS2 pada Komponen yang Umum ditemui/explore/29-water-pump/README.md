# explore/29-water-pump — Kontrol Pompa Air via ROS2

## Tujuan

Belajar **Subscriber aktuator daya** — mengontrol pompa air dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/pompa` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = pompa ON, `false` = pompa OFF |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `water_pump.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Pompa ON
ros2 topic pub /pompa std_msgs/msg/Bool "data: true" --once

# Pompa OFF
ros2 topic pub /pompa std_msgs/msg/Bool "data: false" --once
```

## Coba Ini

1. **Integrasi soil moisture (explore/08):** Auto-watering — pompa ON jika tanah kering
2. **Timer:** Pompa ON 10 detik, OFF 30 detik (irigasi otomatis)
3. **Integrasi flow sensor (explore/27):** Pompa OFF jika debit > threshold (bocor)
4. **Integrasi rain sensor (explore/28):** Pompa OFF jika hujan
