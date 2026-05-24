# Panduan Error / Error Guide

Dual language — Indonesia + English.

---

## 1. `ros2: command not found`

**ID:** ROS2 belum di-source. Setiap buka terminal baru, ROS2 perlu diaktifkan dulu.

**EN:** ROS2 hasn't been sourced. Every new terminal needs ROS2 activation.

**Solusi / Solution:**
```bash
source /opt/ros/humble/setup.bash
```
Atau pakai script yang sudah disediakan:
```bash
source scripts/source_ros.sh
```

---

## 2. `ModuleNotFoundError: No module named 'rclpy'`

**ID:** Python tidak bisa menemukan library ROS2. Biasanya karena belum source.

**EN:** Python can't find the ROS2 library. Usually because it hasn't been sourced.

**Solusi / Solution:**
```bash
source /opt/ros/humble/setup.bash
```
Coba lagi:
```bash
python3 -c "import rclpy; print('OK')"
```

---

## 3. `package 'xxx' not found`

**ID:** ROS2 tidak menemukan package yang dimaksud. Dua kemungkinan: (1) belum build, (2) belum source workspace.

**EN:** ROS2 can't find the specified package. Two possibilities: (1) not built yet, (2) workspace not sourced.

**Solusi / Solution:**
```bash
# Build dulu
cd /path/ke/workspace
colcon build

# Source workspace
source install/setup.bash
```

---

## 4. Permission denied saat jalankan script

**ID:** File script tidak punya izin eksekusi.

**EN:** Script file doesn't have execute permission.

**Solusi / Solution:**
```bash
chmod +x namafile.sh
```

---

## 5. `colcon: command not found`

**ID:** colcon belum terinstall.

**EN:** colcon is not installed.

**Solusi / Solution:**
```bash
sudo apt install python3-colcon-common-extensions
```

---

## 6. Topic tidak muncul (`ros2 topic list`)

**ID:** Sudah menjalankan node tapi topic tidak terlihat.

**EN:** Node is running but topics don't appear.

**Kemungkinan / Possibilities:**
1. Node belum publish — cek apakah ada timer/callback aktif
2. Node mungkin crash sebelum sempat publish — cek terminal errornya
3. Belum source workspace yang benar
4. Node menggunakan namespace berbeda

**Solusi / Solution:**
Pastikan terminal yang menjalankan node sudah di-source:
```bash
source /opt/ros/humble/setup.bash
ros2 run <package_name> <node_name>
```
Di terminal lain:
```bash
source /opt/ros/humble/setup.bash
ros2 topic list
ros2 topic echo /nama_topic
```

---

## 7. `builtins.KeyError: 'PYTHON_DEPS'` atau error aneh di colcon

**ID:** Masalah dependensi Python.

**EN:** Python dependency issue.

**Solusi / Solution:**
```bash
pip3 install setuptools
```

---

## 8. WSL — `Cannot find ROS2` atau permission issue

**ID:** WSL kadang punya masalah path atau permission.

**EN:** WSL sometimes has path or permission issues.

**Solusi / Solution:**
```bash
# Pastikan WSL versi 2
wsl --set-version <distro> 2

# Kalau file di /mnt/ (Windows filesystem) bermasalah,
# pindahkan proyek ke ~/ (Linux filesystem dalam WSL)
```
