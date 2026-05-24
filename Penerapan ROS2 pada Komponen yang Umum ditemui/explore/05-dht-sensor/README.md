# explore/05-dht-sensor — Baca Suhu & Kelembapan via ROS2

## Tujuan

Belajar **Publisher sensor data** — mengirim suhu dan kelembapan ke ROS2 dalam format custom dan Float64.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/suhu` (temperature), `/kelembapan` (humidity) |
| Tipe | `std_msgs/Float64` |
| Frekuensi | 1 Hz |

## Cara Jalankan

### 1. Install library DHT
Di Arduino IDE: Tools → Manage Libraries → Cari "DHT sensor library" by Adafruit → Install

### 2. Upload ke Arduino
Buka `dht_sensor.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /suhu
# data: 28.5

ros2 topic echo /kelembapan
# data: 65.2
```

## Coba Ini

1. **Hembuskan napas ke sensor** — suhu naik, kelembapan naik
2. **Pindahkan ke dekat AC** — suhu turun
3. **Integrasi buzzer** — bunyikan alarm jika suhu > 35°C
4. **Logging data** — buat Python script yang subscribe kedua topic, simpan ke CSV
