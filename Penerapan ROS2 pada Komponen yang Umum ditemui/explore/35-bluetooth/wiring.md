# Wiring: Bluetooth HC-05

## Koneksi (UART)

| Pin HC-05 | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| TX | Hijau | D2 (SoftwareSerial RX) | D16 (RX2) |
| RX | Kuning | D3 (SoftwareSerial TX) | D17 (TX2) |
| EN (optional) | — | — | — |

## Diagram

```
Arduino UNO        HC-05 Bluetooth
┌──────┐           ┌────────────────┐
│ D2   ├──Hijau────┤ TX             │
│ D3   ├──Kuning───┤ RX             │
│ 5V   ├──Merah────┤ VCC            │
│ GND  ├──Hitam────┤ GND            │
└──────┘           └────────────────┘
```

## Catatan
- HC-05 = Bluetooth 2.0, bisa jadi master atau slave
- HC-06 = Bluetooth 2.0, slave only (lebih murah)
- Default baud: 9600 (HC-05) / 9600 (HC-06)
- Pair dengan PC/HP: PIN default 1234
- Untuk UNO: SoftwareSerial untuk komunikasi
- Jarak efektif: ~10 meter
