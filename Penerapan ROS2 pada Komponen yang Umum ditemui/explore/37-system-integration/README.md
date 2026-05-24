# explore/37-system-integration — Integrasi Sistem

## Tujuan

Menggabungkan **beberapa komponen** dalam satu sistem yang terintegrasi via ROS2.

Berbeda dengan explore sebelumnya (1 komponen per folder), di sini kita jalankan **banyak node secara bersamaan** yang saling berkomunikasi via topic ROS2.

## Arsitektur

```
┌─────────────────────────────────────────────────┐
│                   PC (ROS2)                      │
│                                                   │
│  ┌─────────────┐   ┌──────────┐   ┌───────────┐  │
│  │ auto_light   │   │auto_water│   │fire_alarm │  │
│  │ (Python)     │   │ (Python) │   │ (Python)  │  │
│  └──────┬──────┘   └────┬─────┘   └─────┬─────┘  │
│         │               │               │         │
│  ┌──────┴──────┐   ┌────┴─────┐   ┌─────┴─────┐  │
│  │ /cahaya     │   │/kelembapan│   │ /api      │  │
│  └─────────────┘   │  _tanah   │   └───────────┘  │
│                    └───────────┘                   │
└────────────────────────────────────────────────────┘
         │               │               │
         ▼               ▼               ▼
┌─────────────────────────────────────────────────┐
│              Arduino (micro-ROS)                 │
│                                                   │
│  ┌──────────┐  ┌──────────────┐  ┌───────────┐  │
│  │ LDR node │  │ Soil node    │  │ Flame node│  │
│  │ (/cahaya)│  │(/kelembapan) │  │ (/api)    │  │
│  └──────────┘  └──────────────┘  └───────────┘  │
└────────────────────────────────────────────────────┘
```

## Sistem yang Bisa Dibangun

### Sistem A: Smart Garden
| Komponen | Topic | Fungsi |
|----------|-------|--------|
| Soil Moisture (08) | `/kelembapan_tanah` | Baca kelembapan |
| DHT (05) | `/suhu`, `/kelembapan` | Baca suhu/udara |
| Water Pump (29) | `/pompa` | Siram otomatis |
| Rain Sensor (28) | `/hujan` | Jangan siram saat hujan |
| LCD (20) | `/lcd` | Display status |
| LDR (07) | `/cahaya` | Kontrol lampu taman |

### Sistem B: Smart Home Security
| Komponen | Topic | Fungsi |
|----------|-------|--------|
| PIR (11) | `/gerakan` | Deteksi gerakan |
| Flame (10) | `/api` | Deteksi api |
| Gas (09) | `/gas` | Deteksi gas bocor |
| Buzzer (03) | `/buzzer` | Alarm |
| Relay (04) | `/relay` | Nyalakan lampu |
| Servo (13) | `/servo` | Buka/tutup jendela |
| NeoPixel (22) | `/neopixel` | Lampu warning |
| RFID (24) | `/rfid` | Akses kontrol |

### Sistem C: Weather Station
| Komponen | Topic | Fungsi |
|----------|-------|--------|
| DHT (05) | `/suhu`, `/kelembapan` | Suhu + RH |
| LDR (07) | `/cahaya` | Intensitas cahaya |
| Rain (28) | `/hujan` | Deteksi hujan |
| GPS (33) | `/gps_lat`, `/gps_lng` | Lokasi |
| LCD (20) | `/lcd` | Display |
| OLED (21) | `/oled` | Display grafis |
| SD Card (optional) | — | Data logging |

## Cara Jalankan

### 1. Upload semua sketch yang diperlukan
Upload sketch masing-masing komponen ke Arduino.

### 2. Jalankan agent
```bash
source ~/microros_ws/install/setup.bash
source /opt/ros/humble/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0 --baud 115200
```

### 3. Jalankan semua Python node yang diperlukan
```bash
source /opt/ros/humble/setup.bash
python3 smart_garden.py &   # Contoh
python3 display_node.py &   # Contoh
```

### 4. Verifikasi
```bash
ros2 topic list
ros2 topic echo /topic_utama
rqt_graph  # Lihat arsitektur
```

## Catatan

- **Satu Arduino UNO tidak bisa menjalankan semua sensor** — RAM/Flash terbatas
- Solusi: pakai **beberapa Arduino/ESP32**, atau colok sensor berbeda ke board berbeda
- Semua topic terintegrasi secara otomatis via ROS2 — tidak peduli dari board mana asalnya
- Arduino UNO: maks ~3-4 sensor per board (tergantung complexity)
- ESP32: bisa 5-8 sensor per board
