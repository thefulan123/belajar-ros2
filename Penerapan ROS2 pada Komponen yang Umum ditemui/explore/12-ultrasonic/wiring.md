# Wiring: Ultrasonic HC-SR04

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 5V (via Vin) |
| TRIG | Kuning | D10 | D26 |
| ECHO | Hijau | D11 | D27 |
| GND | Hitam | GND | GND |

## Diagram

```
Arduino UNO        HC-SR04
┌──────┐           ┌─────────┐
│ D10  ├──Kuning───┤ TRIG    │
│      │           │         │
│ D11  ├──Hijau────┤ ECHO    │
│      │           │         │
│ 5V   ├──Merah────┤ VCC     │
│      │           │         │
│ GND  ├──Hitam────┤ GND     │
└──────┘           └─────────┘
```

## Catatan
- HC-SR04: jangkauan 2 cm - 400 cm, akurasi ±3 mm
- Cara kerja: TRIG HIGH 10μs → ECHO HIGH (durasi = waktu tempuh suara)
- Jarak = (durasi ECHO × kecepatan suara) / 2
- Kecepatan suara ≈ 343 m/s (pada 20°C)
- Sudut deteksi ~15°, benda di luar sudut ini tidak terdeteksi
- Permukaan lunak (kain, spons) menyerap suara — jarak terbaca lebih pendek
