# explore/24-rfid — Baca RFID Tag via ROS2

## Tujuan

Belajar **Publisher data identifikasi** — membaca UID kartu RFID dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/rfid` |
| Tipe | `std_msgs/String` |
| Data | UID tag dalam hex (contoh: "A1:B2:C3:D4") |
| Trigger | Publish setiap kali tag baru terbaca |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "MFRC522" by GithubCommunity → Install

### 2. Upload ke Arduino
Buka `rfid.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /rfid
# Tempelkan kartu RFID ke reader
# data: "A1:B2:C3:D4"
```

## Coba Ini

1. **Tempekan berbagai tag** — setiap tag punya UID unik
2. **Access control:** Buat Python node — hanya UID tertentu yang boleh akses
3. **Integrasi solenoid (explore/16):** Buka kunci hanya jika UID terdaftar
4. **Logging:** Simpan UID + timestamp ke file CSV
