# MODUL 08: Workspace, Package, dan Build

**TAG:** infrastruktur / organisasi / build / sourcing

---

## APA ITU WORKSPACE?

Workspace adalah folder utama tempat kamu mengerjakan proyek ROS2.

```
nama_workspace/
└── src/              ← tempat semua package ROS2
```

Contoh:
```
ros2_ws/
└── src/
    ├── package_sensor/
    ├── package_motor/
    └── package_navigasi/
```

Nama workspace bebas. Yang penting struktur `src/` di dalamnya.

---

## APA ITU PACKAGE?

Package adalah **unit terkecil** dalam ROS2. Satu package berisi satu atau beberapa node yang saling terkait.

Struktur package Python:
```
nama_package/
├── package.xml          ← informasi package (nama, versi, dependensi)
├── setup.py             ← cara install package ini
├── setup.cfg            ← konfigurasi tambahan
├── nama_package/        ← folder kode Python
│   ├── __init__.py
│   ├── node_satu.py
│   └── node_dua.py
└── resource/            ← file resource (otomatis)
```

Tanpa package, ROS2 tidak tahu:
- Node apa saja yang ada?
- Library apa yang dibutuhkan?
- Bagaimana cara menjalankan node?

Package adalah "kemasan" yang memberitahu ROS2:
> "Ini node-nodenya. Ini dependensinya. Ini cara jalannya."

---

## CARA KERJA

### Struktur Workspace

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

### Struktur Package

Package ibarat **kemasan produk** di supermarket:

| Bagian Package | Analogi |
|----------------|---------|
| `package.xml` | Label kemasan: nama produk, komposisi, berat |
| `setup.py` | Cara membuka kemasan |
| Folder kode | Isi di dalam kemasan |

#### package.xml

```xml
<package format="3">
  <name>ros2_basics</name>
  <version>0.0.1</version>
  <description>Package belajar ROS2</description>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
</package>
```

Fungsi:
- `name` — nama package (untuk `ros2 run`)
- `depend` — library yang dibutuhkan

#### setup.py

```python
from setuptools import setup

package_name = 'ros2_basics'

setup(
    name=package_name,
    packages=[package_name],
    data_files=[],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'talker_node = ros2_basics.talker_node:main',
            'listener_node = ros2_basics.listener_node:main',
        ],
    },
)
```

Fungsi:
- `entry_points` — mendaftarkan node agar bisa dipanggil via `ros2 run`

### Build Process

Build adalah proses mengubah kode sumber menjadi file yang siap dijalankan.

```bash
cd ~/ros2_ws
colcon build
```

| Yang Dilakukan colcon | Kenapa? |
|-----------------------|---------|
| Membaca `package.xml` | Tahu dependensi package |
| Membaca `setup.py` | Tahu node apa saja yang ada |
| Menyalin file ke `install/` | ROS2 bisa menemukan package |
| Membuat `build/` dan `log/` | File sementara + catatan |

**Penting:** Build Python sebenarnya **tidak kompilasi** (tidak seperti C++). Yang dilakukan colcon:
1. Menyalin file ke `install/`
2. Membuat "entry point" agar `ros2 run` bisa memanggil node
3. Mendaftarkan package ke ROS2

### Sourcing Setelah Build

Setelah `colcon build`, kamu harus source file `install/setup.bash`:

```bash
cd ~/ros2_ws
source install/setup.bash
```

**Kenapa?** ROS2 tahu package bawaan (di `/opt/ros/humble/`), tapi **tidak tahu** package buatan kamu (di `~/ros2_ws/install/`).

```
Terminal baru
    │
    ▼
source /opt/ros/humble/setup.bash
    │ ROS2 tahu package Bawaan
    │ (rclpy, std_msgs, dll)
    ▼
source ~/ros2_ws/install/setup.bash
    │ ROS2 sekarang tahu package Kamu
    │ (ros2_belajar, dll)
    ▼
ros2 run ros2_belajar talker_node    ← berhasil
```

**Setiap kali build ulang** → **Source ulang.**

---

## MEMBUAT PACKAGE

```bash
# Format
ros2 pkg create --build-type ament_python nama_package

# Contoh: masuk ke workspace dulu
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python ros2_basics
```

Yang terjadi setelah perintah di atas:

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

Semua file dasar sudah siap tinggal diisi dengan kode node.

| Build Type | Bahasa | File Konfigurasi |
|------------|--------|------------------|
| `ament_python` | Python | setup.py |
| `ament_cmake` | C++ | CMakeLists.txt |

Untuk belajar ROS2, gunakan `ament_python` (Python) karena lebih mudah dibaca.

---

## CONTOH (End-to-End)

### 1. Buat workspace
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### 2. Buat package
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python ros2_belajar
```

### 3. Build
```bash
cd ~/ros2_ws
colcon build
```

### 4. Source workspace
```bash
source install/setup.bash
```

### 5. Verifikasi package terdeteksi
```bash
ros2 pkg list | grep ros2_belajar
```

---

## COBA INI

**Eksperimen 1 — Buat struktur workspace:**
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
ls -la
```
Lihat folder `src/` sudah ada.

**Eksperimen 2 — Lihat package bawaan ROS2:**
```bash
source /opt/ros/humble/setup.bash
ros2 pkg list | head -10
```
Semua package ada di `/opt/ros/humble/share/`.

**Eksperimen 3 — Buat package baru:**
```bash
source /opt/ros/humble/setup.bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python package_coba
ls package_coba/
```

**Eksperimen 4 — Build:**
```bash
cd ~/ros2_ws
colcon build
ls -la
# Output: src  build  install  log
```

**Eksperimen 5 — Source workspace lalu verifikasi:**
```bash
source install/setup.bash
ros2 pkg list | grep package_coba
```

**Eksperimen 6 — Buktikan tanpa source:**
Buka **terminal baru**, source ROS2 saja:
```bash
source /opt/ros/humble/setup.bash
ros2 pkg list | grep package_coba
# Tidak muncul — karena workspace belum di-source
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `package 'xxx' not found` | Belum build atau source | `colcon build` + `source install/setup.bash` |
| `ros2: command not found` | Belum source ROS2 | `source /opt/ros/humble/setup.bash` |
| `colcon: command not found` | colcon belum terinstall | `sudo apt install python3-colcon-common-extensions` |
| `package already exists` | Nama package sudah dipakai | Ganti nama package |
| `ModuleNotFoundError` saat build | Dependensi kurang | Tambah `<depend>` di `package.xml` |
| `setup.bash: No such file` | Belum build | Jalankan `colcon build` dulu |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 07** — Action (konsep komunikasi terakhir sebelum build)
- **Lanjut ke Modul 09** — Launch (menjalankan banyak node sekaligus)
- **Praktek: explore/01 hingga 06** — tidak perlu build karena standalone Python
- **Praktek: src/** — WAJIB melalui proses workspace → package → build → source
- **Penerapan Praktik:** Setup `microros_ws` (workspace micro-ROS) diperlukan untuk [semua 38 komponen penerapan](../../Penerapan%20ROS2%20pada%20Komponen%20yang%20Umum%20ditemui/explore/01-led/README.md)
   Lihat [KORELASI.md](../docs/KORELASI.md) untuk mapping lengkap.

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie cukup buka Arduino IDE, tulis kode, upload. Di ROS2, ada **workspace → package → build → source**.

| Aspek | ROS2 | Arduino Biasa |
|-------|------|---------------|
| Struktur | `workspace/src/` → build → install/ | 1 folder, 1 file `.ino` |
| Organisasi | Package → node → topic/service | `#include` + `setup()` + `loop()` |
| Cara buat proyek | `ros2 pkg create --build-type ament_python` | File → New → Save As |
| Build | `colcon build` — semua package | Ctrl+R — 1 file `.ino` |
| Setelah build | `source install/setup.bash` | Langsung upload ke board |
| Scalability | Puluhan node dalam 1 workspace | 1 program = 1 board |
| Error handling | 1 node error → node lain tetap jalan | Error = seluruh program crash |

**Intinya:** ROS2 butuh setup awal yang lebih ribet, tapi begitu proyekmu punya 5+ sensor dan 3+ aktuator, struktur ini menyelamatkanmu dari kekacauan. Arduino simpel karena targetnya 1 board untuk 1 tugas.

---

## 📁 PRAKTIK

Praktik ini membuat **workspace → package → build → source** secara end-to-end.

### Langkah 1: Buka terminal
Buka terminal baru.

### Langkah 2: Source ROS2
```bash
source /opt/ros/humble/setup.bash
```

### Langkah 3: Buat workspace
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
ls -la
```

**Output yang diharapkan:**
```
drwxr-xr-x ... .
drwxr-xr-x ... ..
drwxr-xr-x ... src
```

### Langkah 4: Buat package
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python package_belajar
```

**Output yang diharapkan:**
```
creating ./package_belajar/package.xml
creating ./package_belajar/setup.py
creating ./package_belajar/setup.cfg
creating ./package_belajar/package_belajar/__init__.py
```

### Langkah 5: Lihat struktur package
```bash
ls -R package_belajar/
```

**Output yang diharapkan:**
```
package_belajar:
package_belajar  package.xml  setup.cfg  setup.py

package_belajar/package_belajar:
__init__.py
```

### Langkah 6: Build semua package
```bash
cd ~/ros2_ws
colcon build
```

**Output yang diharapkan:**
```
Summary: 1 package finished [X.Xs]
  0 packages had errors
```

### Langkah 7: Cek folder hasil build
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

### Langkah 8: Source workspace
```bash
source install/setup.bash
```

### Langkah 9: Verifikasi package terdeteksi
```bash
ros2 pkg list | grep package_belajar
```

**Output yang diharapkan:**
```
package_belajar
```

### Langkah 10: Cek variabel environment
```bash
echo $AMENT_PREFIX_PATH
```

**Output yang diharapkan:**
```
/home/nama_user/ros2_ws/install/package_belajar:/opt/ros/humble
```

**Kesimpulan:** Setiap terminal baru harus menjalankan:
1. `source /opt/ros/humble/setup.bash` — mengaktifkan ROS2
2. `colcon build` — membangun package (cukup sekali, ulangi jika ada perubahan)
3. `source ~/ros2_ws/install/setup.bash` — membuat package dikenali sistem

---

## REFERENSI

- [ROS2 Humble: Creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html)
- [ROS2 Humble: Creating a package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html)
- [ROS2 Humble: Building a package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Building-ROS2-Packages.html)
- [ROS2 Humble: Sourcing workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html)
