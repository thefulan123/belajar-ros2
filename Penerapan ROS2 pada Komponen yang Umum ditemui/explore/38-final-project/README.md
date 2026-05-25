# explore/38-final-project — Proyek Akhir: Robot Monitoring Rumah

## Deskripsi

Proyek akhir menggabungkan **semua komponen** dalam satu sistem **Smart Home Monitoring Robot** — robot sederhana yang bisa:

1. **Berkeliling** (Motor DC + Driver L298N)
2. **Menghindari rintangan** (Ultrasonic HC-SR04)
3. **Mendeteksi kebocoran gas** (MQ-2)
4. **Mendeteksi api** (Flame Sensor)
5. **Mengukur suhu ruangan** (DHT11)
6. **Mengirim data real-time** ke PC via ROS2
7. **Alarm** jika ada bahaya (Buzzer)
8. **Display status** di LCD

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────┐
│                      PC (ROS2)                       │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Dashboard│  │ Logger   │  │ Alarm Monitor     │  │
│  │ (rqt)    │  │ (CSV)    │  │ (Python)          │  │
│  └──────────┘  └──────────┘  └───────────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │
              micro-ROS Agent (Serial/WiFi)
                       │
┌──────────────────────┴──────────────────────────────┐
│              ESP32 / Arduino (Robot)                 │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │Motor DC  │  │Ultrasonic│  │DHT11     │           │
│  │(L298N)   │  │(HC-SR04) │  │(Suhu)    │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │MQ-2      │  │Flame     │  │Buzzer    │           │
│  │(Gas)     │  │(Api)     │  │(Alarm)   │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│  ┌──────────┐  ┌──────────┐                         │
│  │LCD I2C   │  │Encoder   │                         │
│  │(Display) │  │(Odometry)│                         │
│  └──────────┘  └──────────┘                         │
└─────────────────────────────────────────────────────┘
```

## Komponen yang Dibutuhkan

| No | Komponen | Jumlah | Fungsi |
|----|----------|--------|--------|
| 1 | ESP32 atau Arduino UNO | 1 | Otak robot |
| 2 | Motor DC + L298N | 2 + 1 | Penggerak |
| 3 | HC-SR04 Ultrasonic | 1 | Hindari rintangan |
| 4 | DHT11 | 1 | Suhu ruangan |
| 5 | MQ-2 / MQ-135 | 1 | Deteksi gas |
| 6 | Flame Sensor | 1 | Deteksi api |
| 7 | Buzzer | 1 | Alarm |
| 8 | LCD I2C 16x2 | 1 | Display |
| 9 | Baterai 12V + Power bank | 1+1 | Power |
| 10 | Chassis robot + Roda | 1 set | Body |

## Cara Jalankan

### 1. Upload sketch robot
Buka `robot_monitor.ino` di Arduino IDE, upload ke board.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Jalankan dashboard
```bash
source /opt/ros/humble/setup.bash
python3 dashboard.py
```

### 4. Lihat semua data
```bash
ros2 topic list
ros2 topic echo /jarak
ros2 topic echo /suhu
ros2 topic echo /gas
ros2 topic echo /api
ros2 topic echo /robot_status
```

## Fitur Robot

### Mode Otomatis (default)
- Robot bergerak maju
- Jika ultrasonic < 20 cm → putar (hindari rintangan)
- Jika gas > 70 → alarm + stop
- Jika api terdeteksi → alarm + mundur

### Topic yang Dipublish
| Topic | Type | Keterangan |
|-------|------|------------|
| `/jarak` | Float64 | Jarak ke rintangan (cm) |
| `/suhu` | Float64 | Suhu ruangan (°C) |
| `/gas` | Int32 | Level gas (0-100) |
| `/api` | Bool | Api terdeteksi? |
| `/robot_status` | String | Status robot |

### Topic yang Disubscribe
| Topic | Type | Fungsi |
|-------|------|--------|
| `/robot_cmd` | String | Perintah: "MAJU", "MUNDUR", "KIRI", "KANAN", "STOP" |

## Pengembangan Lanjutan

| Ide | Deskripsi |
|-----|-----------|
| **Camera** | Tambah ESP32-CAM + stream video |
| **GPS** | Catat rute robot |
| **Wireless** | Ganti Serial ke WiFi (explore/34) |
| **ROS2 Navigation** | Integrasi dengan ROS2 Nav2 stack |
| **SLAM** | Buat peta ruangan dengan ultrasonic |
| **Voice Control** | Integrasi speech recognition |
| **Teleop** | Kontrol dari keyboard/joystick |


---

## Modul Terkait

- [Dasar ROS2 Modul 03 — Node](../../Dasar%20ROS2/modul/03-node.md) — konsep node ROS2
- [Dasar ROS2 Modul 04 — Topic](../../Dasar%20ROS2/modul/04-topic-pub-sub.md) — komunikasi pub/sub
- [Dasar ROS2 Modul 10 — Callback & Timer](../../Dasar%20ROS2/modul/10-callback-timer.md) — callback & timer periodik
- [Dasar ROS2 Modul 11 — micro-ROS](../../Dasar%20ROS2/modul/11-micro-ros.md) — ROS2 di Arduino/ESP32
- [KORELASI.md](../../Dasar%20ROS2/docs/KORELASI.md) — mapping lengkap modul ↔ komponen

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

