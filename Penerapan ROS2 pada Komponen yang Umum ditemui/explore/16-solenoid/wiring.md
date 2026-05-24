# Wiring: Solenoid Lock / Solenoid Valve

## Koneksi (via Relay)

| Pin Relay | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| IN | Kuning | D6 | D33 |
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |

| Pin Relay | Kabel | Solenoid |
|-----------|-------|----------|
| COM | — | Power supply 12V (+) |
| NO | — | Solenoid (+) |
| — | — | Solenoid (-) → GND power supply |

## Diagram

```
Arduino UNO          Relay Module       Power 12V       Solenoid
┌──────┐             ┌──────────┐      ┌──────┐        ┌────────┐
│ D6   ├──Kuning─────┤ IN       │      │      │        │        │
│      │             │          │      │  +  ├────────┤ (+)    │
│ 5V   ├──Merah──────┤ VCC      │      │     │        │        │
│      │             │          ├──────┤  -  ├────────┤ (-)    │
│ GND  ├──Hitam──────┤ GND      │      └──────┘        └────────┘
└──────┘             └──────────┘
```

## Catatan
- **Solenoid 12V** — jangan langsung dari Arduino
- Solenoid butuh arus besar (~1-2A) — WAJIB pakai relay atau MOSFET
- Solenoid lock = door lock (dorong/ tarik)
- Solenoid valve = katup air/udara (buka/tutup)
- Dioda flyback WAJIB dipasang paralel dengan solenoid (katoda ke +) jika pakai MOSFET
- Dengan relay module, dioda flyback sudah include
