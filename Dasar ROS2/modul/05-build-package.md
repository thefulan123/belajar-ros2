# MODUL 05: Build Package

**TAG:** build / kompilasi / colcon

---

## APA ITU BUILD?

Build adalah proses mengubah kode sumber menjadi file yang siap dijalankan.

Perintah:
```bash
cd ~/ros2_ws
colcon build
```

---

## KENAPA ADA?

### Masalah

Kode Python (.py) sebenarnya bisa langsung dijalankan. Tapi ROS2 perlu tahu:
- Di mana node-node kamu?
- Dependensi apa yang dibutuhkan?
- Package apa saja yang tersedia?

### Solusi

Build mendaftarkan package kamu ke sistem ROS2.

---

## CARA KERJA

### Sebelum Build

```
ros2_ws/
└── src/
    └── ros2_belajar/    ← kode sumber ada di sini
```

Sistem ROS2 tidak tahu package `ros2_belajar` ada.

### Sesudah Build

```
ros2_ws/
├── src/                  ← kode sumber (tidak berubah)
├── build/                ← file sementara (jangan disentuh)
├── install/              ← hasil build siap pakai
│   └── ...
└── log/                  ← catatan build
```

Sekarang sistem tahu package `ros2_belajar` ada.

### Apa yang Terjadi Saat Build?

| Yang Dilakukan colcon | Kenapa? |
|-----------------------|---------|
| Membaca `package.xml` | Tahu dependensi package |
| Membaca `setup.py` | Tahu node apa saja yang ada |
| Menyalin file ke `install/` | ROS2 bisa menemukan package |
| Membuat `build/` dan `log/` | File sementara + catatan |

### Penting!

Build Python sebenarnya **tidak kompilasi** (tidak seperti C++). Yang dilakukan colcon:
1. Menyalin file ke `install/`
2. Membuat "entry point" agar `ros2 run` bisa memanggil node
3. Mendaftarkan package ke ROS2

---

## CONTOH

```bash
# 1. Source ROS2
source /opt/ros/humble/setup.bash

# 2. Masuk workspace
cd ~/ros2_ws

# 3. Build
colcon build

# Output:
# Starting >>> ros2_belajar
# Finished <<< ros2_belajar
#
# Summary: 1 package finished

# 4. Lihat folder baru
ls
# Output: src  build  install  log
```

---

## COBA INI

**Eksperimen — Build package yang sudah dibuat:**

```bash
# Pastikan sudah source
source /opt/ros/humble/setup.bash

# Build
cd ~/ros2_ws
colcon build
```

**Eksperimen — Build hanya satu package (kalau sudah banyak):**

```bash
colcon build --packages-select ros2_belajar
```

Ini lebih cepat karena hanya build package tertentu.

**Eksperimen — Build ulang (kalau ada perubahan kode):**

```bash
colcon build
```

Cukup jalankan `colcon build` lagi setiap kali ada perubahan kode.

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `colcon: command not found` | colcon belum terinstall | `sudo apt install python3-colcon-common-extensions` |
| `package.xml not found` | Bukan di folder workspace | Pastikan `cd` ke root workspace (yang ada `src/`) |
| `ModuleNotFoundError` saat build | Dependensi kurang | Tambah `<depend>` di `package.xml` |
| `SyntaxError` di file Python | Error di kode | Perbaiki error, build ulang |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 04** — Create Package: package yang sudah dibuat perlu di-build
- **Lanjut ke Modul 06** — Source Workspace: setelah build, harus source ulang

---

## 📁 PRAKTIK

Praktik ini **membangun (build) package** ROS2 dengan colcon.

### Langkah 1: Buka terminal
Buka terminal baru.

### Langkah 2: Source ROS2
```bash
source /opt/ros/humble/setup.bash
```

### Langkah 3: Masuk ke workspace
```bash
cd ~/ros2_ws
```

### Langkah 4: Build semua package
```bash
colcon build
```

**Output yang diharapkan:**
```
Summary: 1 package finished [X.Xs]
  1 package had a warning (optional)
  0 packages had errors
```

Pastikan tidak ada **error** (hanya warning boleh ada).

### Langkah 5: Cek folder hasil build
```bash
ls -la
```

**Output yang diharapkan:**
```
drwxr-xr-x ... build/
drwxr-xr-x ... install/
drwxr-xr-x ... log/
drwxr-xr-x ... src/
```

`build/` = file sementara, `install/` = hasil jadi, `log/` = catatan build.

### Langkah 6: Build package tertentu saja (lebih cepat)
```bash
colcon build --packages-select package_belajar
```

**Kesimpulan:** `colcon build` mengubah kode di `src/` menjadi executable di `install/`. Setelah build, jalankan `source install/setup.bash` agar node bisa dipanggil.
