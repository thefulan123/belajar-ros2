# Wiring: Rain Sensor Module

## Koneksi

| Pin Modul | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 5V (Vin) |
| GND | Hitam | GND | GND |
| DO (digital) | Kuning | D4 | D14 |
| AO (analog) | — | — | — |

## Diagram

```
Arduino UNO        Rain Sensor Module
┌──────┐           ┌──────────────────┐
│ D4   ├──Kuning───┤ DO (digital out) │
│      │           │                  │
│ 5V   ├──Merah────┤ VCC              │
│      │           │                  │
│ GND  ├──Hitam────┤ GND              │
└──────┘           └──────────────────┘
```

## Catatan
- Sensor mendeteksi air di permukaan PCB
- DO: LOW = hujan/air terdeteksi, HIGH = kering
- AO: nilai analog (semakin basah, tegangan semakin tinggi)
- Ada potensio untuk adjust threshold digital
- PCB sensor bisa korosi — bersihkan dan keringkan setelah dipakai
- Jangan colok ke air terus-menerus (electrolysis merusak PCB)
