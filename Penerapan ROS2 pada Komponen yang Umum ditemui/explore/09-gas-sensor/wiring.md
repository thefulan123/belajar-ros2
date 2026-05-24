# Wiring: Gas Sensor (MQ-2 / MQ-135)

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 5V (via Vin) |
| GND | Hitam | GND | GND |
| AOUT (analog) | Kuning | A3 | GPIO35 |
| DOUT (digital) | — | — | — |

## Diagram

```
Arduino UNO        MQ-2 / MQ-135
┌──────┐           ┌────────────┐
│ A3   ├──Kuning───┤ AOUT       │
│      │           │            │
│ 5V   ├──Merah────┤ VCC        │
│      │           │            │
│ GND  ├──Hitam────┤ GND        │
└──────┘           └────────────┘
```

## Catatan
- MQ-2: mendeteksi LPG, Propane, Hydrogen, Methane, Smoke
- MQ-135: mendeteksi NH3, NOx, Alcohol, Benzene, Smoke, CO2
- Sensor perlu **warm-up 20-30 detik** sebelum data stabil
- Nilai analog berbanding terbalik dengan konsentrasi gas
- Output digital (DOUT) bisa diatur threshold via potensio di modul
