# Wiring: Keypad 4x4 Matrix

## Koneksi

| Keypad Pin | Kabel | Arduino UNO | ESP32 |
|------------|-------|-------------|-------|
| R1 (row 1) | — | D7 | D13 |
| R2 (row 2) | — | D6 | D12 |
| R3 (row 3) | — | D5 | D14 |
| R4 (row 4) | — | D4 | D27 |
| C1 (col 1) | — | D3 | D26 |
| C2 (col 2) | — | D2 | D25 |
| C3 (col 3) | — | D1 | D33 |
| C4 (col 4) | — | D0 | D32 |

## Diagram

```
Arduino UNO        Keypad 4x4
┌──────┐           ┌─────────────┐
│ D7   ├───────────┤ R1          │
│ D6   ├───────────┤ R2          │
│ D5   ├───────────┤ R3          │
│ D4   ├───────────┤ R4          │
│ D3   ├───────────┤ C1          │
│ D2   ├───────────┤ C2          │
│ D1   ├───────────┤ C3          │
│ D0   ├───────────┤ C4          │
└──────┘           └─────────────┘
```

## Catatan
- Keypad 4x4 = 16 tombol (0-9, A-D, *, #)
- Matriks: 4 baris (rows) + 4 kolom (columns)
- Butuh library: "Keypad" by Mark Stanley
- Cara kerja: Arduino scan tiap row → baca column → dapat tombol
- Debouncing sudah include di library Keypad
