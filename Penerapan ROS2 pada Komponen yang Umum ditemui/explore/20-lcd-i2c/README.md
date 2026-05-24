# explore/20-lcd-i2c — Tampilkan Teks di LCD via ROS2

## Tujuan

Belajar **Subscriber dengan LCD** — menampilkan data ROS2 di layar LCD.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/lcd` |
| Tipe | `std_msgs/String` |
| Data | Teks, format "baris1\nbaris2" untuk 2 baris |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "LiquidCrystal I2C" by Frank de Brabander → Install

### 2. Upload ke Arduino
Buka `lcd_i2c.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Kirim teks
```bash
# Tampilkan teks baris 1
ros2 topic pub /lcd std_msgs/msg/String "data: 'Halo ROS2!'" --once

# Tampilkan 2 baris (gunakan \n)
ros2 topic pub /lcd std_msgs/msg/String "data: 'Suhu: 28C\nKelemb: 65%'" --once
```

## Coba Ini

1. **Integrasi DHT (explore/05):** Buat Python node yang subscribe suhu + kelembapan, publish ke /lcd
2. **Scrolling text:** Kirim teks panjang, geser tiap 0.5 detik
3. **Counter:** Display hitungan mundur
