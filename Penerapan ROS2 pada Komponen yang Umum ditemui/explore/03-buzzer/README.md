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

