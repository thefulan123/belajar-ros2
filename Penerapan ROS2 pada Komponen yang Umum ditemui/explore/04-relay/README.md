# explore/04-relay — Kontrol Relay via ROS2

## Tujuan

Belajar **Subscriber** — mengendalikan perangkat listrik (AC/motor) via relay.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/relay` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = relay ON, `false` = relay OFF |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `relay.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Relay nyala
ros2 topic pub /relay std_msgs/msg/Bool "data: true" --once

# Relay mati
ros2 topic pub /relay std_msgs/msg/Bool "data: false" --once

# Toggle terus (1 Hz)
ros2 topic pub /relay std_msgs/msg/Bool "data: true" -r 1
```

## Coba Ini

1. **Otomatis:** Hubungkan relay ke pompa atau lampu, kontrol dari keyboard
2. **Timer:** Buat script Python publish `true` → delay 5 detik → publish `false`
3. **Safety:** Integrasi dengan push button — relay hanya ON jika button ditekan
