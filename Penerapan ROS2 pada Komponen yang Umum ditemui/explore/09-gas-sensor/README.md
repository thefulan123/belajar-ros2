# explore/09-gas-sensor — Baca Gas / Asap via ROS2

## Tujuan

Belajar **Publisher sensor analog** — mendeteksi kebocoran gas atau asap dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/gas` |
| Tipe | `std_msgs/Int32` |
| Data | 0 (aman) — 100 (berbahaya) |
| Frekuensi | 5 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `gas_sensor.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /gas
# data: 10  → udara normal
# data: 80  → banyak gas/asap
```

PENTING: Setelah upload, tunggu 30 detik agar sensor stabil.

## Coba Ini

1. **Dekatkan korek api (tidak dinyalakan) — gas LPG dari korek terbaca
2. **Asap dari dupa/kertas** — nilai naik
3. **Integrasi buzzer (explore/03):** Bunyikan alarm jika gas > 70
