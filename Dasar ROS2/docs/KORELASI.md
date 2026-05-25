# KORELASI — Dasar ROS2 Modul ↔ Penerapan Komponen

Dokumen ini memetakan setiap modul **Dasar ROS2** ke komponen **Penerapan ROS2 pada Komponen** yang relevan.

---

## Ringkasan

| Modul Dasar ROS2 | Penerapan Komponen Terkait |
|:---|:---|
| [01 — Environment](modul/01-environment.md) | — (infrastruktur, tidak terkait langsung) |
| [02 — turtlesim](modul/02-turtlesim.md) | — (tutorial simulasi, tidak terkait langsung) |
| [03 — Node](modul/03-node.md) | **Semua 38 komponen** — setiap `.ino` adalah ROS2 node |
| [04 — Topic](modul/04-topic-pub-sub.md) | **Semua 38 komponen** — semua komunikasi via topic |
| [05 — Service](modul/05-service.md) | 37-system-integration, 38-final-project |
| [06 — Parameter](modul/06-parameter.md) | 37-system-integration (konfigurasi threshold) |
| [07 — Action](modul/07-action.md) | 38-final-project (navigasi robot) |
| [08 — Workspace-Package](modul/08-workspace-package.md) | micro-ROS workspace setup |
| [09 — Launch](modul/09-launch.md) | 37-system-integration, 38-final-project (multi-node) |
| [10 — Callback & Timer](modul/10-callback-timer.md) | **Semua 38 komponen** — setiap `.ino` punya callback |
| [11 — micro-ROS](modul/11-micro-ros.md) | **Semua 38 komponen** — teknologi inti |
| [12 — Custom Interfaces](modul/12-custom-interfaces.md) | 37-system-integration, 38-final-project (custom msg)

---

## Detail per Modul

### Modul 03 — Node
**Konsep:** Membuat node, memberi nama, menjalankan node.

**Komponen Penerapan:** Semua 38 komponen.
Setiap sketch diawali dengan `rclc_node_init_default(&node, "led_node", ...)`.
Di track explore Python: `rclpy.spin(node)` di setiap `*_node.py`.

### Modul 04 — Topic
**Konsep:** Publisher (kirim), Subscriber (terima), tipe pesan, topik.

**Publisher** (23 komponen sensor/input):
01-Push Button → `/tombol`,
02-Potensiometer → `/potensiometer`,
03-LDR → `/cahaya`,
04-DHT → `/suhu`, `/kelembapan`,
05-Ultrasonic → `/jarak`,
06-PIR Motion → `/gerakan`,
07-Flame Sensor → `/api`,
08-Gas Sensor → `/gas`,
09-Soil Moisture → `/kelembaban_tanah`,
10-Rain Sensor → `/hujan`,
11-Water Flow → `/debit_air`,
12-MPU6050 → `/imu`,
13-Vibration → `/getaran`,
14-Load Cell → `/berat`,
15-Joystick → `/joystick`,
16-RFID → `/rfid`,
17-Fingerprint → `/sidik_jari`,
18-Keypad → `/keypad`,
19-GPS → `/gps`,
20-Encoder → `/encoder`,
21-Microphone → `/suara`

**Subscriber** (13 komponen aktuator/output):
01-LED → `/led`,
02-Buzzer → `/buzzer`,
03-Relay → `/relay`,
04-Servo → `/servo`,
05-Motor DC → `/motor`,
06-Stepper → `/stepper`,
07-Solenoid → `/solenoid`,
08-LCD I2C → `/lcd`,
09-OLED → `/oled`,
10-NeoPixel → `/neopixel`,
11-Speaker → `/speaker`,
12-Water Pump → `/pompa`,
13-Bluetooth HC-05 → `/bluetooth`

### Modul 05 — Service
**Konsep:** Client-server communication (request/reply).

**Komponen Penerapan:**
- 37-system-integration: Smart Garden — service untuk trigger penyiraman
- 38-final-project: Robot Monitor — service untuk query status

### Modul 06 — Parameter
**Konsep:** Parameter node, get/set parameter.

**Komponen Penerapan:**
- 37-system-integration: threshold suhu/kelembaban sebagai parameter

### Modul 07 — Action
**Konsep:** Long-running task dengan feedback (goal/result/feedback).

**Komponen Penerapan:**
- 38-final-project: navigasi robot ke titik tujuan (action navigate)

### Modul 08 — Workspace-Package
**Konsep:** Membuat workspace, package, colcon build.

**Komponen Penerapan:**
- Setup `microros_ws` diperlukan sebelum menjalankan micro-ROS

### Modul 09 — Launch
**Konsep:** Menjalankan multiple node dengan satu perintah.

**Komponen Penerapan:**
- 37-system-integration: `smart_garden.py` meluncurkan sensor + aktuator
- 38-final-project: `dashboard.py` + `robot_monitor.ino` + `teleop_keyboard.py`

### Modul 10 — Callback & Timer
**Konsep:** Timer periodik, callback function.

**Komponen Penerapan:** Semua 38 komponen.
Setiap publisher di `.ino` menggunakan timer untuk publish periodik (misal 1 Hz untuk DHT).
Setiap subscriber punya callback subscription yang dipanggil otomatis.

### Modul 11 — micro-ROS
**Konsep:** ROS2 di mikrokontroler, agent, serial transport.

**Komponen Penerapan:** Semua 38 komponen.
Semua `.ino` menggunakan micro-ROS stack: `rclc_support_init`, `rclc_executor`, dll.

---

## Tabel Komponen ↔ Modul

| # | Komponen | Peran | Topic | Modul Utama |
|:---:|:---|:---:|:---|:---|
| 01 | LED | Subscriber | `/led` | 03, 04, 10, 11 |
| 02 | Push Button | Publisher | `/tombol` | 03, 04, 10, 11 |
| 03 | Buzzer | Subscriber | `/buzzer` | 03, 04, 10, 11 |
| 04 | Relay | Subscriber | `/relay` | 03, 04, 10, 11 |
| 05 | DHT Sensor | Publisher | `/suhu`, `/kelembapan` | 03, 04, 10, 11 |
| 06 | Potentiometer | Publisher | `/potensiometer` | 03, 04, 10, 11 |
| 07 | LDR | Publisher | `/cahaya` | 03, 04, 10, 11 |
| 08 | Soil Moisture | Publisher | `/kelembaban_tanah` | 03, 04, 10, 11 |
| 09 | Gas Sensor | Publisher | `/gas` | 03, 04, 10, 11 |
| 10 | Flame Sensor | Publisher | `/api` | 03, 04, 10, 11 |
| 11 | PIR Motion | Publisher | `/gerakan` | 03, 04, 10, 11 |
| 12 | Ultrasonic HC-SR04 | Publisher | `/jarak` | 03, 04, 10, 11 |
| 13 | Servo | Subscriber | `/servo` | 03, 04, 10, 11 |
| 14 | Motor DC | Subscriber | `/motor` | 03, 04, 10, 11 |
| 15 | Stepper | Subscriber | `/stepper` | 03, 04, 10, 11 |
| 16 | Solenoid | Subscriber | `/solenoid` | 03, 04, 10, 11 |
| 17 | MPU6050 | Publisher | `/imu` | 03, 04, 10, 11 |
| 18 | Vibration | Publisher | `/getaran` | 03, 04, 10, 11 |
| 19 | Load Cell | Publisher | `/berat` | 03, 04, 10, 11 |
| 20 | LCD I2C | Subscriber | `/lcd` | 03, 04, 10, 11 |
| 21 | OLED | Subscriber | `/oled` | 03, 04, 10, 11 |
| 22 | NeoPixel | Subscriber | `/neopixel` | 03, 04, 10, 11 |
| 23 | Joystick | Publisher | `/joystick` | 03, 04, 10, 11 |
| 24 | RFID | Publisher | `/rfid` | 03, 04, 10, 11 |
| 25 | Fingerprint | Publisher | `/sidik_jari` | 03, 04, 10, 11 |
| 26 | Keypad | Publisher | `/keypad` | 03, 04, 10, 11 |
| 27 | Water Flow | Publisher | `/debit_air` | 03, 04, 10, 11 |
| 28 | Rain Sensor | Publisher | `/hujan` | 03, 04, 10, 11 |
| 29 | Water Pump | Subscriber | `/pompa` | 03, 04, 10, 11 |
| 30 | Microphone | Publisher | `/suara` | 03, 04, 10, 11 |
| 31 | Speaker | Subscriber | `/speaker` | 03, 04, 10, 11 |
| 32 | Encoder | Publisher | `/encoder` | 03, 04, 10, 11 |
| 33 | GPS | Publisher | `/gps` | 03, 04, 10, 11 |
| 34 | ESP32 WiFi | Two-way | `/wifi_status` | 03, 04, 10, 11 |
| 35 | Bluetooth HC-05 | Two-way | `/bluetooth` | 03, 04, 10, 11 |
| 36 | — | — | — | — |
| 37 | System Integration | Mixed | Various | 03-11 |
| 38 | Final Project | Mixed | Various | 03-11 |

---

## Cara Menggunakan Dokumen Ini

1. **Saat belajar modul tertentu** → lihat kolom "Komponen Penerapan" untuk praktik langsung
2. **Saat mengerjakan komponen** → lihat "Modul Utama" untuk teori yang perlu dipahami
3. **Saat troubleshoot** → periksa modul 10 (callback) dan modul 11 (micro-ROS) untuk error umum
