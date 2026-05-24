# MODUL 04: Create Package

**TAG:** praktik / command / struktur

---

## APA ITU CREATE PACKAGE?

Membuat package ROS2 baru dengan perintah:

```bash
ros2 pkg create --build-type ament_python <nama_package>
```

Perintah ini otomatis membuat struktur folder package yang siap pakai.

---

## KENAPA ADA?

### Masalah

Membuat struktur package secara manual rawan salah:
- Lupa `package.xml`
- Salah format `setup.py`
- Folder kode tidak sesuai

### Solusi

`ros2 pkg create` membuat struktur yang benar secara otomatis.

---

## CARA KERJA

### Perintah Dasar

```bash
# Format
ros2 pkg create --build-type ament_python nama_package

# Contoh
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python ros2_basics
```

### Yang Terjadi

Setelah perintah di atas, folder `ros2_basics/` muncul dengan isi:

```
ros2_basics/
├── package.xml
├── setup.py
├── setup.cfg
├── ros2_basics/
│   └── __init__.py
├── resource/
│   └── ros2_basics
└── test/
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py
```

Semua file dasar sudah siap tinggal diisi.

### Build Type

| Build Type | Bahasa | File Konfigurasi |
|------------|--------|------------------|
| `ament_python` | Python | setup.py |
| `ament_cmake` | C++ | CMakeLists.txt |

Untuk belajar ROS2, gunakan `ament_python` (Python) karena lebih mudah dibaca.

---

## CONTOH

```bash
# 1. Masuk ke workspace
cd ~/ros2_ws/src

# 2. Buat package baru
ros2 pkg create --build-type ament_python ros2_belajar

# 3. Lihat hasilnya
ls ros2_belajar/
# Output: package.xml  setup.py  setup.cfg  ros2_belajar/  resource/  test/
```

---

## COBA INI

**Eksperimen — Buat package baru:**

```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python package_coba
ls package_coba/
```

**Yang perlu diperhatikan:**
- Folder `package_coba/package_coba/` — tempat kode Python
- File `package.xml` — edit nama, deskripsi, dependensi
- File `setup.py` — edit `entry_points` untuk daftar node

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `package already exists` | Nama sudah dipakai | Ganti nama package |
| `ros2: command not found` | Belum source | `source /opt/ros/humble/setup.bash` |
| `SyntaxError di package.xml` | Format XML salah | Hapus package, buat ulang |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 03** — Package: penjelasan struktur package
- **Lanjut ke Modul 05** — Build Package: cara build package yang sudah dibuat
