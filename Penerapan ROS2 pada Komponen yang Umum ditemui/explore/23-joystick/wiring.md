# Wiring: Joystick Module (KY-023)

## Koneksi

| Pin Joystick | Kabel | Arduino UNO | ESP32 |
|--------------|-------|-------------|-------|
| GND | Hitam | GND | GND |
| +5V | Merah | 5V | 3.3V |
| VRx | Kuning | A0 | GPIO36 |
| VRy | Hijau | A1 | GPIO39 |
| SW | Biru | D4 (input) | D26 |

## Diagram

```
Arduino UNO        Joystick KY-023
┌──────┐           ┌──────────────┐
│ A0   ├──Kuning───┤ VRx          │
│ A1   ├──Hijau────┤ VRy          │
│ D4   ├──Biru─────┤ SW (button)  │
│ 5V   ├──Merah────┤ +5V          │
│ GND  ├──Hitam────┤ GND          │
└──────┘           └──────────────┘
```

## Catatan
- Joystick = 2 potensiometer (X, Y) + 1 push button (Z)
- VRx = horizontal (kiri=0, tengah=~512, kanan=1023)
- VRy = vertikal (atas=0, tengah=~512, bawah=1023)
- SW = push button (LOW when pressed, with INPUT_PULLUP)
- Untuk ESP32: pin ADC2 (GPIO 25, 26, 27, 14) tidak bisa dipakai saat WiFi aktif
- Gunakan ADC1 (GPIO 32-39) untuk ESP32
