# Wiring: Sound Sensor (KY-038 / MAX9814)

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| AOUT (analog) | Kuning | A0 | GPIO36 |
| DOUT (digital) | — | — | — |

## Diagram

```
Arduino UNO        Sound Sensor KY-038
┌──────┐           ┌────────────────┐
│ A0   ├──Kuning───┤ AOUT (analog)  │
│      │           │                │
│ 5V   ├──Merah────┤ VCC            │
│      │           │                │
│ GND  ├──Hitam────┤ GND            │
└──────┘           └────────────────┘
```

## Catatan
- KY-038: sensor suara berbasis electret microphone + LM393 comparator
- AOUT: tegangan proporsional dengan intensitas suara
- DOUT: HIGH/LOW (threshold diatur potensio di modul)
- Untuk UNO: output analog 0-1023 (10-bit)
- Untuk ESP32: output 0-4095 (12-bit)
- Nilai tanpa suara ≠ 0 — ada noise ambient
