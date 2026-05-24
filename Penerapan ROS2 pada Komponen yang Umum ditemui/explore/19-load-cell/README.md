# explore/19-load-cell — Baca Berat via ROS2 (Load Cell + HX711)

## Tujuan

Belajar **Publisher sensor berat** — membaca berat dari load cell dan kirim ke ROS2.

## Konsep ROS2

| Aspek | Penjelasan |
|-------|-----------|
| Peran | Publisher |
| Topic | `/berat` |
| Tipe | `std_msgs/Float64` |
| Data | Berat dalam gram |
| Frekuensi | 5 Hz |

## Cara Jalankan

### 1. Install library
Arduino IDE → Tools → Manage Libraries → Cari "HX711" by Bogdan Necula → Install

### 2. Kalibrasi
Sebelum dipakai, load cell perlu kalibrasi:

1. Upload code
2. Buka Serial Monitor (115200 baud)
3. Letakkan beban yang diketahui beratnya (misal 100g)
4. Catat nilai `hx711.read()` yang muncul
5. Hitung faktor = nilai / berat
6. Ganti `KALIBRASI_FAKTOR` di code

### 3. Upload ke Arduino
Buka `load_cell.ino` di Arduino IDE, upload ke board.

### 4. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 5. Cek data
```bash
ros2 topic echo /berat
# data: 150.0  → 150 gram
```

## Coba Ini

1. **Timbang benda sekitar** — berapa gram?
2. **Tara:** Buat script Python subscribe /berat, record nilai awal sebagai offset
3. **Integrasi relay (explore/04):** Nyalakan relay jika berat > threshold (conveyor)


---

## 🔄 ROS2 vs Arduino Biasa

Sensor ini bisa dibaca dengan Arduino biasa via `Serial.print()`. Tapi bedanya:

### Arduino Biasa (Serial Monitor):
```cpp
void loop() {
  int nilai = analogRead(PIN_SENSOR);
  Serial.println(nilai);  // Cuma angka di monitor
  delay(500);
}
```
- Kamu lihat angkanya di Serial Monitor
- Nggak bisa dipake program lain
- Kalau mau kontrol sesuatu, harus tulis semua logic di 1 sketch

### Arduino + micro-ROS (Topic Publisher):
```cpp
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  msg.data = analogRead(PIN_SENSOR);
  rcl_publish(&publisher, &msg, NULL);
}
```
- Data otomatis masuk ke sistem ROS2
- Bisa dibaca node lain (PC, motor, LED, dll)
- Bisa di-log, dianalisis, digabung sensor lain

### Perbandingan Langsung

| Aspek | Arduino + micro-ROS | Arduino Standalone |
|-------|--------------------|--------------------|
| Data sampai ke | Seluruh sistem ROS2 (PC + board lain) | Hanya Serial Monitor |
| Integrasi | 1 baris `rcl_publish()` — langsung nyambung | Tulis ulang kode parsing |
| Expandability | Tinggal tambah subscriber di node lain | Ubah sketch + upload ulang |
| Debug | `ros2 topic echo /topic` | Serial Monitor |
| Cocok | Robot multi-sensor, sistem terdistribusi | Belajar 1 sensor, cek data cepat |

