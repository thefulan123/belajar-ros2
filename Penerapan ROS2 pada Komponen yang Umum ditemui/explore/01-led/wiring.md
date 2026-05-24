# Wiring: LED

## Koneksi

| Pin LED | Kabel | Arduino UNO | ESP32 |
|---------|-------|-------------|-------|
| Anode (+) | Merah → 220Ω → | D3 (PWM) | D25 (PWM) |
| Cathode (-) | Hitam | GND | GND |

## Diagram

```
Arduino UNO       220Ω        LED
┌──────┐       ┌──────┐    ┌──────┐
│ D3   ├──/\/\/──────┤ (+) │
│      │               │     │
│ GND  ├───────────────┤ (-) │
└──────┘               └──────┘
```

## Catatan
- LED (+) = kaki panjang (anoda)
- LED (-) = kaki pendek (katoda)
- Resistor 220Ω WAJIB, tanpa resistor LED bisa rusak
- Gunakan pin PWM (~) untuk efek brightness
