# Wiring: Load Cell + HX711

## Koneksi

| Pin HX711 | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| DT (data) | Kuning | D3 | D14 |
| SCK (clock) | Hijau | D2 | D12 |

| Load Cell | Warna Kabel | HX711 |
|-----------|-------------|-------|
| Red (E+) | Merah | E+ |
| Black (E-) | Hitam | E- |
| White (A-) | Putih | A- |
| Green (A+) | Hijau | A+ |

## Diagram

```
Arduino UNO        HX711           Load Cell
┌──────┐           ┌──────┐        ┌─────────┐
│ D2   ├──Hijau────┤ SCK  │        │         │
│ D3   ├──Kuning───┤ DT   │        │  Merah  ├──E+
│      │           │      │        │         │
│ 5V   ├──Merah────┤ VCC  │        │  Hitam  ├──E-
│      │           │      │        │         │
│ GND  ├──Hitam────┤ GND  ├──A+────┤  Hijau  │
└──────┘           │      │        │         │
                   │   A──┼──Putih─┤  Putih  │
                   └──────┘        └─────────┘
```

## Catatan
- Load Cell mengubah tekanan/berat menjadi perubahan resistansi (strain gauge)
- HX711 = ADC 24-bit khusus untuk load cell
- Butuh library: "HX711 Arduino Library" by Bogdan Necula
- Kalibrasi: ganti `KALIBRASI_FAKTOR` di code dengan hasil kalibrasi
- Berat maksimal tergantung load cell (biasanya 1kg, 5kg, 10kg, 20kg, 50kg)
- Gantung/letakkan beban di tengah load cell untuk akurasi terbaik
