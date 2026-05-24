# Wiring: GPS NEO-6M / NEO-8M

## Koneksi (UART)

| Pin GPS | Kabel | Arduino UNO | ESP32 |
|---------|-------|-------------|-------|
| VCC | Merah | 5V | 3.3V |
| GND | Hitam | GND | GND |
| TX | Hijau | D2 (SoftwareSerial RX) | D16 (RX2) |
| RX | Kuning | D3 (SoftwareSerial TX) | D17 (TX2) |

## Diagram

```
Arduino UNO        GPS NEO-6M
┌──────┐           ┌───────────┐
│ D2   ├──Hijau────┤ TX        │
│ D3   ├──Kuning───┤ RX        │
│ 5V   ├──Merah────┤ VCC       │
│ GND  ├──Hitam────┤ GND       │
└──────┘           └───────────┘
```

## Catatan
- GPS butuh **view langit terbuka** — tidak akan fix di dalam ruangan
- Butuh library: "TinyGPSPlus" by Mikal Hart
- Waktu fix pertama (TTFF): 30-60 detik (cold start)
- NEO-6M: 50 channel, update 1 Hz (5 Hz jika pakai binary mode)
- NEO-8M: lebih sensitif, update 10 Hz
- Antena GPS harus menghadap ke atas
- LED pada modul: blink = cari sinyal, solid = sudah fix
