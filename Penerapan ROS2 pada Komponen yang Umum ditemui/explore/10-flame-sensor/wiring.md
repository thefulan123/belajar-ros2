# Wiring: Flame Sensor

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| DOUT (digital) | Kuning | D8 | D14 |
| AOUT (analog) | — | — | — |

## Diagram

```
Arduino UNO        Flame Sensor
┌──────┐           ┌────────────┐
│ D8   ├──Kuning───┤ DOUT       │
│      │           │            │
│ 5V   ├──Merah────┤ VCC        │
│      │           │            │
│ GND  ├──Hitam────┤ GND        │
└──────┘           └────────────┘
```

## Catatan
- Spektrum inframerah: 760nm - 1100nm
- Jangkauan deteksi: ~30-100 cm tergantung ukuran api
- DOUT: LOW = api terdeteksi, HIGH = tidak ada api
- Sensor ini sensitif terhadap cahaya matahari langsung
- Jangan dekatkan api terlalu dekat (< 10 cm) — bisa merusak sensor
