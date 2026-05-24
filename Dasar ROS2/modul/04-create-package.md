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

---

## 📁 PRAKTIK

Praktik ini membuat **package ROS2 Python** pertama kamu.

### Langkah 1: Buka terminal
Buka terminal baru.

### Langkah 2: Source ROS2
```bash
source /opt/ros/humble/setup.bash
```

### Langkah 3: Buat workspace (jika belum ada)
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### Langkah 4: Buat package baru
```bash
ros2 pkg create --build-type ament_python package_belajar
```

**Output yang diharapkan:**
```
going to create a new package
 - package name: package_belajar
 - destination: ...
 - package format: 3
 - ...
creating ./package_belajar/package.xml
creating ./package_belajar/setup.py
creating ./package_belajar/setup.cfg
creating ./package_belajar/package_belajar
creating ./package_belajar/package_belajar/__init__.py
```

Package `package_belajar` berhasil dibuat.

### Langkah 5: Lihat struktur package
```bash
ls -R package_belajar/
```

**Output yang diharapkan:**
```
package_belajar/:
package_belajar  package.xml  setup.cfg  setup.py

package_belajar/package_belajar:
__init__.py
```

### Langkah 6: Lihat isi `package.xml`
```bash
cat package_belajar/package.xml
```

**Output yang diharapkan:**
```xml
<?xml version="1.0"?>
<package format="3">
  <name>package_belajar</name>
  <version>0.0.0</version>
  <description>TODO: Package description</description>
  ...
</package>
```

**Kesimpulan:** Package ROS2 Python siap diisi dengan node di `package_belajar/package_belajar/` dan didaftarkan di `setup.py`.
