# explore/03-buzzer — Kontrol Buzzer via ROS2

## Tujuan

Belajar **Subscriber** dan PWM — buzzer bunyi berdasarkan perintah ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/buzzer` |
| Tipe | `std_msgs/Int32` |
| Data | `0` = mati, `>0` = bunyi (frequency Hz) |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `buzzer.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Buzzer mati
ros2 topic pub /buzzer std_msgs/msg/Int32 "data: 0" --once

# Buzzer bunyi frekuensi 1000 Hz
ros2 topic pub /buzzer std_msgs/msg/Int32 "data: 1000" --once

# Alarm (pakai script Python)
```

## Coba Ini

1. **Alarm system:** Integrasi dengan push button — bunyikan buzzer saat tombol di-press
2. **Musik:** Ganti frekuensi tiap 500ms untuk membuat nada sederhana
3. **Peringatan sensor:** Bunyikan jika suhu > 30°C (integrasi dengan explore/05-dht-sensor)
