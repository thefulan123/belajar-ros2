# 03 — Panduan Wiring Dasar

Panduan ini menjelaskan cara menghubungkan komponen ke Arduino/ESP dengan aman dan benar.

---

## 1. PRINSIP DASAR

### 1.1 Tiga Kabel Utama

Setiap komponen umumnya punya 3 koneksi:

| Kabel | Warna Standar | Fungsi |
|-------|--------------|--------|
| **VCC / Power** | Merah | Catu daya (5V atau 3.3V) |
| **GND / Ground** | Hitam / Biru | Ground (kembali) |
| **Signal / DATA** | Kuning / Hijau / Putih | Data / sinyal |

### 1.2 Aturan Emas

1. **GND harus disatukan** — Semua komponen harus share GND yang sama
2. **Tegangan sesuai spesifikasi** — Jangan kasih 5V ke komponen 3.3V
3. **LED harus pakai resistor** — Minimal 220Ω, tanpa resistor LED bisa meledak
4. **Motor jangan langsung dari pin Arduino** — Pin Arduino cuma bisa 40mA, motor butuh 100mA+
5. **Power terpisah untuk motor** — Jangan ambil daya motor dari pin 5V Arduino

---

## 2. WARNA KABEL STANDAR

Gunakan kode warna ini biar wiring rapi dan mudah di-debug:

| Fungsi | Warna | Contoh |
|--------|-------|--------|
| VCC / Power | Merah | 5V, 3.3V |
| GND | Hitam | Ground |
| Sinyal Digital | Kuning | D2, D3, D4 |
| Sinyal Analog | Hijau | A0, A1, A2 |
| I2C SDA | Biru | A4 (UNO) / D21 (ESP32) |
| I2C SCL | Putih | A5 (UNO) / D22 (ESP32) |
| PWM | Oranye | Pin dengan ~ |

---

## 3. TEGANGAN DAN ARUS

### 3.1 Batas Arduino UNO

| Parameter | Max | Catatan |
|-----------|-----|---------|
| Tegangan input pin | 5V | Jangan lebih! |
| Arus per pin | 40 mA | LED aman, motor tidak |
| Arus total semua pin | 200 mA | Semua pin digabung |
| Tegangan output 5V | 5V | Max 500mA (dari USB) |
| Tegangan output 3.3V | 3.3V | Max 150mA |

### 3.2 Kapan Perlu External Power

| Kondisi | Solusi |
|---------|--------|
| Motor DC / Stepper | Pakai driver L298N + power supply terpisah |
| Servo (lebih dari 1) | Power servo dari external 5V |
| Solenoid / Relay besar | Power terpisah (sesuai tegangan) |
| NeoPixel (banyak) | Power terpisah (setiap 30 LED butuh ~1A) |
| ESP32 saat WiFi aktif | Jangan pakai regulator Arduino, power langsung 5V |

---

## 4. KONEKSI UMUM

### 4.1 Sensor Digital (DHT11, PIR, Button, dll)

```
Sensor                   Arduino/ESP
┌──────┐                ┌─────────┐
│ VCC  ├────────────────┤ 5V/3.3V │
│ DATA ├────────────────┤ D2-D13  │
│ GND  ├────────────────┤ GND     │
└──────┘                └─────────┘
```

Catatan: Sensor 1-wire (DHT) kadang butuh resistor pull-up 10kΩ antara VCC dan DATA.

### 4.2 Sensor Analog (LDR, Potensiometer, Soil Moisture)

```
Sensor                   Arduino/ESP
┌──────┐                ┌─────────┐
│ VCC  ├────────────────┤ 5V      │
│ OUT  ├────────────────┤ A0-A5   │
│ GND  ├────────────────┤ GND     │
└──────┘                └─────────┘
```

Potensiometer:

```
Potensio                 Arduino
┌──────┐                ┌─────────┐
│ VCC  ├────────────────┤ 5V      │
│ OUT  ├────────────────┤ A0      │
│ GND  ├────────────────┤ GND     │
└──────┘                └─────────┘
```

### 4.3 Sensor I2C (MPU6050, LCD I2C, OLED, BMP180)

```
Sensor I2C               Arduino UNO           ESP32
┌──────┐                ┌─────────┐          ┌─────────┐
│ VCC  ├────────────────┤ 5V/3.3V │          │ 3.3V    │
│ SDA  ├────────────────┤ A4      │          │ D21     │
│ SCL  ├────────────────┤ A5      │          │ D22     │
│ GND  ├────────────────┤ GND     │          │ GND     │
└──────┘                └─────────┘          └─────────┘
```

I2C bisa并联 (daisy chain) — semua sensor I2C bisa pakai SDA/SCL yang sama.

### 4.4 Sensor UART (GPS, Fingerprint, HC-05 Bluetooth)

```
Sensor UART              Arduino UNO
┌──────┐                ┌─────────┐
│ VCC  ├────────────────┤ 5V      │
│ TX   ├────────────────┤ RX (D3) │  ← Cross!
│ RX   ├────────────────┤ TX (D2) │  ← Cross!
│ GND  ├────────────────┤ GND     │
└──────┘                └─────────┘
```

PENTING: TX sensor → RX Arduino, RX sensor → TX Arduino (cross / silang).

### 4.5 Aktuator Sederhana (LED, Buzzer)

```
LED                      Arduino
┌──────┐   220Ω          ┌─────────┐
│ (+)  ├──/\/\/\─────────┤ D3 (PWM)│
│ (-)  ├─────────────────┤ GND     │
└──────┘                 └─────────┘
```

LED (+) = kaki panjang (anoda). LED (-) = kaki pendek (katoda).

### 4.6 Motor DC + Driver L298N

```
L298N                    Arduino         Power
┌──────────┐            ┌─────────┐    ┌─────────┐
│ VCC (12V)├───────────────────────────┤ PSU 12V │
│ GND      ├───────────────────────────┤ GND     │ ← Satu GND!
│ 5V       ├───────────────────────────┤ (opsional)
│ IN1      ├────────────────┤ D5      │
│ IN2      ├────────────────┤ D6      │
│ ENA (PWM)├────────────────┤ D9      │
│ Motor A  ├──── ke motor DC ──────────┤
│ Motor B  ├──── ke motor DC ──────────┤
└──────────┘               └─────────┘
```

PENTING: GND L298N harus terhubung ke GND Arduino.

### 4.7 Servo SG90

```
Servo                    Arduino
┌──────┐                ┌─────────┐
│ Merah ├────────────────┤ 5V      │
│ Oranye├────────────────┤ D9 (PWM)│
│ Coklat├────────────────┤ GND     │
└──────┘                └─────────┘
```

Untuk lebih dari 1 servo: power servo dari external 5V, jangan dari Arduino.

---

## 5. TABEL PIN ARDUINO UNO

| Pin | Fungsi Utama | Fungsi Lain |
|-----|-------------|-------------|
| D0 | RX | Serial UART |
| D1 | TX | Serial UART |
| D2-D13 | Digital I/O | D3, D5, D6, D9, D10, D11: PWM (~) |
| D10 | SS | SPI |
| D11 | MOSI | SPI |
| D12 | MISO | SPI |
| D13 | SCK / LED | SPI |
| A0-A5 | Analog Input | A4=SDA, A5=SCL (I2C) |
| 5V | Output 5V | - |
| 3.3V | Output 3.3V | Max 150mA |
| GND | Ground | (3 pin) |
| VIN | Input 7-12V | Power dari adaptor |

---

## 6. TABEL PIN ESP32

| Pin | Fungsi | Catatan |
|-----|--------|---------|
| D21 | SDA (I2C) | Untuk LCD, MPU, OLED |
| D22 | SCL (I2C) | - |
| D23 | MOSI (SPI) | - |
| D19 | MISO (SPI) | - |
| D18 | SCK (SPI) | - |
| D5 | SS (SPI) | - |
| D4, D16, D17, D25 | PWM | Untuk servo, motor |
| D2 | Built-in LED | - |
| TX0 / RX0 | Serial UART | Untuk GPS, fingerprint |
| 3.3V | Output 3.3V | JANGAN kasih 5V langsung |
| VIN | Input 5V | Power dari USB |

CATATAN: ESP32 adalah **3.3V logic** — jangan kasih sinyal 5V langsung!

---

## 7. CHECKLIST SEBELUM NYALAKAN

Sebelum memberikan power:

- [ ] Tegangan sudah sesuai (3.3V vs 5V)?
- [ ] GND semua terhubung?
- [ ] Resistor untuk LED sudah terpasang?
- [ ] Motor pakai driver?
- [ ] Tidak ada kabel terbalik?
- [ ] USB terhubung?
- [ ] Board terdeteksi di komputer?

## 8. TROUBLESHOOTING WIRING

| Masalah | Kemungkinan | Cek |
|---------|------------|-----|
| Komponen tidak hidup | Tidak dapat power | Cek VCC dan GND dengan multimeter |
| Data tidak terbaca | Salah pin signal | Cek tabel wiring di explore/XX |
| Nilai sensor aneh | Kabel longgar atau noise | Perpendek kabel, perkuat koneksi |
| Arduino restart terus | Arus terlalu besar | Pakai power supply terpisah |
| ESP32 hang | Power kurang | Pakai power supply 5V 2A |
| Servo bergetar | Power servo kurang | External power untuk servo |
| LCD tidak muncul | I2C address salah | Scan: `I2C Scanner` sketch |
