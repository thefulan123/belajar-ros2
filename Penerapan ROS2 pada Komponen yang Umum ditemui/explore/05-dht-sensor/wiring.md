# Wiring: DHT11 / DHT22

## Koneksi

| Pin DHT | Kabel | Arduino UNO | ESP32 |
|---------|-------|-------------|-------|
| VCC (pin 1) | Merah | 5V | 3.3V |
| DATA (pin 2) | Kuning | D7 | D32 |
| NC (pin 3) | — | — | — |
| GND (pin 4) | Hitam | GND | GND |

**PERHATIAN:** Pasang resistor pull-up 4.7kΩ - 10kΩ antara VCC dan DATA.

## Diagram

```
Arduino UNO        DHT11
┌──────┐         ┌──────┐
│ 5V   ├──Merah──┤ VCC  │
│      │         │      │
│ D7   ├──Kuning─┤ DATA │
│      │   │     │      │
│      │  ┌┴┐    │      │
│      │  │4k7Ω  │      │
│      │  └┬┘    │      │
│      │   │     │      │
│ GND  ├──Hitam──┤ GND  │
└──────┘         └──────┘
```

## Catatan
- DHT11: akurasi ±2°C, range 0-50°C, update max 1 Hz
- DHT22: akurasi ±0.5°C, range -40°C - 80°C, lebih akurat
- WAJIB ada resistor 4.7kΩ - 10kΩ antara VCC dan DATA
- Kalau tidak ada resistor, data tidak terbaca (timeout error)
- Jika error terus, coba ganti pin atau pakai DHT sensor library versi 1.4.4
