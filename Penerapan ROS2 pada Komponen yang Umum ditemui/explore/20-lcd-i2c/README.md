# explore/20-lcd-i2c — Tampilkan Teks di LCD via ROS2

## Tujuan

Belajar **Subscriber dengan LCD** — menampilkan data ROS2 di layar LCD.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Subscriber |
| Topic | `/lcd` |
| Tipe | `std_msgs/String` |
| Data | Teks, format "baris1\nbaris2" untuk 2 baris |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "LiquidCrystal I2C" by Frank de Brabander → Install

### 2. Upload ke Arduino
Buka `lcd_i2c.ino` di Arduino IDE, upload ke board.

### 3. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 4. Kirim teks
```bash
# Tampilkan teks baris 1
ros2 topic pub /lcd std_msgs/msg/String "data: 'Halo ROS2!'" --once

# Tampilkan 2 baris (gunakan \n)
ros2 topic pub /lcd std_msgs/msg/String "data: 'Suhu: 28C\nKelemb: 65%'" --once
```

## Coba Ini

1. **Integrasi DHT (explore/05):** Buat Python node yang subscribe suhu + kelembapan, publish ke /lcd
2. **Scrolling text:** Kirim teks panjang, geser tiap 0.5 detik
3. **Counter:** Display hitungan mundur


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

