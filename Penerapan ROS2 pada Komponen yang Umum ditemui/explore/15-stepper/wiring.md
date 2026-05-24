# Wiring: Stepper Motor 28BYJ-48 + Driver ULN2003

## Koneksi

| Pin ULN2003 | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| IN1 (Blue) | Biru | D8 | D14 |
| IN2 (Pink) | Merah Muda | D9 | D27 |
| IN3 (Yellow) | Kuning | D10 | D26 |
| IN4 (Orange) | Orange | D11 | D25 |
| GND | Hitam | GND | GND |
| VCC | Merah | 5V | 5V (Vin) |

## Diagram

```
Arduino UNO        ULN2003        28BYJ-48
┌──────┐          ┌────────┐     ┌─────────┐
│ D8   ├──Biru────┤ IN1    │     │         │
│      │          │        ├─────┤         │
│ D9   ├──Pink────┤ IN2    │     │ Stepper │
│      │          │        ├─────┤ Motor   │
│ D10  ├──Kuning──┤ IN3    │     │         │
│      │          │        ├─────┤         │
│ D11  ├──Orange──┤ IN4    │     │         │
│      │          │        │     └─────────┘
│ 5V   ├──Merah───┤ VCC    │
│ GND  ├──Hitam───┤ GND    │
└──────┘          └────────┘
```

## Catatan
- 28BYJ-48 = stepper 5V, 4-phase, gear ratio 64:1
- 2048 steps per revolution (dengan gearbox)
- Sudut per step: ~0.176° (dengan gearbox)
- Driver ULN2003 sudah include di paket 28BYJ-48
- Stepper ini butuh arus ~200-300mA — aman dari pin 5V Arduino
- Untuk ESP32: pin 25, 26, 27, 14 — pilih pin yang tidak dipakai ADC2
