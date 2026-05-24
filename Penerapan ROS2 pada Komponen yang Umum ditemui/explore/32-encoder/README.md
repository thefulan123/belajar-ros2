# explore/32-encoder — Baca Rotary Encoder via ROS2

## Tujuan

Belajar **Publisher dengan interrupt** — membaca posisi rotary encoder dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher (2 topic) |
| Topic | `/encoder` (Int32 — posisi), `/encoder_button` (Bool) |
| Tipe | `std_msgs/Int32`, `std_msgs/Bool` |
| Data | Posisi: counter (naik/turun), Button: true = ditekan |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `encoder.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Cek data
```bash
ros2 topic echo /encoder
# data: 10  → putar ke kanan (posisi naik)
# data: 9   → putar ke kiri (posisi turun)

ros2 topic echo /encoder_button
# data: true → encoder ditekan
```

## Coba Ini

1. **Kontrol servo (explore/13):** Putar encoder → gerakkan servo
2. **Kontrol LED brightness:** Encoder untuk atur kecerahan
3. **Menu selection:** Putar pilih menu, tekan untuk konfirmasi
4. **Integrasi LCD (explore/20):** Tampilkan nilai encoder di LCD
