# Wiring: Robot Monitoring Rumah (Proyek Akhir)

## Koneksi — Arduino UNO

| Komponen | Pin Arduino | Keterangan |
|----------|-------------|------------|
| **Motor Driver L298N** | | |
| ENA | D9 | PWM kecepatan |
| IN1 | D10 | Arah motor 1 |
| IN2 | D11 | Arah motor 2 |
| **Ultrasonic HC-SR04** | | |
| TRIG | D2 | Trigger ping |
| ECHO | D3 | Echo receive |
| **DHT11** | | |
| DATA | D7 | Data pin (pakai resistor pull-up 4.7kΩ) |
| **MQ-2 Gas Sensor** | | |
| AOUT | A0 | Analog output (0-5V gas level) |
| **Flame Sensor** | | |
| DOUT | D4 | Digital output (LOW = api terdeteksi) |
| **Buzzer** | | |
| SIG | D5 | Active buzzer (HIGH = bunyi) |
| **LCD I2C 16x2** | | |
| SDA | A4 | I2C data |
| SCL | A5 | I2C clock |

## Koneksi — ESP32

| Komponen | Pin ESP32 |
|----------|-----------|
| Motor L298N ENA | D25 |
| Motor L298N IN1 | D26 |
| Motor L298N IN2 | D27 |
| HC-SR04 TRIG | D13 |
| HC-SR04 ECHO | D14 |
| DHT11 DATA | D32 |
| MQ-2 AOUT | GPIO34 |
| Flame DOUT | D15 |
| Buzzer SIG | D5 |
| LCD SDA | D21 |
| LCD SCL | D22 |

## Power

| Komponen | Tegangan | Arus |
|----------|----------|------|
| Arduino UNO | 5V (via USB) | ~500mA |
| Motor L298N | 7-12V (external) | ~1A (tergantung motor) |
| Sensor (total) | 5V (dari Arduino) | ~200mA |
| ESP32 | 5V (via USB) | ~250mA |

> **PERHATIAN:** Jangan supply motor L298N dari pin 5V Arduino — gunakan power supply terpisah!
> Ground semua perangkat HARUS terhubung (Arduino, L298N, sensor).

## Diagram Blok

```
[Power 12V] ──┬── [L298N Motor Driver] ── [Motor DC]
              │
              ├── [Arduino 5V pin] ──┬── [HC-SR04]
              │                      ├── [DHT11]
              │                      ├── [MQ-2]
              │                      ├── [Flame]
              │                      ├── [Buzzer]
              │                      └── [LCD I2C]
              │
              └── [ESP32] (alternatif, via USB terpisah)
```

Lihat wiring detail masing-masing komponen di explore/ masing-masing.
