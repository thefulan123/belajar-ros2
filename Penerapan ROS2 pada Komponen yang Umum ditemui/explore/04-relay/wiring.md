# Wiring: Relay Module

## Koneksi

| Pin Relay | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V / Vin |
| GND | Hitam | GND | GND |
| IN (signal) | Kuning | D6 | D33 |
| COM | — | — | Perangkat eksternal |
| NO (Normally Open) | — | — | Perangkat eksternal |
| NC (Normally Closed) | — | — | (tidak dipakai) |

## Diagram

```
Arduino UNO          Relay (2-channel)
┌──────┐           ┌──────────────┐
│ D6   ├──Kuning───┤ IN1          │
│      │           │              │
│ 5V   ├──Merah────┤ VCC          │
│      │           │              │
│ GND  ├──Hitam────┤ GND          │
└──────┘           └──────┬───────┘
                          │
                     ┌────┴────┐
                     │ COM  NO │
                     └────┬────┘
                          │
                     ┌────┴────┐
                     │ Lampu   │
                     │ AC 220V │
                     └─────────┘
```

## Catatan
- Relay untuk saklar **arus besar** (lampu, pompa, motor AC)
- JANGAN hubungkan perangkat AC langsung ke Arduino
- `HIGH` pada IN = relay aktif (COM terhubung ke NO)
- `LOW` pada IN = relay nonaktif (COM terhubung ke NC)
- Relay butuh arus lebih besar dari pin biasa — module relay sudah include driver transistor
