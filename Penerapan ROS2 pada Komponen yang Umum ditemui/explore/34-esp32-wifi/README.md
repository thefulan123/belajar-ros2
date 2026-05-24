# explore/34-esp32-wifi — ESP32 micro-ROS via WiFi

## Tujuan

Belajar **bridge wireless** — ganti transport micro-ROS dari Serial ke WiFi.

## Konsep

Selama ini kita pakai micro-ROS via **Serial USB**. Untuk aplikasi mobile/robot, kabel tidak praktis. ESP32 punya WiFi built-in — kita bisa ganti transport ke **UDP** via WiFi.

## Perubahan

| Aspek | Serial (sebelumnya) | WiFi (sekarang) |
|-------|-------------------|-----------------|
| Koneksi | USB kabel | Wireless |
| Jarak | 2-3 meter (USB) | ~30 meter (WiFi) |
| Baud rate | 115200 | N/A |
| Agent | serial --dev /dev/ttyACM0 | udp --port 8888 |
| Power | Dari USB | Baterai / Power bank |

## Cara Jalankan

### 1. Ganti code

Di setiap sketch `.ino`, ganti bagian setup transport:

```cpp
// OLD (Serial):
#include <micro_ros_arduino.h>
// ...
Serial.begin(115200);
set_microros_serial_transports(Serial);

// NEW (WiFi):
#include <micro_ros_arduino.h>
#include <WiFi.h>
// ...
set_microros_wifi_transports("SSID_WIFI", "PASSWORD", "192.168.1.100", 8888);
```

### 2. Upload WiFi-enabled sketch ke ESP32
Ubah code sesuai di atas, upload ke ESP32.

### 3. Jalankan agent di PC
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent udp --port 8888
```

### 4. ESP32 akan connect otomatis ke agent via WiFi

### 5. Cek seperti biasa
```bash
ros2 topic list
ros2 topic echo /topic_anda
```

## Catatan Penting

| Masalah | Solusi |
|---------|--------|
| ESP32 tidak connect | Cek SSID/password, pastikan PC dan ESP32 di network sama |
| Agent "No data" | Firewall: allow port 8888 UDP `sudo ufw allow 8888/udp` |
| Topic tidak muncul | ESP32 butuh ~5 detik untuk WiFi connect + micro-ROS init |
| IP agent berubah | Set static IP di router, atau ganti IP di code |

## Contoh Sketch WiFi

File `esp32_wifi.ino` di folder ini.

## Coba Ini

1. **Bawa ESP32 ke ruangan lain** — masih terhubung?
2. **Ganti ke battery power** — ESP32 via power bank
3. **Integrasi semua explore sebelumnya** — sekarang nirkabel!
