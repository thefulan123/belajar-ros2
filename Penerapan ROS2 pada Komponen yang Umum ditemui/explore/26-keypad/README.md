# explore/26-keypad — Baca Keypad 4x4 via ROS2

## Tujuan

Belajar **Publisher input matrix** — membaca tombol keypad dan kirim karakter ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/keypad` |
| Tipe | `std_msgs/String` |
| Data | Karakter tombol yang ditekan ("1", "A", "*", dll) |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "Keypad" by Mark Stanley → Install

### 2. Upload ke Arduino
Buka `keypad.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /keypad
# Tekan tombol pada keypad
# data: "1"
# data: "5"
# data: "#"
```

## Coba Ini

1. **Password entry:** Buat Python node — subscribe /keypad, jika kode benar ("1234#") → unlock
2. **Kalkulator:** Baca angka + operator via keypad, tampilkan hasil di LCD (explore/20)
3. **Integrasi solenoid (explore/16):** Buka kunci jika password benar
4. **Kombinasi RFID (explore/24):** Kartu + PIN untuk akses ganda
