# MODUL 06: Source Workspace

**TAG:** sourcing / environment / workflow

---

## APA ITU SOURCE WORKSPACE?

Setelah `colcon build`, kamu harus source file `install/setup.bash` di workspace kamu:

```bash
cd ~/ros2_ws
source install/setup.bash
```

---

## KENAPA ADA?

### Masalah

Kamu sudah:
1. Source ROS2 (`source /opt/ros/humble/setup.bash`)
2. Build package (`colcon build`)

Tapi ketika menjalankan:
```bash
ros2 run ros2_belajar talker_node
```
Hasil:
```
package 'ros2_belajar' not found
```

Kenapa? Karena ROS2 tahu package bawaan (di `/opt/ros/humble/`), tapi **tidak tahu** package buatan kamu (di `~/ros2_ws/install/`).

### Solusi

Source workspace kamu:
```bash
source ~/ros2_ws/install/setup.bash
```

Ini memberitahu ROS2:
> "Lihat juga di folder ini untuk package tambahan."

---

## CARA KERJA

### Alur Lengkap Sourcing

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

### Kenapa Harus Source Ulang Setelah Build?

Karena:
1. Build menambahkan file baru ke `install/`
2. Sourcing ulang membuat ROS2 membaca daftar terbaru

### Analogi

Bayangkan daftar menu restoran:
- `source /opt/ros/humble/setup.bash` = daftar menu nasional
- `colcon build` = koki membuat menu baru di dapur
- `source install/setup.bash` = menu baru ditambahkan ke daftar

Kalau tidak source ulang, pelayan (ROS2) tidak tahu ada menu baru.

---

## CONTOH

```bash
# Terminal baru
# 1. Source ROS2 (wajib)
source /opt/ros/humble/setup.bash

# 2. Build package
cd ~/ros2_ws
colcon build

# 3. Source workspace (wajib setelah build)
source install/setup.bash

# 4. Jalankan node
ros2 run ros2_belajar talker_node
```

### Catatan Penting

**Setiap kali build ulang** → **Source ulang.**

Urutan SOURCING selalu:
1. ROS2 dulu (`/opt/ros/humble/setup.bash`)
2. Workspace kedua (`install/setup.bash`)

Kalau source workspace duluan, ROS2 belum aktif — error.

---

## COBA INI

**Eksperimen — Buktikan bahwa workspace harus di-source:**

Buka terminal, lakukan:
```bash
# 1. Source ROS2
source /opt/ros/humble/setup.bash

# 2. Coba cari package kamu (tanpa source workspace)
ros2 pkg list | grep ros2_belajar
# Mungkin tidak muncul

# 3. Source workspace
cd ~/ros2_ws
source install/setup.bash

# 4. Coba lagi
ros2 pkg list | grep ros2_belajar
# Sekarang muncul
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `package 'xxx' not found` | Workspace belum di-source | `cd ~/ros2_ws && source install/setup.bash` |
| `setup.bash: No such file` | Belum build | Jalankan `colcon build` dulu |
| `command not found` padahal sudah source | Source workspace duluan | Source ROS2 dulu, baru workspace |
| `package lama masih terlihat` | Build baru belum di-source | `source install/setup.bash` ulang |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Sebelumnya: Modul 01** — Sourcing: konsep sourcing environment variable
- **Sebelumnya: Modul 05** — Build Package: kenapa harus source ulang setelah build
- **Praktek: explore/01 hingga 06** — tidak perlu source workspace karena standalone Python
- **Praktek: src/** — WAJIB source workspace

---

## 📁 PRAKTIK

Praktik ini mensimulasikan **sourcing workspace** setelah `colcon build`.

### Langkah 1: Buka terminal
Buka terminal baru.

### Langkah 2: Source ROS2 dulu (WAJIB)
```bash
source /opt/ros/humble/setup.bash
```

### Langkah 3: Masuk ke workspace
```bash
cd ~/ros2_ws
```

### Langkah 4: Source workspace
```bash
source install/setup.bash
```

Tidak ada output jika berhasil.

### Langkah 5: Verifikasi — cari package workspace
```bash
ros2 pkg list | grep package_belajar
```

**Output yang diharapkan:**
```
package_belajar
```

Package buatanmu sekarang terdeteksi oleh ROS2.

### Langkah 6: Cek variabel environment
```bash
echo $AMENT_PREFIX_PATH
```

**Output yang diharapkan:**
```
/home/nama_user/ros2_ws/install/package_belajar:/opt/ros/humble
```

### Langkah 7: Coba tanpa source workspace
Buka **terminal baru**, source ROS2 saja:
```bash
source /opt/ros/humble/setup.bash
ros2 pkg list | grep package_belajar
```

**Output yang diharapkan:**
```
(tidak muncul apa-apa)
```

**Kesimpulan:** Setiap terminal baru harus menjalankan BOTH:
1. `source /opt/ros/humble/setup.bash`
2. `source ~/ros2_ws/install/setup.bash`
