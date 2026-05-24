# explore/12-ultrasonic — Baca Jarak via ROS2

## Tujuan

Belajar **Publisher sensor jarak** — mengukur jarak dengan HC-SR04 dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/jarak` |
| Tipe | `std_msgs/Float64` |
| Data | Jarak dalam cm (0 - 400) |
| Frekuensi | 10 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `ultrasonic.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /jarak
# data: 150.0  → tidak ada benda dalam 150 cm
# data: 10.0   → benda sangat dekat (10 cm)
```

## Coba Ini

1. **Letakkan tangan di depan sensor** — gerak maju-mundur, lihat nilai berubah
2. **Integrasi LED (explore/01):** Nyalakan LED jika jarak < 20 cm
3. **Integrasi buzzer (explore/03):** Bunyikan buzzer dengan frekuensi tergantung jarak (parking sensor)
4. **Parking sensor simulator:** Buzzer bunyi makin cepat makin dekat
