# Wiring: LCD 16x2 I2C

## Koneksi

| Pin LCD I2C | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| VCC | Merah | 5V | 5V (Vin) |
| GND | Hitam | GND | GND |
| SDA | Hijau | A4 (SDA) | D21 |
| SCL | Biru | A5 (SCL) | D22 |

## Diagram

```
Arduino UNO        LCD I2C Backpack
┌──────┐           ┌────────────────┐
│ A4   ├──Hijau────┤ SDA            │
│      │           │                │
│ A5   ├──Biru─────┤ SCL            │
│      │           │                │
│ 5V   ├──Merah────┤ VCC            │
│      │           │                │
│ GND  ├──Hitam────┤ GND            │
└──────┘           └────────────────┘
```

## Catatan
- LCD 16x2 I2C = 16 karakter x 2 baris
- Alamat I2C default: 0x27 (atau 0x3F untuk beberapa module)
- Butuh library: LiquidCrystal I2C by Frank de Brabander
- Potensio di belakang LCD untuk kontras (putar pelan sampai tulisan jelas)
- LCD 16x2 bisa nampilin 32 karakter total (16x2)
