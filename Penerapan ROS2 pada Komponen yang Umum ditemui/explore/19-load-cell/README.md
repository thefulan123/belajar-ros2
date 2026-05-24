# explore/19-load-cell — Baca Berat via ROS2 (Load Cell + HX711)

## Tujuan

Belajar **Publisher sensor berat** — membaca berat dari load cell dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/berat` |
| Tipe | `std_msgs/Float64` |
| Data | Berat dalam gram |
| Frekuensi | 5 Hz |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "HX711" by Bogdan Necula → Install

### 2. Kalibrasi
Sebelum dipakai, load cell perlu kalibrasi:

1. Upload code
2. Buka Serial Monitor (115200 baud)
3. Letakkan beban yang diketahui beratnya (misal 100g)
4. Catat nilai `hx711.read()` yang muncul
5. Hitung faktor = nilai / berat
6. Ganti `KALIBRASI_FAKTOR` di code

### 3. Upload ke Arduino
Buka `load_cell.ino` di Arduino IDE, upload ke board.

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek data
```bash
ros2 topic echo /berat
# data: 150.0  → 150 gram
```

## Coba Ini

1. **Timbang benda sekitar** — berapa gram?
2. **Tara:** Buat script Python subscribe /berat, record nilai awal sebagai offset
3. **Integrasi relay (explore/04):** Nyalakan relay jika berat > threshold (conveyor)
