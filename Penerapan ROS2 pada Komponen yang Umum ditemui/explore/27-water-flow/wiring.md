# Wiring: Water Flow Sensor (YF-S201)

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| Red (VCC) | Merah | 5V | 5V (Vin) |
| Black (GND) | Hitam | GND | GND |
| Yellow (Signal) | Kuning | D2 (interrupt) | D14 (interrupt) |

## Diagram

```
Arduino UNO        YF-S201
┌──────┐           ┌─────────┐
│ D2   ├──Kuning───┤ Signal  │
│      │           │         │
│ 5V   ├──Merah────┤ VCC     │
│      │           │         │
│ GND  ├──Hitam────┤ GND     │
└──────┘           └─────────┘
```

## Catatan
- YF-S201 = flow sensor berbasis hall effect
- Output: pulse (setiap putaran kincir = ~2.25 mL air)
- Frekuensi pulse ~ 7.5 Hz per L/min
- Rumus: Flow (L/min) = pulse_freq / 7.5
- Untuk UNO: D2 dan D3 adalah satu-satunya pin interrupt
- JANGAN alirkan air panas > 80°C
- Sensor TIDAK untuk air minum (contain lead/tin solder)
