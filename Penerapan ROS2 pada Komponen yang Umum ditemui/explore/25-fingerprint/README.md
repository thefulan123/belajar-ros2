# explore/25-fingerprint — Baca Sidik Jari via ROS2

## Tujuan

Belajar **Publisher sensor biometrik** — mendeteksi sidik jari dan kirim ID ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/sidikjari` |
| Tipe | `std_msgs/Int32` |
| Data | ID sidik jari (1-127) jika cocok, -1 jika tidak dikenali |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "Adafruit Fingerprint Sensor Library" → Install

### 2. Upload ke Arduino
Buka `fingerprint.ino` di Arduino IDE, upload ke board.

### 3. Daftarkan sidik jari
Sebelum dipakai, daftarkan sidik jari dulu via Serial Monitor:
- Buka Serial Monitor (115200 baud)
- Lihat: "Fingerprint sensor ready"
- Tempelkan jari → ID akan muncul di topic /sidikjari

Jika baru pertama kali, **enroll** dulu via contoh sketch "enroll" dari Arduino → File → Examples → Adafruit Fingerprint Sensor Library → enroll

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek data
```bash
ros2 topic echo /sidikjari
# Tempelkan jari yang sudah didaftarkan
# data: 1  → ID sidik jari = 1
```

## Coba Ini

1. **Daftarkan beberapa jari** — ibu jari = ID 1, telunjuk = ID 2, dst
2. **Access control:** Integrasi dengan solenoid (explore/16) — buka kunci jika sidik jari cocok
3. **Absensi:** Simpan ID + timestamp ke file CSV
