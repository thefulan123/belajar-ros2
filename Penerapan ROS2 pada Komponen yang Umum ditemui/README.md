# Penerapan ROS2 pada Komponen yang Umum Ditemui

Proyek ini berisi **38+ proyek praktik** menghubungkan komponen elektronik umum ke ROS2 menggunakan **micro-ROS** (Arduino UNO / ESP32).

---

## Prasyarat

Sebelum memulai, pastikan sudah menyelesaikan atau paham:

1. **Dasar ROS2/** — Node, Topic, Publisher, Subscriber, Callback
2. **Modul 08 — micro-ROS Arduino** — Teori micro-ROS dan instalasi
3. **Referensi/00 — Software Requirements** — Semua software terinstall

---

## Cara Pakai

### 1. Pilih komponen
Cari folder komponen di `explore/XX-nama-komponen/`

### 2. Baca wiring
Setiap folder punya `wiring.md` — tabel koneksi pin

### 3. Upload sketch
```bash
Buka .ino di Arduino IDE
Pilih board: Arduino UNO (atau ESP32)
Upload
```

### 4. Jalankan micro-ROS Agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek di ROS2
```bash
ros2 topic list
ros2 topic echo /nama_topic
```

---

## Starter Pack (Minimal)

| Item | Estimasi |
|------|----------|
| Arduino UNO R3 | Rp 60k |
| Breadboard + Jumper | Rp 25k |
| 5x LED + Resistor | Rp 5k |
| Push Button | Rp 2k |
| Potensiometer | Rp 5k |
| Buzzer | Rp 3k |
| DHT11 | Rp 10k |
| **Total** | **~Rp 110k** |

Dengan ini bisa menjalankan explore/01 sampai explore/06.

---

## Daftar Isi

### Referensi
- [00 — Software Requirements](referensi/00-software-requirements.md)
- [01 — Daftar Komponen](referensi/01-daftar-komponen.md)
- [02 — Klasifikasi Peran ROS2](referensi/02-klasifikasi-peran-ros2.md)
- [03 — Panduan Wiring Dasar](referensi/03-panduan-wiring-dasar.md)

### Error & Disclaimer
- [ERRORS.md](docs/ERRORS.md)
- [Disclaimer](docs/disclaimer.md)
