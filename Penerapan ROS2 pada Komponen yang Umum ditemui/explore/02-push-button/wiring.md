# Wiring: Push Button

## Koneksi

| Pin Komponen | Kabel | Arduino UNO | ESP32 |
|-------------|-------|-------------|-------|
| Button pin 1 | — | D4 (input) | D26 (input) |
| Button pin 2 | — | GND | GND |

## Diagram

```
Arduino UNO        Push Button
┌──────┐          ┌─────┐
│ D4   ├──────────┤  . .│
│      │          │     │
│ GND  ├──────────┤  . .│
└──────┘          └─────┘
```

## Catatan
- Pin pada board adalah **digital input dengan internal pull-up**
- Jadi LED pada board membaca HIGH saat button TIDAK ditekan, dan LOW saat ditekan
- Kalau ingin terbalik (LOW = tidak ditekan), gunakan external pull-down resistor 10kΩ
- Internal pull-up diaktifkan dengan `pinMode(pin, INPUT_PULLUP)`
