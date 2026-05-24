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

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie cukup punya **1 folder** berisi file `.ino`. Di ROS2, workspace punya struktur baku.

| Aspek | ROS2 | Arduino Biasa |
|-------|------|---------------|
| Struktur | `workspace/src/` → build → install/ | 1 folder, 1 file `.ino` |
| Organisasi | Package → node → topic/service | `#include` + `setup()` + `loop()` |
| Scalability | Puluhan node dalam 1 workspace | 1 program = 1 file (ribet kalau besar) |
| Build | `colcon build` → compile semua package | Ctrl+R → compile 1 file |
| Analogi | Seperti proyek VS Code dengan banyak folder | Seperti notepad — simpel tapi terbatas |

**Intinya:** Workspace ROS2 agak ribet di awal, tapi begitu proyekmu punya 5+ sensor dan 3+ aktuator, struktur ini menyelamatkanmu dari kekacauan.

---

## 📁 PRAKTIK

Praktik ini membuat **ROS2 workspace** pertama kamu.

### Langkah 1: Buka terminal
Buka terminal baru.

### Langkah 2: Source ROS2
```bash
source /opt/ros/humble/setup.bash
```

### Langkah 3: Buat folder workspace
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### Langkah 4: Lihat struktur workspace
```bash
ls -la
```

**Output yang diharapkan:**
```
total ...
drwxr-xr-x ... .
drwxr-xr-x ... ..
drwxr-xr-x ... src
```

Folder `src/` adalah tempat semua package ROS2 akan disimpan.

### Langkah 5: Cek path absolut workspace
```bash
pwd
```

**Output yang diharapkan:**
```
/home/nama_user/ros2_ws
```

**Kesimpulan:** Workspace `~/ros2_ws/src/` sudah siap diisi dengan package ROS2.
