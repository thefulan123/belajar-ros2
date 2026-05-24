# ERROR.md — Panduan Troubleshooting

Error umum pada proyek ROS2 + Arduino.

---

## A. Error ROS2

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `ros2: command not found` | Belum source ROS2 | `source /opt/ros/humble/setup.bash` |
| `package 'xxx' not found` | Belum build / source | `colcon build` lalu `source install/setup.bash` |

## B. Error micro-ROS

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `No device found` | Arduino tidak terdeteksi | Cek: `ls /dev/tty*`, coba `/dev/ttyACM0` atau `/dev/ttyUSB0` |
| `Permission denied: /dev/ttyACM0` | Tidak punya akses serial | `sudo chmod 666 /dev/ttyACM0` |
| Agent connect lalu disconnect | Baud rate salah | Pastikan `Serial.begin(115200)` cocok dengan `--baud 115200` |
| `Agent not responding` | Library tidak cocok | Re-build micro-ROS agent untuk board yang dipakai |
| Topic dari Arduino tidak muncul | Node name conflict | Ganti nama node di sketch `.ino` |

## C. Error Arduino

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `avrdude: stk500_recv(): programmer is not responding` | Port salah atau board tidak terdeteksi | Pilih port yang benar di Tools → Port |
| `Error compiling for board` | Library tidak lengkap | Install library micro_ros_arduino via Library Manager |
| `Sketch too big` | Code terlalu besar untuk UNO (32KB) | Kurangi fitur, atau pindah ke ESP32 |
| `Out of memory` | RAM UNO penuh (2KB) | Kurangi variable global, kurangi array |

## D. Error Wiring

| Masalah | Kemungkinan | Cek |
|---------|------------|-----|
| Komponen tidak menyala | VCC/GND tidak terhubung | Cek dengan multimeter |
| LED tidak nyala | Resistor terlalu besar atau LED terbalik | LED kaki panjang = positif |
| Sensor baca 0 terus | Pin salah atau sensor rusak | Cek di contoh tanpa ROS2 dulu |
| Servo tidak bergerak | Power kurang | Coba power external |
| LCD tidak muncul | I2C address salah | Jalankan I2C Scanner sketch |

## E. Error ESP32

| Error | Penyebab | Solusi |
|-------|----------|--------|
| ESP32 tidak terdeteksi | Driver CH340/CP2102 tidak ada | Install driver USB-to-UART |
| WiFi tidak connect | SSID/password salah | Cek di serial monitor |
| `Brownout detector triggered` | Power tidak cukup | Pakai power supply 5V 2A |

## F. Error Python

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `ModuleNotFoundError: rclpy` | Belum source ROS2 | `source /opt/ros/humble/setup.bash` |
| `ModuleNotFoundError: cv2` | OpenCV belum install | `pip3 install opencv-python` |

## G. Error Serial

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `SerialException: could not open port` | Port sudah dipakai | Tutup monitor serial lain |
| Data serial acak | Baud rate tidak cocok | Pastikan 115200 di kedua sisi |
| `device or resource busy` | Program lain pakai port | `lsof /dev/ttyACM0` lalu kill proses |
