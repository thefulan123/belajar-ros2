# 00 — Software Requirements & Instalasi

Semua software yang dibutuhkan untuk menjalankan proyek ROS2 dengan Arduino/ESP.

---

## A. ROS2 Humble

### Instalasi

```bash
# 1. Setup source list
sudo apt update && sudo apt install curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 2. Install ROS2 Humble
sudo apt update
sudo apt install ros-humble-desktop

# 3. Source (tambahkan ke ~/.bashrc biar otomatis)
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verifikasi

```bash
ros2 --version
# Output: ros2 humble ... (atau versi terbaru)

ros2 topic list
# Output: (daftar kosong — tidak error)
```

---

## B. Arduino IDE

### Cara 1 — Snap (Mudah)

```bash
sudo snap install arduino
```

### Cara 2 — Download Manual

1. Buka: https://www.arduino.cc/en/software
2. Download **Linux ZIP file** (bukan AppImage)
3. Ekstrak:
   ```bash
   cd ~/Downloads
   unzip arduino-*-linux*.zip
   sudo mv arduino-* /opt/
   cd /opt/arduino-*
   sudo ./install.sh
   ```

### Verifikasi

```bash
arduino --version
# Output: Arduino CLI ...
```

### Setelah Install — Konfigurasi Board

1. Buka Arduino IDE
2. **Tools → Board → Boards Manager**
3. Cari dan install:
   - `Arduino AVR Boards` (untuk UNO/Nano)
   - `esp32` by Espressif (untuk ESP32)

### Izin Port Serial

Supaya bisa upload tanpa sudo:

```bash
sudo usermod -aG dialout $USER
# Logout lalu login lagi (atau restart WSL)
```

---

## C. micro-ROS Agent

micro-ROS Agent adalah jembatan antara Arduino dan ROS2.

### Instalasi

```bash
source /opt/ros/humble/setup.bash

# Buat workspace
mkdir -p ~/microros_ws/src
cd ~/microros_ws

# Clone micro-ROS setup
git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Install dependencies
sudo apt update
rosdep update
rosdep install --from-paths src --ignore-src -y

# Build setup tools
colcon build
source install/setup.bash

# Download dan build agent
ros2 run micro_ros_setup create_agent_ws.sh
colcon build
source install/setup.bash
```

### Verifikasi

```bash
ros2 run micro_ros_agent micro_ros_agent --help
# Output: (daftar parameter — tidak error)
```

### Cara Jalankan Agent

```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash

# Serial (Arduino UNO/Nano)
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200

# UDP/WiFi (ESP32)
ros2 run micro_ros_agent micro_ros_agent udp --port 8888
```

---

## D. micro-ROS Arduino Library

### Cara 1 — Arduino Library Manager

1. Buka Arduino IDE
2. **Sketch → Include Library → Manage Libraries**
3. Cari: `micro_ros_arduino`
4. Install

### Cara 2 — Manual via Git

```bash
cd ~/Arduino/libraries
git clone https://github.com/micro-ROS/micro_ros_arduino.git
```

### Verifikasi

Buka Arduino IDE:
- **File → Examples → micro_ros_arduino**
- Harusnya muncul contoh: `micro-ros_publisher`, `micro-ros_subscriber`

---

## E. Python Packages (untuk PC-side nodes)

```bash
pip3 install opencv-python      # Webcam / image processing
pip3 install pyserial           # Serial communication
pip3 install numpy              # Array manipulation
```

---

## F. PlatformIO (Opsional — Alternatif Arduino IDE)

```bash
# Install VS Code extension
# Buka VS Code → Extensions → cari "PlatformIO IDE" → Install
```

Atau CLI:

```bash
pip3 install platformio
```

---

## G. Tools Pendukung

```bash
# Serial monitor CLI
sudo apt install screen

# GUI serial monitor
sudo apt install moserial

# ROS2 tools
sudo apt install ros-humble-rqt
sudo apt install ros-humble-rqt-graph
sudo apt install ros-humble-plotjuggler
```

---

## H. Diagnostik — Cek Semua Instalasi

Jalankan script ini untuk verifikasi:

```bash
#!/usr/bin/env bash
echo "=== DIAGNOSTIK ==="

echo -n "ROS2: "
source /opt/ros/humble/setup.bash 2>/dev/null && echo "✅ $ROS_DISTRO" || echo "❌"

echo -n "Arduino CLI: "
which arduino 2>/dev/null && echo "✅" || echo "❌"

echo -n "micro-ROS Agent: "
source ~/microros_ws/install/setup.bash 2>/dev/null
which micro_ros_agent 2>/dev/null && echo "✅" || echo "❌"

echo -n "Python rclpy: "
python3 -c "import rclpy; print('✅')" 2>/dev/null || echo "❌"

echo -n "colcon: "
colcon --version 2>/dev/null || echo "❌"

echo -n "Git: "
git --version 2>/dev/null || echo "❌"
```

Simpan sebagai `cek-instalasi.sh` dan jalankan:

```bash
bash cek-instalasi.sh
```

---

## Ringkasan

| Software | Wajib? | Install |
|----------|--------|---------|
| ROS2 Humble | ✅ Wajib | `apt install ros-humble-desktop` |
| Arduino IDE | ✅ Wajib | `snap install arduino` |
| micro-ROS Agent | ✅ Wajib | Build dari source |
| micro-ROS Library | ✅ Wajib | Arduino Library Manager |
| Python + rclpy | ✅ Wajib | (dari ROS2) |
| PlatformIO | ⬜ Opsional | VS Code extension |
| rqt / plotjuggler | ⬜ Opsional | `apt install` |
| Git | ⬜ Opsional | `apt install git` |
