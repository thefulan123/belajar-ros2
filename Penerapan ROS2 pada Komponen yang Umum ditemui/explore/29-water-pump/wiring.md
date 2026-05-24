# Wiring: Water Pump (via Relay)

## Koneksi

### Control (Arduino → Relay)
| Pin Relay | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| IN | Kuning | D6 | D33 |
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |

### Power (Relay → Pump)
| Pin Relay | Kabel | Power Supply |
|-----------|-------|-------------|
| COM | — | 12V (+) |
| NO | — | Pompa (+) |
| — | — | Pompa (-) → 12V GND |

## Diagram

```
Arduino UNO     Relay          Power 12V      Pompa Air
┌──────┐        ┌────────┐     ┌──────┐      ┌─────────┐
│ D6   ├─Kuning─┤ IN     │     │      │      │         │
│ 5V   ├─Merah──┤ VCC    │     │  +   ├──────┤ (+)     │
│ GND  ├─Hitam──┤ GND    │     │      │      │         │
└──────┘        │ COM ───┼─────┤  -   ├──────┤ (-)     │
                │ NO  ───┼─────┤      │      │         │
                └────────┘     └──────┘      └─────────┘
```

## Catatan
- Pompa air DC mini (3-12V) atau pompa AC — keduanya WAJIB relay
- Arus pompa biasanya 0.5-3A — jangan langsung dari Arduino
- Pompa air = induktif — pasang dioda flyback jika pakai MOSFET
- Relay module 5V sudah include optocoupler + driver
- JANGAN nyalakan pompa tanpa air di dalamnya (running dry = rusak)
