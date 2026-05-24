# explore/35-bluetooth — Bridge Bluetooth Serial via ROS2

## Tujuan

Belajar **bridge komunikasi** — menghubungkan HC-05 Bluetooth dengan ROS2.

## Konsep

HC-05 sebagai **bridge serial wireless** — data dari ROS2 dikirim via micro-ROS Agent → Arduino → Bluetooth → perangkat lain (HP/PC).

Atau sebaliknya: data dari HP → Bluetooth → Arduino → publish ke ROS2.

## Cara Jalankan

### 1. Upload ke Arduino
Buka `bluetooth.ino` di Arduino IDE, upload ke board.

### 2. Pair Bluetooth
Di PC/HP: cari "HC-05" (atau "HC-06"), pair dengan PIN 1234.
Catat COM port (Windows) atau /dev/rfcomm0 (Linux).

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Cek data
```bash
ros2 topic echo /bluetooth
# data: "data dari HP" → terima dari Bluetooth
```

## Coba Ini

1. **Kirim teks dari HP via terminal Bluetooth** — tampil di ROS2
2. **Kontrol LED dari HP:** Kirim "LED_ON" → Arduino parse → publish Bool ke /led
3. **Remote control:** HP sebagai remote robot via Bluetooth
