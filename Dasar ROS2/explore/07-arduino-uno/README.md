# explore/07-arduino-uno — Arduino + ROS2 dengan micro-ROS

## Tujuan

Belajar menghubungkan Arduino UNO ke ROS2 menggunakan **micro-ROS**:
- Arduino sebagai **publisher** — kirim data sensor ke ROS2
- Arduino sebagai **subscriber** — terima perintah dari ROS2
- micro-ROS Agent sebagai jembatan serial

## Yang Kamu Butuhkan

| Hardware | Software |
|----------|----------|
| Arduino UNO | Arduino IDE |
| USB kabel | micro-ROS library |
| Sensor LM35 (opsional) | micro-ROS Agent |
| LED + resistor (opsional) | ROS2 Humble |

## Arsitektur

```
Arduino UNO                      PC/Laptop                   ROS2 Network
(publisher_suhu.ino)             (micro-ROS Agent)           (ros2 topic)
      │                                │                         │
      ├── publish /suhu (Float32) ────►├── forward ────────────►│
      │                                │                         │
      │◄── subscribe /led (Bool) ──────┼── dari ROS2 ───────────┤
      │                                │                         │
```

## Cara Pakai

### 1. Upload Sketch ke Arduino

Buka file `.ino` di Arduino IDE, upload ke Arduino UNO.

Ada 2 sketch:
| Sketch | Fungsi | Topic |
|--------|--------|-------|
| `publisher_suhu/` | Kirim data suhu | `/suhu` (Float32) |
| `subscriber_led/ | Terima perintah LED | `/led` (Bool) |

### 2. Jalankan micro-ROS Agent

```bash
# Terminal 1
source /opt/ros/humble/setup.bash
bash run-agent.sh
```

### 3. Cek Koneksi

```bash
# Terminal 2
source /opt/ros/humble/setup.bash

# Cek node Arduino
ros2 node list
# Output: /arduino_sensor  (atau /arduino_led)

# Cek topic
ros2 topic list
# Output: /suhu  /led

# Lihat data sensor
ros2 topic echo /suhu

# Kirim perintah ke LED
ros2 topic pub /led std_msgs/msg/Bool "data: true" --once
ros2 topic pub /led std_msgs/msg/Bool "data: false" --once
```

## Integrasi dengan ROS2 Lain

Karena Arduino publish ke topic `/suhu`, semua node ROS2 lain bisa membaca data itu:

```bash
# Terminal 3 — Integrasi dengan node kita
cd "Dasar ROS2/src"
source install/setup.bash
ros2 run ros2_basics listener_node  # Subscribe ke /chatter (bukan /suhu)

# TAPI kamu bisa bikin node Python yang subscribe ke /suhu juga
```

Atau:

```bash
# Bridge: dari /suhu ke /chatter
ros2 topic pub /suhu std_msgs/msg/Float32 "data: 28.5" --once
```

## Coba Ini

1. **Ganti sensor** — Ubah `publisher_suhu.ino` untuk membaca sensor cahaya (LDR) atau jarak (ultrasonic)
2. **Tambah aktuator** — Tambah subscriber untuk mengontrol motor servo
3. **Integrasi dengan explore/** — Buat node Python di explore/02 yang subscribe ke `/suhu` dari Arduino
4. **Rubah baud rate** — Ganti Serial.begin(115200) ke 57600 atau 9600 (untuk kabel panjang)

## Error Umum

| Error | Solusi |
|-------|--------|
| `Permission denied: /dev/ttyACM0` | `sudo chmod 666 /dev/ttyACM0` |
| `Agent tidak melihat Arduino` | Cek port: `ls /dev/tty*` |
| `Publisher "suhu" not found` | Agent belum jalan, atau port salah |
| `Out of memory` | Sketch terlalu besar untuk UNO, kurangi fitur |

## Hubungan dengan Modul

- **[Modul 11](../../modul/11-micro-ros.md)** — Penjelasan lengkap micro-ROS
- **explore/02** — Pub/sub di PC (bandingkan dengan pub/sub di Arduino)
- **Modul 10** — Callback dan timer di Arduino juga pakai konsep yang sama
