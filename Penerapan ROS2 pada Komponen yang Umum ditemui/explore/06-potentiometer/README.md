# explore/06-potentiometer — Baca Potensiometer via ROS2

## Tujuan

Belajar **Publisher analog** — membaca nilai analog dan mengirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/potensiometer` |
| Tipe | `std_msgs/Int32` |
| Data | 0 — 100 (persentase) |
| Frekuensi | 20 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `potentiometer.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /potensiometer
# data: 0    → potensio diputar ke kiri penuh
# data: 50   → posisi tengah
# data: 100  → potensio diputar ke kanan penuh
```

## Coba Ini

1. **Kontrol LED brightness:** Buat script Python subscribe `/potensiometer`, publish ke `/led` dengan Bool (misal threshold > 50 nyala)
2. **Kontrol servo:** Nilai potensio 0-100 → sudut servo 0-180° (explore/13-servo)
3. **Kontrol buzzer:** Nilai potensio → frekuensi buzzer
