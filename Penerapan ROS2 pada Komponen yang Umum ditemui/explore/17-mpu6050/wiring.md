# Wiring: MPU6050 (Accelerometer + Gyroscope)

## Koneksi (I2C)

| Pin MPU6050 | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| SCL | Biru | A5 (SCL) | D22 |
| SDA | Hijau | A4 (SDA) | D21 |

## Diagram

```
Arduino UNO        MPU6050
┌──────┐           ┌─────────┐
│ A4   ├──Hijau────┤ SDA     │
│      │           │         │
│ A5   ├──Biru─────┤ SCL     │
│      │           │         │
│ 5V   ├──Merah────┤ VCC     │
│      │           │         │
│ GND  ├──Hitam────┤ GND     │
└──────┘           └─────────┘
```

## Catatan
- MPU6050 = 6-DOF IMU (3-axis accel + 3-axis gyro)
- Komunikasi via **I2C** (bukan analog/digital biasa)
- Alamat I2C default: 0x68
- VCC: 3.3V (ESP32) atau 5V (Arduino UNO) — module MPU6050 punya regulator
- ESP32 pin I2C: default SDA=21, SCL=22
- Untuk UNO: A4=SDA, A5=SCL (jangan pakai pin digital biasa)
