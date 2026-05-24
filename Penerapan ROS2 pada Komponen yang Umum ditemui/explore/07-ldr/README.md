# explore/07-ldr — Baca Intensitas Cahaya via ROS2

## Tujuan

Belajar **Publisher sensor analog** — membaca LDR dan mengirim intensitas cahaya ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/cahaya` |
| Tipe | `std_msgs/Int32` |
| Data | 0 (gelap) — 100 (terang) |
| Frekuensi | 10 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `ldr.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /cahaya
# data: 80  → terang
# data: 10  → gelap
```

## Coba Ini

1. **Tutup LDR dengan tangan** — nilai turun drastis
2. **Sorot senter ke LDR** — nilai naik
3. **Integrasi LED (explore/01):** Buat lampu otomatis — nyala saat gelap (< 30), mati saat terang
