# explore/30-microphone — Baca Intensitas Suara via ROS2

## Tujuan

Belajar **Publisher audio sensor** — membaca level suara dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/suara` |
| Tipe | `std_msgs/Int32` |
| Data | 0 (senyap) — 100 (keras) |
| Frekuensi | 20 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `microphone.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /suara
# data: 10  → ruangan hening
# data: 80  → tepuk tangan / suara keras
```

## Coba Ini

1. **Tepuk tangan** — nilai naik drastis
2. **Bicara ke sensor** — nilai naik turun sesuai suara
3. **Clap switch:** Nyalakan LED (explore/01) jika 2 tepukan
4. **Integrasi relay (explore/04):** Nyalakan lampu dengan tepukan
