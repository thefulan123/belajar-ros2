# Penerapan ROS2 pada Komponen yang Umum Ditemui

Proyek ini berisi **38 proyek praktik** menghubungkan komponen elektronik umum ke ROS2 menggunakan **micro-ROS** (Arduino UNO / ESP32).

---

## Prasyarat

Sebelum memulai, pastikan sudah menyelesaikan atau paham:

1. **Dasar ROS2/** — Node, Topic, Publisher, Subscriber, Callback
2. **[Modul 11 — micro-ROS](../Dasar%20ROS2/modul/11-micro-ros.md)** — Teori micro-ROS dan instalasi
3. **[Referensi/00](referensi/00-software-requirements.md)** — Software requirements

---

## Klasifikasi Komponen

| Peran | Jumlah | Contoh |
|-------|--------|--------|
| **Publisher** (sensor → ROS2) | 22 | DHT (suhu), Ultrasonic (jarak), GPS, dll |
| **Subscriber** (ROS2 → aktuator) | 14 | LED, Servo, Motor DC, Relay, dll |
| **Two-way** | 2 | ESP32 WiFi, Bluetooth HC-05 |
| **Integrasi & Proyek Akhir** | 2 | 37-system-integration, 38-final-project |

Lihat [KORELASI.md](../Dasar%20ROS2/docs/KORELASI.md) untuk mapping lengkap modul ↔ komponen.

---

## Cara Pakai

### 1. Pilih komponen
Cari folder komponen di `explore/XX-nama-komponen/`

### 2. Baca wiring
Setiap folder punya `wiring.md` — tabel koneksi pin + diagram

### 3. Upload sketch
```bash
Buka .ino di Arduino IDE
Pilih board: Arduino UNO (atau ESP32)
Upload
```

### 4. Jalankan micro-ROS Agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek di ROS2
```bash
ros2 topic list
ros2 topic echo /nama_topic
```

---

## Starter Pack (Minimal)

| Item | Estimasi | Dipakai di |
|------|----------|------------|
| Arduino UNO R3 | Rp 60k | Semua explore |
| Breadboard + Jumper | Rp 25k | Semua explore |
| 5x LED + Resistor | Rp 5k | explore/01-led |
| Push Button | Rp 2k | explore/02-push-button |
| Potensiometer | Rp 5k | explore/06-potentiometer |
| Buzzer | Rp 3k | explore/03-buzzer |
| DHT11 | Rp 10k | explore/05-dht-sensor |
| **Total** | **~Rp 110k** | Cukup untuk explore 01-06 |

---

## Modul Dasar ROS2 Terkait

| Modul | Relevansi |
|:---|---:|
| [Modul 03 — Node](../Dasar%20ROS2/modul/03-node.md) | Setiap `.ino` adalah ROS2 node |
| [Modul 04 — Topic](../Dasar%20ROS2/modul/04-topic-pub-sub.md) | Semua komunikasi via topic pub/sub |
| [Modul 10 — Callback & Timer](../Dasar%20ROS2/modul/10-callback-timer.md) | Setiap `.ino` punya callback + timer |
| [Modul 11 — micro-ROS](../Dasar%20ROS2/modul/11-micro-ros.md) | Teknologi inti: ROS2 di Arduino/ESP32 |
| [KORELASI.md](../Dasar%20ROS2/docs/KORELASI.md) | Mapping lengkap modul ↔ komponen |

---

## Daftar Isi

### Publisher (Sensor — mengirim data ke ROS2)
| # | Komponen | Topic | Modul |
|:---:|:---|:---|---:|
| 02 | [Push Button](explore/02-push-button/) | `/tombol` | 03, 04, 10, 11 |
| 06 | [Potentiometer](explore/06-potentiometer/) | `/potensiometer` | 03, 04, 10, 11 |
| 07 | [LDR](explore/07-ldr/) | `/cahaya` | 03, 04, 10, 11 |
| 05 | [DHT Sensor](explore/05-dht-sensor/) | `/suhu`, `/kelembapan` | 03, 04, 10, 11 |
| 12 | [Ultrasonic HC-SR04](explore/12-ultrasonic/) | `/jarak` | 03, 04, 10, 11 |
| 11 | [PIR Motion](explore/11-pir-motion/) | `/gerakan` | 03, 04, 10, 11 |
| 10 | [Flame Sensor](explore/10-flame-sensor/) | `/api` | 03, 04, 10, 11 |
| 09 | [Gas Sensor MQ-2](explore/09-gas-sensor/) | `/gas` | 03, 04, 10, 11 |
| 08 | [Soil Moisture](explore/08-soil-moisture/) | `/kelembaban_tanah` | 03, 04, 10, 11 |
| 28 | [Rain Sensor](explore/28-rain-sensor/) | `/hujan` | 03, 04, 10, 11 |
| 27 | [Water Flow](explore/27-water-flow/) | `/debit_air` | 03, 04, 10, 11 |
| 17 | [MPU6050 IMU](explore/17-mpu6050/) | `/imu` | 03, 04, 10, 11 |
| 18 | [Vibration SW-420](explore/18-vibration/) | `/getaran` | 03, 04, 10, 11 |
| 19 | [Load Cell HX711](explore/19-load-cell/) | `/berat` | 03, 04, 10, 11 |
| 23 | [Joystick](explore/23-joystick/) | `/joystick` | 03, 04, 10, 11 |
| 24 | [RFID RC522](explore/24-rfid/) | `/rfid` | 03, 04, 10, 11 |
| 25 | [Fingerprint](explore/25-fingerprint/) | `/sidik_jari` | 03, 04, 10, 11 |
| 26 | [Keypad 4x4](explore/26-keypad/) | `/keypad` | 03, 04, 10, 11 |
| 33 | [GPS NEO-6M](explore/33-gps/) | `/gps` | 03, 04, 10, 11 |
| 32 | [Encoder KY-040](explore/32-encoder/) | `/encoder` | 03, 04, 10, 11 |
| 30 | [Microphone MAX4466](explore/30-microphone/) | `/suara` | 03, 04, 10, 11 |
| 36 | [Webcam USB](explore/36-webcam/) | `/kamera` | 03, 04, 10, 11 |

### Subscriber (Aktuator — menerima perintah dari ROS2)
| # | Komponen | Topic | Modul |
|:---:|:---|:---|---:|
| 01 | [LED](explore/01-led/) | `/led` | 03, 04, 10, 11 |
| 03 | [Buzzer](explore/03-buzzer/) | `/buzzer` | 03, 04, 10, 11 |
| 04 | [Relay](explore/04-relay/) | `/relay` | 03, 04, 10, 11 |
| 13 | [Servo SG90](explore/13-servo/) | `/servo` | 03, 04, 10, 11 |
| 14 | [Motor DC L298N](explore/14-motor-dc/) | `/motor` | 03, 04, 10, 11 |
| 15 | [Stepper 28BYJ-48](explore/15-stepper/) | `/stepper` | 03, 04, 10, 11 |
| 16 | [Solenoid 12V](explore/16-solenoid/) | `/solenoid` | 03, 04, 10, 11 |
| 20 | [LCD I2C](explore/20-lcd-i2c/) | `/lcd` | 03, 04, 10, 11 |
| 21 | [OLED SSD1306](explore/21-oled/) | `/oled` | 03, 04, 10, 11 |
| 22 | [NeoPixel WS2812B](explore/22-neopixel/) | `/neopixel` | 03, 04, 10, 11 |
| 29 | [Water Pump](explore/29-water-pump/) | `/pompa` | 03, 04, 10, 11 |
| 31 | [Speaker 8Ω](explore/31-speaker/) | `/speaker` | 03, 04, 10, 11 |

### Two-way / Special
| # | Komponen | Topic | Modul |
|:---:|:---|:---|---:|
| 34 | [ESP32 WiFi](explore/34-esp32-wifi/) | `/wifi_status` | 03, 04, 10, 11 |
| 35 | [Bluetooth HC-05](explore/35-bluetooth/) | `/bluetooth` | 03, 04, 10, 11 |
| 37 | [System Integration](explore/37-system-integration/) | Various | 03–11 |
| 38 | [Final Project](explore/38-final-project/) | Various | 03–11 |

### Referensi
- [00 — Software Requirements](referensi/00-software-requirements.md)
- [01 — Daftar Komponen](referensi/01-daftar-komponen.md)
- [02 — Klasifikasi Peran ROS2](referensi/02-klasifikasi-peran-ros2.md)
- [03 — Panduan Wiring Dasar](referensi/03-panduan-wiring-dasar.md)

### Error & Disclaimer
- [ERRORS.md](docs/ERRORS.md)
- [Disclaimer](docs/disclaimer.md)
