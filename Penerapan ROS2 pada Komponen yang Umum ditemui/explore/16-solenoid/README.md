# explore/16-solenoid — Kontrol Solenoid via ROS2

## Tujuan

Belajar **Subscriber + aktuator** — mengontrol solenoid lock/valve dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/solenoid` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = aktifkan solenoid (door lock ON / valve OPEN) |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `solenoid.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Solenoid ON (door terkunci / valve terbuka)
ros2 topic pub /solenoid std_msgs/msg/Bool "data: true" --once

# Solenoid OFF (door terbuka / valve tertutup)
ros2 topic pub /solenoid std_msgs/msg/Bool "data: false" --once
```

## Coba Ini

1. **Timer:** Kirim `true`, delay 5 detik, kirim `false` (simulasi door lock otomatis)
2. **Integrasi push button (explore/02):** Tekan tombol → unlock selama 3 detik
3. **Integrasi PIR (explore/11):** Deteksi gerakan → unlock door
