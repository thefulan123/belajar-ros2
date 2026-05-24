# Wiring: Speaker (DFPlayer Mini)

## Koneksi

| Pin DFPlayer | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| VCC | Merah | 5V | 5V (Vin) |
| GND | Hitam | GND | GND |
| TX | Hijau | D2 (SoftwareSerial RX) | D16 (RX2) |
| RX | Kuning | D3 (SoftwareSerial TX) | D17 (TX2) |
| SPK_1 | — | — | Speaker (+) |
| SPK_2 | — | — | Speaker (-) |

## Diagram

```
Arduino UNO        DFPlayer Mini     Speaker 3W
┌──────┐           ┌────────────┐    ┌────────┐
│ D2   ├──Hijau────┤ TX         │    │        │
│ D3   ├──Kuning───┤ RX         │    │        │
│ 5V   ├──Merah────┤ VCC        ├────┤ (+)    │
│ GND  ├──Hitam────┤ GND        ├────┤ (-)    │
└──────┘           │ SPK_1 ─────┘    └────────┘
                   │ SPK_2 ─────┘
                   └────────────┘
```

## Catatan
- DFPlayer Mini = modul MP3 player via microSD card
- Butuh library: DFRobotDFPlayerMini atau DFMiniMp3
- microSD card harus diformat FAT16/FAT32
- File MP3 diberi nama: 0001.mp3, 0002.mp3, dst (di folder /mp3)
- Output speaker 3W (jangan pakai speaker > 3W tanpa amplifier)
- Atau bisa lewat headphone jack
