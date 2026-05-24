# Wiring: Motor DC + Driver L298N

## Koneksi

| Pin L298N | Kabel | Arduino UNO | ESP32 |
|-----------|-------|-------------|-------|
| IN1 | Kuning | D7 | D32 |
| IN2 | Hijau | D6 | D33 |
| ENA (PWM) | Biru | D5 (PWM) | D25 |
| VCC (12V) | Merah | — | — |
| GND | Hitam | GND | GND |
| 5V output | — | (optional) | (optional) |

Power motor → baterai 9-12V ke VCC L298N
Power logika → dari Arduino 5V ke L298N (atau dari 5V output L298N)

| Pin Motor | Kabel | L298N |
|-----------|-------|-------|
| Motor + | — | OUT1 |
| Motor - | — | OUT2 |

## Diagram

```
Arduino UNO        L298N            Motor DC
┌──────┐           ┌────────┐       ┌──────┐
│ D5   ├──Biru─────┤ ENA    │       │      │
│ D6   ├──Hijau────┤ IN1    ├──OUT1─┤ (+)  │
│ D7   ├──Kuning───┤ IN2    ├──OUT2─┤ (-)  │
│      │           │        │       └──────┘
│ GND  ├──Hitam────┤ GND    │
└──────┘           │ VCC ──┬┤ 12V
                   └───────┘│
                            └─ Baterai 9-12V
```

## Catatan
- L298N butuh **2 sumber daya**: power motor (9-12V) + power logika (5V dari Arduino)
- **JANGAN** power L298N dari pin 5V Arduino — arus motor terlalu besar
- IN1 HIGH, IN2 LOW = motor maju
- IN1 LOW, IN2 HIGH = motor mundur
- IN1 LOW, IN2 LOW = motor stop (brake)
- ENA = PWM untuk kontrol kecepatan (0-255)
