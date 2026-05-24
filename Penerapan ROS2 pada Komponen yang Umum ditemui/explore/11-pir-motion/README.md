# explore/11-pir-motion — Deteksi Gerakan via ROS2

## Tujuan

Belajar **Publisher sensor digital** — mendeteksi gerakan manusia/hewan dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/gerakan` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = gerakan terdeteksi, `false` = tidak ada |
| Frekuensi | 20 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `pir_motion.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /gerakan
# data: false → tidak ada gerakan
# data: true  → ada yang bergerak!
```
PENTING: Setelah upload, tunggu **30-60 detik** agar sensor stabil.

## Coba Ini

1. **Lambai tangan di depan sensor** — data berubah ke true
2. **Diam tanpa bergerak** — setelah beberapa detik kembali false
3. **Integrasi LED (explore/01):** Nyalakan lampu saat gerakan terdeteksi
4. **Integrasi buzzer (explore/03):** Alarm saat ada gerakan
