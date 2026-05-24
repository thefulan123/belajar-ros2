# 01 — Daftar Komponen, Board, dan Alat

Daftar lengkap semua hardware yang digunakan dalam proyek ini.

---

## A. SENSOR — Input (30 komponen)

### A.1 Suhu & Lingkungan

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 1 | DHT11 | Digital (1-wire) | 3.3-5V | Publisher | Rp 10k | ⭐ Mudah |
| 2 | DHT22 | Digital (1-wire) | 3.3-5V | Publisher | Rp 25k | ⭐ Mudah |
| 3 | DS18B20 | Digital (1-wire) | 3.3-5V | Publisher | Rp 15k | ⭐ Mudah |
| 4 | BMP180 | I2C | 3.3V | Publisher | Rp 20k | ⭐⭐ Sedang |

### A.2 Jarak

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 5 | HC-SR04 Ultrasonic | Digital (2 pin) | 5V | Publisher | Rp 12k | ⭐⭐ Sedang |
| 6 | VL53L0X LiDAR | I2C | 3.3V | Publisher | Rp 60k | ⭐⭐ Sedang |

### A.3 Cahaya

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 7 | LDR + Resistor 10kΩ | Analog | 5V | Publisher | Rp 3k | ⭐ Mudah |
| 8 | Flame Sensor | Digital + Analog | 5V | Publisher | Rp 8k | ⭐ Mudah |
| 9 | BH1750 Lux Meter | I2C | 3.3V | Publisher | Rp 25k | ⭐⭐ Sedang |

### A.4 Gerakan & Posisi

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 10 | PIR HC-SR501 | Digital | 5V | Publisher | Rp 10k | ⭐ Mudah |
| 11 | MPU6050 (Accel+Gyro) | I2C | 3.3V | Publisher | Rp 30k | ⭐⭐ Sedang |
| 12 | Vibration SW-420 | Digital | 5V | Publisher | Rp 5k | ⭐ Mudah |
| 13 | Encoder KY-040 | Digital (2 pin) | 5V | Publisher | Rp 10k | ⭐⭐ Sedang |

### A.5 Cairan & Tanah

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 14 | Soil Moisture | Analog | 5V | Publisher | Rp 8k | ⭐ Mudah |
| 15 | Rain Sensor | Digital + Analog | 5V | Publisher | Rp 10k | ⭐ Mudah |
| 16 | Water Flow YF-S201 | Digital (pulse) | 5V | Publisher | Rp 20k | ⭐⭐ Sedang |

### A.6 Gas & Udara

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 17 | MQ-2 (Gas) | Analog | 5V | Publisher | Rp 12k | ⭐ Mudah |
| 18 | MQ-135 (Kualitas Udara) | Analog | 5V | Publisher | Rp 15k | ⭐ Mudah |

### A.7 Identifikasi

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 19 | RFID RC522 | SPI | 3.3V | Publisher | Rp 15k | ⭐⭐ Sedang |
| 20 | Fingerprint R307 | UART | 3.3V | Publisher | Rp 120k | ⭐⭐⭐ Sulit |
| 21 | Keypad 4x4 Matrix | Digital (8 pin) | 5V | Publisher | Rp 12k | ⭐⭐ Sedang |

### A.8 Input Mekanik

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 22 | Push Button | Digital | 5V | Publisher | Rp 2k | ⭐ Mudah |
| 23 | Potensiometer 10kΩ | Analog | 5V | Publisher | Rp 5k | ⭐ Mudah |
| 24 | Joystick Module | Analog (2) + Dig (1) | 5V | Publisher | Rp 12k | ⭐ Mudah |

### A.9 Berat & Tekanan

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 25 | Load Cell + HX711 | Digital (2 pin) | 5V | Publisher | Rp 40k | ⭐⭐ Sedang |
| 26 | Touch Sensor TTP223 | Digital | 5V | Publisher | Rp 5k | ⭐ Mudah |

### A.10 Audio & Kamera

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 27 | MAX4466 / MAX9814 Mic | Analog | 5V | Publisher | Rp 15k | ⭐ Mudah |
| 28 | Webcam USB | USB (PC) | - | Publisher | Rp 100k+ | ⭐⭐ Sedang |
| 29 | Camera OV2640 (ESP32) | ESP32 native | 3.3V | Publisher | Rp 40k | ⭐⭐⭐ Sulit |

### A.11 Lainnya

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 30 | GPS NEO-6M / NEO-8M | UART | 3.3V | Publisher | Rp 80k | ⭐⭐⭐ Sulit |

---

## B. AKTUATOR — Output (13 komponen)

### B.1 Cahaya & Visual

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 1 | LED 5mm + Resistor 220Ω | Digital (PWM) | 5V | Subscriber | Rp 2k | ⭐ Mudah |
| 2 | NeoPixel WS2812B | Digital (1 pin) | 5V | Subscriber | Rp 15k | ⭐⭐ Sedang |

### B.2 Suara

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 3 | Buzzer Active | Digital | 5V | Subscriber | Rp 3k | ⭐ Mudah |
| 4 | Buzzer Passive | Digital (PWM) | 5V | Subscriber | Rp 3k | ⭐ Mudah |
| 5 | Speaker Mini 8Ω | Digital (PWM) | 5V | Subscriber | Rp 5k | ⭐ Mudah |

### B.3 Gerak

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 6 | Servo SG90 | PWM (50Hz) | 5V | Subscriber | Rp 15k | ⭐ Mudah |
| 7 | Servo MG996R | PWM (50Hz) | 5-7V | Subscriber | Rp 40k | ⭐ Mudah |
| 8 | Motor DC + L298N | PWM (2 pin) | 5-12V | Subscriber | Rp 50k | ⭐⭐ Sedang |
| 9 | Stepper 28BYJ-48 + ULN2003 | Digital (4 pin) | 5V | Subscriber | Rp 20k | ⭐⭐ Sedang |
| 10 | Stepper NEMA17 + A4988 | Step/Dir | 8-12V | Subscriber | Rp 100k | ⭐⭐⭐ Sulit |
| 11 | Kipas DC 5V | Digital (PWM) | 5V | Subscriber | Rp 15k | ⭐ Mudah |

### B.4 Saklar & Katup

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 12 | Relay Module 1ch | Digital | 5V | Subscriber | Rp 8k | ⭐ Mudah |
| 13 | Relay Module 2ch / 4ch | Digital | 5V | Subscriber | Rp 15k | ⭐ Mudah |
| 14 | Solenoid Door Lock 12V | Digital (via relay) | 12V | Subscriber | Rp 30k | ⭐⭐ Sedang |
| 15 | Pompa Air Mini 3-6V | Digital (via relay) | 3-6V | Subscriber | Rp 15k | ⭐⭐ Sedang |

### B.5 Display

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 16 | LCD 16x2 I2C | I2C | 5V | Subscriber | Rp 25k | ⭐⭐ Sedang |
| 17 | OLED SSD1306 | I2C / SPI | 3.3-5V | Subscriber | Rp 30k | ⭐⭐ Sedang |
| 18 | TM1637 4-Digit | Digital (2 pin) | 5V | Subscriber | Rp 15k | ⭐ Mudah |

---

## C. BOARD & KOMUNIKASI (6 komponen)

| # | Komponen | Interface | Tegangan | Peran ROS2 | Biaya | Kesulitan |
|---|----------|-----------|----------|------------|------|-----------|
| 1 | Arduino UNO R3 | USB + Dig + An | 5V | Both | Rp 100k | ⭐ Mudah |
| 2 | Arduino Nano | USB + Dig + An | 5V | Both | Rp 60k | ⭐ Mudah |
| 3 | ESP32 DevKit | USB + WiFi + BT | 3.3V | Both (WiFi) | Rp 60k | ⭐⭐ Sedang |
| 4 | ESP8266 NodeMCU | USB + WiFi | 3.3V | Both (WiFi) | Rp 35k | ⭐⭐ Sedang |
| 5 | HC-05 Bluetooth | UART | 3.3-5V | Bridge | Rp 35k | ⭐⭐ Sedang |
| 6 | HC-06 Bluetooth | UART | 3.3-5V | Bridge | Rp 25k | ⭐⭐ Sedang |

---

## D. ALAT PENDUKUNG (10 item)

| # | Alat | Fungsi | Biaya |
|---|------|--------|-------|
| 1 | Breadboard + Kabel Jumper M/M + M/F | Rakit rangkaian tanpa solder | Rp 25k |
| 2 | Multimeter Digital | Cek tegangan, kontinuitas | Rp 50k |
| 3 | Resistor Kit (220Ω, 1kΩ, 10kΩ, 220kΩ) | Safety komponen | Rp 20k |
| 4 | Power Supply 5V 2A | Daya untuk board + komponen | Rp 30k |
| 5 | Power Supply 12V 2A | Daya untuk motor, solenoid | Rp 50k |
| 6 | USB Cable (Arduino) | Koneksi ke PC | Rp 15k |
| 7 | Logic Level Converter 3.3V-5V | Bridge sinyal sensor 3.3V | Rp 10k |
| 8 | Screw Terminal / Terminal Block | Koneksi rapi kabel besar | Rp 10k |
| 9 | Heat Shrink + Solder + Soldering Iron | Rakit permanen | Rp 100k |
| 10 | Step-down / Step-up regulator | Ubah tegangan suplai | Rp 20k |

---

## E. STARTER PACK — Minimal untuk Mulai

Kalau baru mulai, cukup beli ini dulu:

| # | Item | Estimasi |
|---|------|----------|
| 1 | Arduino UNO R3 (clone) | Rp 60k |
| 2 | Breadboard + Jumper | Rp 25k |
| 3 | 5x LED + 5x Resistor 220Ω | Rp 5k |
| 4 | 2x Push Button | Rp 2k |
| 5 | 1x Potensiometer 10kΩ | Rp 5k |
| 6 | 1x Buzzer | Rp 3k |
| 7 | 1x DHT11 | Rp 10k |
| 8 | 1x HC-SR04 Ultrasonic | Rp 12k |
| **Total** | | **~Rp 122k** |

Dengan starter pack ini, kamu bisa menjalankan 6 project pertama (explore/01 sampai explore/06).
