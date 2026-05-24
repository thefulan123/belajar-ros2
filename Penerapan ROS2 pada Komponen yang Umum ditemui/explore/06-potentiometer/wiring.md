# Wiring: Potensiometer

## Koneksi

| Pin Potensio | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| Kiri (GND) | Hitam | GND | GND |
| Tengah (Wiper) | Kuning | A0 | GPIO36 (ADC) |
| Kanan (VCC) | Merah | 5V | 3.3V |

## Diagram

```
Arduino UNO        Potensiometer 10kΩ
┌──────┐            ┌─────┐
│ A0   ├──Kuning────┤     │
│      │            │  .  │
│ 5V   ├──Merah─────┤  .  │
│      │            │     │
│ GND  ├──Hitam─────┤  .  │
└──────┘            └─────┘
```

## Catatan
- Potensiometer = voltage divider
- Wiper bergerak dari 0V (GND) ke VCC
- Arduino UNO: ADC 10-bit → nilai 0 - 1023
- ESP32: ADC 12-bit → nilai 0 - 4095
- Untuk ESP32 pin ADC: GPIO32-39 (khusus ADC1)
- Output dipublish sebagai Int32 (0-100 untuk persentase)
