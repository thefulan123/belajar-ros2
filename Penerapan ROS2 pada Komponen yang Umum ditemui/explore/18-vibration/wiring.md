# Wiring: Vibration Motor Module

## Koneksi

| Pin Modul | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| SIG (signal) | Kuning | D10 | D15 (PWM) |

## Diagram

```
Arduino UNO        Vibration Motor
┌──────┐           ┌────────────────┐
│ D10  ├──Kuning───┤ SIG            │
│      │           │                │
│ 5V   ├──Merah────┤ VCC            │
│      │           │                │
│ GND  ├──Hitam────┤ GND            │
└──────┘           └────────────────┘
```

## Catatan
- Vibration motor = motor DC kecil dengan pemberat tidak seimbang
- Getaran sebanding dengan tegangan (PWM)
- Untuk module siap pakai: langsung colok VCC/GND/SIG
- Untuk motor vibration bare (tanpa module): butuh transistor driver
- Module vibration biasanya pakai transistor built-in
