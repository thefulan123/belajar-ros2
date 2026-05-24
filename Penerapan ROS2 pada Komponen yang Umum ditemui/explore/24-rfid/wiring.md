# Wiring: RFID RC522

## Koneksi (SPI)

| Pin RC522 | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| SDA (SS) | Abu-abu | D10 | D5 |
| SCK | Biru | D13 | D18 |
| MOSI | Hijau | D11 | D23 |
| MISO | Kuning | D12 | D19 |
| IRQ | — | — | — |
| GND | Hitam | GND | GND |
| RST | Putih | D9 | D4 |
| 3.3V | Merah | 3.3V | 3.3V |

## Diagram

```
Arduino UNO        RC522 RFID
┌──────┐           ┌───────────┐
│ D9   ├──Putih────┤ RST       │
│ D10  ├──Abu──────┤ SDA (SS)  │
│ D11  ├──Hijau────┤ MOSI      │
│ D12  ├──Kuning───┤ MISO      │
│ D13  ├──Biru─────┤ SCK       │
│      │           │           │
│ 3.3V ├──Merah────┤ 3.3V      │
│ GND  ├──Hitam────┤ GND       │
└──────┘           └───────────┘
```

## Catatan
- RC522 = RFID Reader 13.56MHz
- Komunikasi via **SPI** (Serial Peripheral Interface)
- Butuh library: "MFRC522" by GithubCommunity
- Jarak baca: ~2-5 cm (tergantung tag/antena)
- Support tag: Mifare (Classic 1K/4K, Ultralight, Desfire)
- **RC522 adalah 3.3V device** — JANGAN colok ke 5V!
- RC522 butuh arus ~30mA — aman dari pin 3.3V Arduino
