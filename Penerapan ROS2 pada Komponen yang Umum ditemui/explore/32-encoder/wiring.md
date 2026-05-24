# Wiring: Rotary Encoder (KY-040)

## Koneksi

| Pin Encoder | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| CLK | Kuning | D2 (interrupt) | D14 |
| DT | Hijau | D3 (interrupt) | D27 |
| SW | Biru | D4 | D26 |
| + | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |

## Diagram

```
Arduino UNO        Rotary Encoder KY-040
┌──────┐           ┌──────────────────┐
│ D2   ├──Kuning───┤ CLK              │
│ D3   ├──Hijau────┤ DT               │
│ D4   ├──Biru─────┤ SW (button)      │
│ 5V   ├──Merah────┤ +                │
│ GND  ├──Hitam────┤ GND              │
└──────┘           └──────────────────┘
```

## Catatan
- Rotary encoder menghasilkan 2 sinyal (CLK, DT) — phase berbeda
- Arah putaran: CLK naik saat DT LOW = CW, DT HIGH = CCW
- SW = push button (LOW saat ditekan)
- Butuh debouncing — delay atau interrupt-based
- Untuk UNO: D2 dan D3 = pin interrupt
