# Wiring: PIR Motion Sensor (HC-SR501)

## Koneksi

| Pin Sensor | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 5V (via Vin) |
| OUT | Kuning | D9 | D12 |
| GND | Hitam | GND | GND |

## Diagram

```
Arduino UNO        PIR HC-SR501
┌──────┐           ┌────────────┐
│ D9   ├──Kuning───┤ OUT        │
│      │           │            │
│ 5V   ├──Merah────┤ VCC        │
│      │           │            │
│ GND  ├──Hitam────┤ GND        │
└──────┘           └────────────┘
```

## Catatan
- PIR mendeteksi **perubahan** suhu (gerakan tubuh manusia/hewan)
- Sensor butuh **stabilisasi 30-60 detik** setelah power ON
- Saat stabilisasi, output bisa HIGH-LOW acak — ini normal
- Jangkauan: ~3-7 meter, sudut deteksi ~120°
- Ada 2 potensio di modul: sensitivitas (jarak) dan waktu (delay output)
- Output: HIGH = gerakan terdeteksi, LOW = tidak ada gerakan
