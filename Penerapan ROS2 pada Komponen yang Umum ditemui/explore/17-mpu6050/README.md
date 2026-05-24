# explore/17-mpu6050 — Baca IMU (Accel + Gyro) via ROS2

## Tujuan

Belajar **Publisher data IMU** — membaca accelerometer dan gyroscope dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (multiple) |
| Topic | `/accel_x`, `/accel_y`, `/accel_z`, `/gyro_x`, `/gyro_y`, `/gyro_z` |
| Tipe | `std_msgs/Float64` |
| Frekuensi | 20 Hz |

## Cara Jalankan

### 1. Install library MPU6050
Arduino IDE → Tools → Manage Libraries → Cari "MPU6050" by Electronic Cats → Install

### 2. Upload ke Arduino
Buka `mpu6050.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /accel_x
# data: 0.02  → percepatan sumbu X (dalam G)

ros2 topic echo /gyro_z
# data: -0.5  → kecepatan sudut Z (dalam deg/s)
```

## Coba Ini

1. **Miringkan sensor** — nilai accel_x, accel_y berubah
2. **Putar sensor** — nilai gyro_z berubah
3. **Deteksi jatuh:** Jika accel total > 3G = ada benturan/jatuh
4. **Integrasi buzzer (explore/03):** Alarm jika sensor digerakkan terlalu keras
