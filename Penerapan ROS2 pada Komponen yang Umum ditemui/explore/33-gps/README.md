# explore/33-gps — Baca GPS via ROS2

## Tujuan

Belajar **Publisher data lokasi** — membaca koordinat GPS dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (4 topic) |
| Topic | `/gps_lat`, `/gps_lng` (Float64), `/gps_alt` (Float64), `/gps_sats` (Int32) |
| Tipe | `std_msgs/Float64`, `std_msgs/Int32` |
| Data | Latitude, Longitude, Altitude (meter), Satellites |
| Frekuensi | 1 Hz |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "TinyGPSPlus" → Install

### 2. Upload ke Arduino
Buka `gps.ino` di Arduino IDE, upload ke board.

### 3. Bawa ke luar ruangan
GPS tidak akan fix di dalam ruangan — bawa ke tempat dengan view langit.

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek data
```bash
ros2 topic echo /gps_lat
# data: -6.2088  → latitude Jakarta

ros2 topic echo /gps_sats
# data: 8 → 8 satelit terlihat
```

## Coba Ini

1. **Bawa jalan-jalan keluar** — lihat koordinat berubah
2. **Logging route:** Simpan lat/lng ke CSV, visualisasi di Google Maps
3. **Geofencing:** Alarm jika posisi keluar area tertentu
4. **Integrasi buzzer (explore/03):** Beep jika mendekati waypoint
