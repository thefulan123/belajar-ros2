# AGENTS.md — Penerapan ROS2 pada Komponen

Aturan khusus untuk folder ini.

## Struktur

```
Penerapan ROS2 pada Komponen yang Umum Ditemui/
├── referensi/                 ← Panduan instalasi, daftar komponen, wiring
├── explore/01-38/             ← Setiap komponen = 1 folder (01-led, 02-push-button, ...)
│   ├── *.ino                  ← micro-ROS sketch (nama_komponen.ino)
│   ├── *_node.py              ← (opsional) PC-side Python node
│   ├── wiring.md              ← Tabel koneksi pin + diagram
│   └── README.md              ← Cara jalankan + konsep ROS2
├── docs/
│   ├── disclaimer.md
│   └── ERRORS.md
├── logs/
├── AGENTS.md
└── README.md
```

## Aturan

1. **Setiap explore/ harus bisa standalone** — jalankan sendiri tanpa dependensi folder lain
2. **micro-ROS hanya support Arduino UNO + ESP32** — jangan gunakan board lain tanpa testing
3. **Serial baud ratem WAJIB 115200** — konsisten di semua sketch
4. **Setiap sketch harus punya error handling** — minimal serial print error
5. **Wiring.md harus ada di setiap explore/** — tabel pinout, bukan gambar
6. **Topic naming** — `/nama_komponen` contoh: `/led`, `/servo`, `/suhu`

## Dual Board Support

Setiap sketch mendukung 2 board:
- Arduino UNO (micro-ROS via Serial)
- ESP32 (micro-ROS via WiFi)

## Hubungan dengan Dasar ROS2/

Proyek ini adalah **lanjutan praktik** dari [Modul 11 — micro-ROS](../../Dasar%20ROS2/modul/11-micro-ros.md).
Semua konsep (node, topic, pub/sub, callback) sudah dipelajari di Dasar ROS2/.


## Modul Dasar ROS2 Terkait

Setiap komponen di explore/ menggunakan konsep dari modul-modul berikut:

| Modul Dasar ROS2 | Relevansi dengan Penerapan |
|:---|:---|
| [Modul 03 — Node](../Dasar%20ROS2/modul/03-node.md) | Setiap `.ino` adalah ROS2 node |
| [Modul 04 — Topic](../Dasar%20ROS2/modul/04-topic-pub-sub.md) | Semua komunikasi via topic pub/sub |
| [Modul 10 — Callback & Timer](../Dasar%20ROS2/modul/10-callback-timer.md) | Setiap `.ino` punya callback + timer |
| [Modul 11 — micro-ROS](../Dasar%20ROS2/modul/11-micro-ros.md) | Teknologi inti: ROS2 di Arduino/ESP32 |

> **Catatan:** Lihat [KORELASI.md](../Dasar%20ROS2/docs/KORELASI.md) untuk mapping lengkap modul ↔ komponen.
