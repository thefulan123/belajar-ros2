# Wiring: LDR (Light Dependent Resistor)

## Koneksi

| Pin LDR | Kabel | Arduino UNO | ESP32 |
|---------|-------|-------------|-------|
| LDR kaki 1 | Merah | 5V | 3.3V |
| LDR kaki 2 | Kuning | A1 | GPIO39 |
| — | — | GND via 10kΩ resistor | GND via 10kΩ resistor |

Rangkaian: LDR + resistor 10kΩ membentuk **voltage divider**.

## Diagram

```
Arduino UNO
┌──────┐
│ 5V   ├──Merah────┐
│      │           │
│ A1   ├──Kuning───┤──┬── LDR ──┬── 5V
│      │           │  │         │
│ GND  ├──Hitam────┤  └──10kΩ───┘
└──────┘           │
                   └── GND
```

## Catatan
- LDR = resistor yang nilainya berubah sesuai cahaya
- Terang → resistansi rendah (R LDR kecil) → tegangan tinggi di A1
- Gelap → resistansi tinggi (R LDR besar) → tegangan rendah di A1
- Nilai LDR tanpa serial resistor 10kΩ tidak akan terbaca
