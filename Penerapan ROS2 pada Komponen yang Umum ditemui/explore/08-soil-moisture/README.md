# explore/08-soil-moisture — Baca Kelembapan Tanah via ROS2

## Tujuan

Belajar **Publisher sensor analog** — membaca kelembapan tanah untuk sistem penyiraman otomatis.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/kelembapan_tanah` |
| Tipe | `std_msgs/Int32` |
| Data | 0 (kering) — 100 (basah) |
| Frekuensi | 5 Hz |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `soil_moisture.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /kelembapan_tanah
# data: 10  → tanah kering
# data: 80  → tanah basah
```

## Coba Ini

1. **Celupkan sensor ke air** — nilai 100%
2. **Biarkan di udara kering** — nilai mendekati 0
3. **Integrasi relay (explore/04):** Nyalakan pompa jika tanah kering (< 30)
