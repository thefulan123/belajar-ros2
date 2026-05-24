# explore/01-led — Kontrol LED via ROS2

## Tujuan

Belajar **Subscriber** di micro-ROS — LED menyala/mati berdasarkan perintah dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/led` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = LED nyala, `false` = LED mati |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `led.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Nyalakan LED
ros2 topic pub /led std_msgs/msg/Bool "data: true" --once

# Matikan LED
ros2 topic pub /led std_msgs/msg/Bool "data: false" --once

# Blink terus-menerus
ros2 topic pub /led std_msgs/msg/Bool "data: true" -r 1
# ↑ -r 1 = publish setiap 1 detik (blink)
```

## Coba Ini

1. **Blink 2 Hz:** `ros2 topic pub /led std_msgs/msg/Bool "data: true" -r 2`
2. **Ganti pin LED:** Edit pin di `led.ino` (cari `LED_PIN`)
3. **Integrasi dengan button:** Lihat explore/02-push-button, buat button kontrol LED

## Hubungan dengan Dasar ROS2

Konsep yang sama dengan `explore/02-pub-sub/listener.py` — bedanya, subscriber-nya ada di Arduino, bukan di PC.
