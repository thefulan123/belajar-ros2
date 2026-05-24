# Wiring: NeoPixel WS2812B

## Koneksi

| Pin NeoPixel | Kabel | Arduino UNO | ESP32 |
|--------------|-------|-------------|-------|
| VCC (5V) | Merah | 5V | 5V (Vin) |
| GND | Hitam | GND | GND |
| DIN (data) | Kuning | D6 | D14 |

## Diagram

```
Arduino UNO        NeoPixel Strip
┌──────┐           ┌──────────────┐
│ D6   ├──Kuning───┤ DIN          │
│      │           │              │
│ 5V   ├──Merah────┤ VCC (5V)     │
│      │           │              │
│ GND  ├──Hitam────┤ GND          │
└──────┘           └──────────────┘
```

## Catatan
- NeoPixel = LED RGB addressable (WS2812B)
- Setiap LED punya IC sendiri — semua LED bisa warna berbeda
- Butuh library: Adafruit NeoPixel
- Untuk strip panjang (> 30 LED), butuh power eksternal 5V
- Kapasitor 1000μF antara VCC dan GND untuk stabilisasi power
- Resistor 300-500Ω pada DIN untuk mencegah noise
- 5V logic untuk UNO, pastikan ESP32 pin 14 kompatibel (3.3V → 5V level shifter jika perlu)
