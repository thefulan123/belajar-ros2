# 02 — Klasifikasi Peran ROS2 per Komponen

Setiap komponen punya **peran ROS2** tetap berdasarkan fungsinya dalam sistem.

---

## PUBLISHER — Sensor / Input

Komponen yang **mengirim data** dari dunia nyata ke ROS2.

| Komponen | Tipe Data ROS2 | Topic | Frekuensi |
|----------|---------------|-------|-----------|
| Push Button | `std_msgs/Bool` | `/tombol` | On change |
| Potensiometer | `std_msgs/Int32` | `/potensiometer` | 10 Hz |
| LDR | `std_msgs/Int32` | `/cahaya` | 5 Hz |
| DHT11/DHT22 | `std_msgs/Float32` (2x) | `/suhu`, `/kelembaban` | 1 Hz |
| DS18B20 | `std_msgs/Float32` | `/suhu_air` | 1 Hz |
| HC-SR04 | `std_msgs/Float32` | `/jarak` | 5 Hz |
| VL53L0X | `std_msgs/Float32` | `/jarak_akurat` | 10 Hz |
| PIR Motion | `std_msgs/Bool` | `/gerakan` | On change |
| Flame Sensor | `std_msgs/Bool` | `/api` | 5 Hz |
| MQ-2 Gas | `std_msgs/Int32` | `/gas` | 2 Hz |
| MQ-135 | `std_msgs/Int32` | `/kualitas_udara` | 2 Hz |
| Soil Moisture | `std_msgs/Int32` | `/kelembaban_tanah` | 2 Hz |
| Rain Sensor | `std_msgs/Bool` | `/hujan` | 5 Hz |
| Water Flow | `std_msgs/Float32` | `/debit_air` | 1 Hz |
| MPU6050 | `std_msgs/Float32[6]` | `/imu` | 20 Hz |
| Vibration SW-420 | `std_msgs/Bool` | `/getaran` | On change |
| Load Cell HX711 | `std_msgs/Float32` | `/berat` | 5 Hz |
| Joystick | `std_msgs/Int32[2]` + `Bool` | `/joystick` | 10 Hz |
| RFID RC522 | `std_msgs/String` | `/rfid` | On scan |
| Fingerprint | `std_msgs/Int32` | `/sidik_jari` | On scan |
| Keypad 4x4 | `std_msgs/String` | `/keypad` | On press |
| GPS NEO-6M | `std_msgs/String` | `/gps` | 1 Hz |
| Encoder KY-040 | `std_msgs/Int32` | `/encoder` | On change |
| MAX4466 Mic | `std_msgs/Int32` | `/suara` | 10 Hz |
| Webcam USB | `sensor_msgs/Image` | `/kamera` | 15-30 Hz |
| OV2640 (ESP32) | `sensor_msgs/Image` | `/kamera` | 10-15 Hz |
| BMP180 | `std_msgs/Float32` | `/tekanan` | 1 Hz |
| BH1750 | `std_msgs/Float32` | `/lux` | 5 Hz |
| MAX30100 | `std_msgs/Int32` | `/heartrate` | 1 Hz |
| TCRT5000 | `std_msgs/Int32` | `/line_sensor` | 10 Hz |
| Touch TTP223 | `std_msgs/Bool` | `/touch` | On change |

---

## SUBSCRIBER — Aktuator / Output

Komponen yang **menerima perintah** dari ROS2 dan melakukan aksi.

| Komponen | Tipe Data ROS2 | Topic | Action |
|----------|---------------|-------|--------|
| LED | `std_msgs/Bool` atau `Int32` | `/led` | ON/OFF atau brightness |
| NeoPixel WS2812B | `std_msgs/Int32[3]` | `/neopixel` | Warna RGB |
| Buzzer Active | `std_msgs/Bool` | `/buzzer` | ON/OFF |
| Buzzer Passive | `std_msgs/Int32` | `/buzzer` | Frekuensi nada |
| Speaker 8Ω | `std_msgs/Int32` | `/speaker` | Frekuensi nada |
| Servo SG90 | `std_msgs/Int32` (0-180) | `/servo` | Sudut |
| Motor DC + L298N | `std_msgs/Int32` (-255..255) | `/motor` | Kecepatan + arah |
| Stepper 28BYJ-48 | `std_msgs/Int32` | `/stepper` | Jumlah langkah |
| Solenoid 12V | `std_msgs/Bool` | `/solenoid` | Buka/tutup |
| Relay Module | `std_msgs/Bool` | `/relay` | ON/OFF |
| Kipas DC | `std_msgs/Int32` | `/kipas` | Kecepatan PWM |
| Pompa Air | `std_msgs/Bool` | `/pompa` | ON/OFF |
| LCD 16x2 I2C | `std_msgs/String` | `/lcd` | Tampilkan teks |
| OLED SSD1306 | `std_msgs/String` | `/oled` | Tampilkan teks |
| TM1637 4-Digit | `std_msgs/Int32` | `/display` | Tampilkan angka |

---

## TWO-WAY — Publisher + Subscriber

Komponen yang bisa **mengirim DAN menerima** data.

| Komponen | Publish | Subscribe | Use Case |
|----------|---------|-----------|----------|
| ESP32 | Sensor data | Aktuator control | Robot wireless, monitoring jarak jauh |
| Arduino UNO | Bisa (sensor) | Bisa (aktuator) | Robot dengan sensor + aktuator |
| HC-05 Bluetooth | Data dari serial BT | Data ke serial BT | Bridge/remote via smartphone |
| Robot Base | Odometry, baterai | Velocity cmd | Mobile robot |

---

## TOPIC NAMING CONVENTION

Gunakan format: `/jenis_fungsi` (lowercase, underscore).

```
Sensor → /suhu, /jarak, /gas, /imu, /berat, /gps, /cahaya
Aktuator → /led, /servo, /motor_kiri, /motor_kanan, /relay_1
Status → /baterai, /error, /status
Perintah → /cmd_vel, /cmd_led, /cmd_servo
```

---

## STREAMING FREQUENCY REFERENCE

| Jenis Data | Frekuensi | Alasan |
|-----------|-----------|--------|
| Suhu lingkungan | 1 Hz | Tidak berubah cepat |
| Kelembaban tanah | 1-2 Hz | Perubahan lambat |
| Jarak (ultrasonic) | 5-10 Hz | Cukup untuk hindar rintangan |
| IMU (MPU6050) | 20-50 Hz | Butuh respons cepat |
| Tombol | On change | Hemat bandwidth |
| GPS | 1-5 Hz | Update posisi |
| Webcam | 15-30 Hz | Video流畅 |
| Encoder | 10-50 Hz | Butuh presisi kecepatan |
