# explore/29-water-pump — Kontrol Pompa Air via ROS2

## Tujuan

Belajar **Subscriber aktuator daya** — mengontrol pompa air dari ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/pompa` |
| Tipe | `std_msgs/Bool` |
| Data | `true` = pompa ON, `false` = pompa OFF |

## Cara Jalankan

### 1. Upload ke Arduino
Buka `water_pump.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Kirim perintah
```bash
# Pompa ON
ros2 topic pub /pompa std_msgs/msg/Bool "data: true" --once

# Pompa OFF
ros2 topic pub /pompa std_msgs/msg/Bool "data: false" --once
```

## Coba Ini

1. **Integrasi soil moisture (explore/08):** Auto-watering — pompa ON jika tanah kering
2. **Timer:** Pompa ON 10 detik, OFF 30 detik (irigasi otomatis)
3. **Integrasi flow sensor (explore/27):** Pompa OFF jika debit > threshold (bocor)
4. **Integrasi rain sensor (explore/28):** Pompa OFF jika hujan


---

---

## 🔄 ROS2 vs Arduino Biasa

Komponen ini bisa dikontrol dengan Arduino biasa via `digitalWrite()` / `analogWrite()`. Tapi bedanya:

### Arduino Biasa (langsung di sketch):
```cpp
void loop() {
  digitalWrite(PIN, HIGH);
  delay(1000);
  digitalWrite(PIN, LOW);
  delay(1000);
}
```
- Polanya KERAS — harus ditentukan di kode
- Mau rubah? Edit kode, upload ulang
- Nggak bisa dikontrol dari luar (PC, sensor lain)

### Arduino + micro-ROS (Topic Subscriber):
```cpp
void subscription_callback(const void *msgin) {
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;
  digitalWrite(PIN, msg->data);
}
```
- Dikontrol dari MANA SAJA via topic ROS2
- Bisa dari CLI: `ros2 topic pub /topic ...`
- Bisa dari sensor lain: button, suhu, timer
- Tanpa upload ulang!

### Perbandingan Langsung

| Aspek | Arduino + micro-ROS | Arduino Standalone |
|-------|--------------------|--------------------|
| Kontrol dari | PC, sensor lain, timer, CLI | Cuma dari kode yang sudah di-upload |
| Ubah perilaku | `ros2 topic pub` — langsung tanpa upload | Edit sketch → compile → upload |
| Integrasi | Langsung nyambung ke publisher mana pun | Manual — semua kode di 1 sketch |
| Cocok | Robot butuh kontrol dinamis dari banyak sumber | Projekt fixed-function (blink, timer) |

