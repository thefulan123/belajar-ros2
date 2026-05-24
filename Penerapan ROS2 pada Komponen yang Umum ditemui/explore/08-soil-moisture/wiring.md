# Wiring: Soil Moisture Sensor

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| AOUT (analog) | Kuning | A2 | GPIO34 |

## Diagram

```
Arduino UNO        Soil Moisture Sensor
┌──────┐           ┌─────────────────┐
│ A2   ├──Kuning───┤ AOUT            │
│      │           │                 │
│ 5V   ├──Merah────┤ VCC             │
│      │           │                 │
│ GND  ├──Hitam────┤ GND             │
└──────┘           └─────────────────┘
```

## Catatan
- Sensor ini mengukur konduktivitas listrik tanah
- Tanah kering → konduktivitas rendah → tegangan rendah
- Tanah basah → konduktivitas tinggi → tegangan tinggi
- JANGAN colok sensor ke tanah kering terlalu lama — bisa korosi
- Output analog: 0 (kering) - maks (basah)
