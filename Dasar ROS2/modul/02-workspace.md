# MODUL 02: Workspace

**TAG:** infrastruktur / organisasi / build

---

## APA ITU WORKSPACE?

Workspace adalah folder utama tempat kamu mengerjakan proyek ROS2.

Strukturnya:
```
nama_workspace/
└── src/              ← tempat semua package ROS2
```

Contoh:
```
ros2_ws/
└── src/
    ├── package_1/
    ├── package_2/
    └── package_3/
```

Nama workspace bebas. Yang penting struktur `src/` di dalamnya.

---

## KENAPA ADA?

### Masalah

Bayangkan kamu punya 10 node ROS2. Tanpa workspace:

```
Desktop/
├── node_sensor.py
├── node_motor.py
├── node_kamera.py
├── node_navigasi.py
├── ...
```

Berantakan. Tidak jelas mana yang satu proyek. Sulit di-share ke orang lain.

### Solusi

Workspace mengelompokkan semua package yang saling berhubungan ke dalam satu folder.

---

## CARA KERJA

```
ros2_ws/              ← root workspace
└── src/              ← tempat source code
    ├── package_a/
    │   ├── package.xml
    │   ├── setup.py
    │   └── ...
    └── package_b/
        ├── package.xml
        ├── setup.py
        └── ...

(setelah build, folder baru muncul:)

ros2_ws/
├── src/              ← source code (kamu yang buat)
├── build/            ← file sementara saat build (otomatis)
├── install/          ← hasil build siap pakai (otomatis)
└── log/              ← catatan proses build (otomatis)
```

| Folder | Dibuat oleh | Fungsi |
|--------|-------------|--------|
| `src/` | Kamu | Tempat kode sumber |
| `build/` | colcon | File sementara saat kompilasi |
| `install/` | colcon | Hasil build (siap di-source) |
| `log/` | colcon | Catatan proses build |

---

## CONTOH

```bash
# 1. Buat workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# 2. Lihat struktur
ls
# Output: src/

# 3. Nanti setelah ada package:
ls src/
# Output: package_ku/
```

---

## COBA INI

**Eksperimen — Buat workspace pertama:**

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
ls -la
```

Lihat folder `src/` sudah ada. Workspace siap.

**Eksperimen — Cek folder muncul setelah build (nanti):**

Setelah Modul 05 (Build Package), folder `build/`, `install/`, `log/` akan muncul otomatis.

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `workspace tidak ditemukan` | Salah folder | Pastikan `cd` ke folder workspace |
| `package 'xxx' not found` | Workspace belum di-source | `source install/setup.bash` |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 01** — Sourcing: cara mengaktifkan ROS2
- **Lanjut ke Modul 03** — Package: apa yang ada di dalam `src/`
- **Lanjut ke Modul 05** — Build: cara mengubah `src/` menjadi `install/`
- **Lanjut ke Modul 06** — Source Workspace: kenapa harus source ulang
