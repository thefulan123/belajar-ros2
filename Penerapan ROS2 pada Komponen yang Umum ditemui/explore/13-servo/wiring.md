# Wiring: Servo Motor (SG90 / MG995)

## Koneksi

| Pin Servo | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| Orange (Signal) | Kuning | D9 | D13 |
| Red (VCC) | Merah | 5V | 5V (Vin) |
| Brown (GND) | Hitam | GND | GND |

## Diagram

```
Arduino UNO        Servo SG90
┌──────┐           ┌─────────┐
│ D9   ├──Kuning───┤ Orange  │
│      │           │ (Signal)│
│ 5V   ├──Merah────┤ Red     │
│      │           │ (VCC)   │
│ GND  ├──Hitam────┤ Brown   │
└──────┘           │ (GND)   │
                   └─────────┘
```

## Catatan
- **SG90:** 5V, 0.12s/60°, ~200mA — cocok untuk robot kecil
- **MG995:** 5-7.4V, 0.17s/60°, ~900mA — butuh power eksternal untuk beban berat
- Untuk MG995/MG996: jangan pakai power dari pin 5V Arduino — arus terlalu besar
- Servo dikontrol via PWM: pulsa 1ms = 0°, 1.5ms = 90°, 2ms = 180°
- Sudut dibatasi 0° - 180° (fisik)
