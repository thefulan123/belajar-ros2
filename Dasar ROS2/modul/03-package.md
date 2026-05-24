# MODUL 03: Package

**TAG:** organisasi / struktur / dependensi

---

## APA ITU PACKAGE?

Package adalah unit terkecil dalam ROS2. Satu package berisi satu atau beberapa node yang saling terkait.

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

---

## KENAPA ADA?

### Masalah

Tanpa package, ROS2 tidak tahu:
- Node apa saja yang ada?
- Library apa yang dibutuhkan?
- Bagaimana cara menjalankan node?

### Solusi

Package adalah "kemasan" yang memberitahu ROS2:
> "Ini node-nodenya. Ini dependensinya. Ini cara jalannya."

---

## CARA KERJA

Package ibarat **kemasan produk** di supermarket:

| Bagian Package | Analogi |
|----------------|---------|
| `package.xml` | Label kemasan: nama produk, komposisi, berat |
| `setup.py` | Cara membuka kemasan |
| Folder kode | Isi di dalam kemasan |

### package.xml

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

### setup.py

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

---

## CONTOH

```bash
# 1. Cek package yang terinstall
ros2 pkg list

# Output: daftar panjang semua package ROS2
# (termasuk yang kamu buat setelah build)
```

---

## COBA INI

**Eksperimen — Lihat package ROS2 yang sudah ada:**

```bash
source /opt/ros/humble/setup.bash
ros2 pkg list | head -10
```

Kamu akan lihat puluhan package bawaan ROS2. Semua itu ada di folder:
```
/opt/ros/humble/share/
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `package 'xxx' not found` | Belum build atau source | `colcon build` + `source install/setup.bash` |
| `ros2: command not found` | Belum source ROS2 | `source /opt/ros/humble/setup.bash` |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 02** — Workspace: package ada di dalam `src/`
- **Lanjut ke Modul 04** — Create Package: cara membuat package sendiri
- **Lanjut ke Modul 05** — Build Package: cara build package

---

## 🔄 ROS2 vs Arduino Biasa

Anak robotik newbie pake **library Arduino** dari Library Manager. ROS2 punya **package**.

| Aspek | ROS2 Package | Arduino Library |
|-------|-------------|-----------------|
| Lokasi | `src/nama_package/` | `~/Arduino/libraries/` |
| Isi | `package.xml`, `setup.py`, `src/` | `.h` + `.cpp` + `library.properties` |
| Fungsi | Bungkus node + msg + service + action | Bungkus fungsi hardware (LCD, sensor) |
| Cara pasang | `ros2 pkg create` | Tools → Manage Libraries |
| Dependensi | Tulis di `package.xml` | `#include <...>` aja |
| Milik siapa | Bikin sendiri + package bawaan ROS2 | Dibuat komunitas Arduino |

**Intinya:** Package ROS2 = library Arduino versi dewasa — lebih terstruktur dan bisa berisi banyak komponen (node, topic, service, action) sekaligus.

---

## 📁 PRAKTIK

Praktik ini menjelajahi package bawaan ROS2 dan melihat strukturnya.

### Langkah 1: Buka terminal
Buka terminal baru.

### Langkah 2: Source ROS2
```bash
source /opt/ros/humble/setup.bash
```

### Langkah 3: Lihat semua package terinstall
```bash
ros2 pkg list
```

**Output yang diharapkan:**
```
ackermann_msgs
action_msgs
action_tutorials_interfaces
...
```
Puluhan package bawaan ROS2 akan muncul.

### Langkah 4: Lihat 10 package pertama
```bash
ros2 pkg list | head -10
```

### Langkah 5: Cek lokasi file package
```bash
ls /opt/ros/humble/share/
```

**Output yang diharapkan:**
```
action_msgs          action_tutorials_interfaces  ...
...
```
Semua package ROS2 tersimpan di `/opt/ros/humble/share/`.

### Langkah 6: Lihat isi satu package
```bash
ls /opt/ros/humble/share/std_msgs/
```

**Output yang diharapkan:**
```
cmake  msg  package.xml
```

**Kesimpulan:** Setiap package ROS2 berisi `package.xml`, folder `msg/`, `srv/`, `action/`, dan kode sumber.
