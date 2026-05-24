# Wiring: Fingerprint Sensor (AS608 / R305)

## Koneksi (UART)

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|------------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| TX | Hijau | D2 (SoftwareSerial RX) | D16 (RX2) |
| RX | Kuning | D3 (SoftwareSerial TX) | D17 (TX2) |

## Diagram

```
Arduino UNO        Fingerprint AS608
┌──────┐           ┌─────────────────┐
│ D2   ├──Hijau────┤ TX              │
│ D3   ├──Kuning───┤ RX              │
│ 5V   ├──Merah────┤ VCC             │
│ GND  ├──Hitam────┤ GND             │
└──────┘           └─────────────────┘
```

## Catatan
- Butuh library: "Adafruit Fingerprint Sensor Library"
- Komunikasi UART (Serial) — untuk UNO pakai SoftwareSerial
- Untuk UNO: pin D2 = RX, D3 = TX (SoftwareSerial)
- Untuk ESP32: pin D16 = RX2, D17 = TX2 (hardware UART2)
- JANGAN gunakan pin 0 (RX) dan 1 (TX) untuk fingerprint — dipakai micro-ROS
- Sensitivitas: butuh sidik jari yang jelas, tangan kering lebih baik
- Bisa simpan hingga 127-256 sidik jari (tergantung modul)
- Fingertip (buku jari) — sentuh perlahan, jangan ditekan
