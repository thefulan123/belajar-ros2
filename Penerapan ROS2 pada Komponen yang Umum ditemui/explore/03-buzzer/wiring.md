# Wiring: Buzzer

## Koneksi

| Pin Buzzer | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| (+) positif | Merah → | D5 (PWM) | D27 (PWM) |
| (-) negatif | Hitam | GND | GND |

## Diagram

```
Arduino UNO        Buzzer
┌──────┐         ┌──────┐
│ D5   ├─────────┤ (+)  │
│      │         │      │
│ GND  ├─────────┤ (-)  │
└──────┘         └──────┘
```

## Catatan
- Buzzer active = langsung bunyi saat diberi HIGH
- Buzzer passive = perlu PWM untuk menghasilkan bunyi (nada berbeda)
- Kode ini mendukung **active buzzer** (dengan HIGH/LOW)
- Untuk passive buzzer, gunakan PWM dengan frekuensi berbeda (contoh: tone())
