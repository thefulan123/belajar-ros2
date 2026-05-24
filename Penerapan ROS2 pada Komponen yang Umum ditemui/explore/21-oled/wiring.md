# Wiring: OLED SSD1306 (I2C)

## Koneksi

| Pin OLED | Kabel | Arduino UNO | ESP32 |
|----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| SCL | Biru | A5 (SCL) | D22 |
| SDA | Hijau | A4 (SDA) | D21 |

## Diagram

```
Arduino UNO        OLED 128x64
┌──────┐           ┌───────────┐
│ A4   ├──Hijau────┤ SDA       │
│      │           │           │
│ A5   ├──Biru─────┤ SCL       │
│      │           │           │
│ 5V   ├──Merah────┤ VCC       │
│      │           │           │
│ GND  ├──Hitam────┤ GND       │
└──────┘           └───────────┘
```

## Catatan
- OLED 128x64 = 128 pixel x 64 pixel
- Alamat I2C default: 0x3C
- Butuh library: "Adafruit SSD1306" + "Adafruit GFX"
- OLED tidak perlu backlight — pixel sendiri yang menyala
- Konsumsi daya sangat rendah (~20mA)
- Support grafik: garis, lingkaran, teks, bitmap
