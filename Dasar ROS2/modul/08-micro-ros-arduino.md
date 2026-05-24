# MODUL 08: micro-ROS — ROS2 di Arduino

**TAG:** hardware / mikrokontroler / embedded

---

## APA ITU micro-ROS?

micro-ROS adalah versi ROS2 yang bisa jalan di **mikrokontroler kecil** seperti Arduino UNO.

```
PC/Laptop                              Arduino UNO
┌──────────────────┐                   ┌──────────────────┐
│  ROS2 (rclpy)    │                   │  micro-ROS       │
│  ┌────────────┐  │    Serial UART   │  ┌────────────┐  │
│  │ Talker     │◄─┼──────────────────┼─►│ Publisher   │  │
│  │ Node       │  │                   │  │ (sensor)   │  │
│  └────────────┘  │                   │  └────────────┘  │
│  ┌────────────┐  │                   │  ┌────────────┐  │
│  │ Listener   ├──┼──────────────────┼─►│ Subscriber │  │
│  │ Node       │  │                   │  │ (motor)    │  │
│  └────────────┘  │                   │  └────────────┘  │
│  ┌────────────┐  │                   │                  │
│  │ micro-ROS  │◄─┼──────────────────┼─                  │
│  │ Agent      │  │   Serial Bridge  │                  │
│  └────────────┘  │                   └──────────────────┘
└──────────────────┘
```

Komponen utama:

| Komponen | Fungsi | Jalan di |
|----------|--------|----------|
| **micro-ROS Agent** | Jembatan antara serial dan ROS2 | PC (Linux) |
| **micro-ROS Node** | Node ROS2 yang berjalan di Arduino | Arduino UNO |

---

## KENAPA ADA?

### Masalah

Arduino UNO punya spesifikasi sangat terbatas:

| Spesifikasi | Arduino UNO | PC/Laptop |
|-------------|-------------|-----------|
| RAM | 2 KB | 8+ GB |
| Flash | 32 KB | 256+ GB |
| Kecepatan | 16 MHz | 2+ GHz |

ROS2 penuh (rclpy) tidak bisa jalan di Arduino — terlalu berat.

### Solusi

micro-ROS adalah versi ROS2 yang **sangat ringan**, dirancang khusus untuk mikrokontroler.

Yang bisa dilakukan Arduino dengan micro-ROS:
- **Publish** data sensor (suhu, jarak, cahaya)
- **Subscribe** ke perintah (nyalakan LED, gerakan motor)
- **Service** sederhana (request-response)

Yang TIDAK bisa:
- Action (butuh terlalu banyak memori)
- Launch file (jalan di PC, bukan di Arduino)
- TF2 kompleks

---

## CARA KERJA

### Alur Komunikasi

```
Arduino UNO                    PC/Laptop                        ROS2 Network
  (micro-ROS node)              (micro-ROS Agent)               (ros2 topic, dll)
        │                            │                               │
        ├── publish /suhu ──────────►├── forward ke ROS2 ──────────►│
        │                            │                               │
        │◄── subscribe /led ─────────┼── dari ROS2 ─────────────────┤
        │                            │                               │
```

Arduino mengirim data sensor dengan micro-ROS → Agent menerima via serial → Agent meneruskan ke ROS2 network → Node ROS2 lain bisa membaca data itu.

### micro-ROS vs ROS2 Penuh

| Aspek | ROS2 (rclpy) | micro-ROS |
|-------|-------------|-----------|
| Hardware | PC, Raspberry Pi | Arduino, ESP32, STM32 |
| RAM butuh | 100+ MB | ~2 KB |
| Memory | Tidak masalah | Sangat terbatas |
| Bahasa | Python | C/C++ |
| Komunikasi | DDS via UDP | Serial UART |

### Transport

Arduino UNO tidak punya WiFi/Ethernet. Komunikasi via **Serial UART** (USB):

```
Arduino UNO ─── USB kabel ─── PC ─── ROS2
```

micro-ROS Agent di PC membaca data serial dan meneruskannya ke ROS2 network.

---

## INSTALASI

### 1. Instal micro-ROS Agent di PC

```bash
source /opt/ros/humble/setup.bash

# Buat workspace untuk micro-ROS agent
mkdir -p ~/microros_ws/src
cd ~/microros_ws

# Clone micro-ROS agent
git clone -b humble https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup

# Update dependencies
rosdep update
rosdep install --from-paths src --ignore-src -y

# Build
colcon build
source install/setup.bash

# Download micro-ROS agent
ros2 run micro_ros_setup create_agent_ws.sh
colcon build
source install/setup.bash
```

### 2. Instal Library Arduino

1. Buka Arduino IDE
2. **File → Preferences** → "Additional Boards Manager URLs" → tambah:
   ```
   https://raw.githubusercontent.com/micro-ROS/micro_ros_arduino/main/arduino_deps/package_micro-ros_arduino_index.json
   ```
3. **Tools → Board → Boards Manager** → cari "micro-ROS" → install
4. Pilih board: **micro-ROS Arduino**

Atau manual:
```bash
# Install micro-ROS library via git
cd ~/Arduino/libraries
git clone https://github.com/micro-ROS/micro_ros_arduino.git
```

### 3. Struktur Sketch Arduino

```
Arduino Sketch/
├── publisher.ino        ← contoh publisher
├── subscriber.ino       ← contoh subscriber
├── lib/                 ← library micro-ROS
└── README.md
```

---

## CONTOH

### Publisher Arduino — Kirim Data Sensor

```cpp
// publisher.ino — Arduino sebagai publisher ROS2
// Mengirim data sensor ke topic /suhu setiap 2 detik

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/float32.h>

rclc_executor_t executor;
rcl_node_t node;
rcl_publisher_t publisher;
std_msgs__msg__Float32 msg;

// Timer callback — dipanggil setiap 2 detik
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  // Baca sensor suhu dari pin analog (LM35 atau DHT11)
  int sensor_value = analogRead(A0);
  float suhu = sensor_value * (5.0 / 1023.0) * 100.0;  // LM35: 10mV/°C

  msg.data = suhu;
  rcl_publish(&publisher, &msg, NULL);
}

void setup() {
  // Inisialisasi micro-ROS
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Buat node
  rclc_support_t support;
  rcl_allocator_t allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);

  // Nama node: arduino_sensor_node
  rclc_node_init_default(&node, "arduino_sensor_node", "", &support);

  // Buat publisher ke topic /suhu
  rclc_publisher_init_default(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
    "suhu"
  );

  // Timer 2 detik
  rcl_timer_t timer;
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(2000), timer_callback);

  // Executor
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  // Proses callback
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
```

### Subscriber Arduino — Terima Perintah

```cpp
// subscriber.ino — Arduino sebagai subscriber ROS2
// Menerima perintah dari topic /led dan menyalakan LED

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/bool.h>

rclc_executor_t executor;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__Bool msg;

// Callback — dipanggil setiap ada pesan masuk di /led
void subscription_callback(const void *msgin) {
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;
  
  if (msg->data) {
    digitalWrite(LED_BUILTIN, HIGH);  // Nyalakan LED
  } else {
    digitalWrite(LED_BUILTIN, LOW);   // Matikan LED
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  rclc_support_t support;
  rcl_allocator_t allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);

  rclc_node_init_default(&node, "arduino_led_node", "", &support);

  // Subscribe ke topic /led
  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
    "led"
  );

  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_subscription(&executor, &subscriber, &msg, &subscription_callback, ON_NEW_DATA);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
```

### Menjalankan

```bash
# Terminal 1 — Jalankan micro-ROS Agent
source ~/microros_ws/install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0

# Terminal 2 — Cek topic dari Arduino
source /opt/ros/humble/setup.bash
ros2 topic list
ros2 topic echo /suhu

# Terminal 3 — Kirim perintah ke Arduino
ros2 topic pub /led std_msgs/msg/Bool "data: true" --once
```

---

## ERROR UMUM

| Error | Penyebab | Solusi |
|-------|----------|--------|
| `No device found` | Port salah | Cek `/dev/ttyACM0` atau `/dev/ttyUSB0` |
| `Permission denied` | Izin port | `sudo chmod 666 /dev/ttyACM0` |
| Agent tidak merespon | Baud rate salah | Pastikan Serial.begin(115200) cocok |
| Compile error | Library tidak lengkap | Install micro_ros_arduino library dengan benar |
| `Out of memory` | Sketch terlalu besar | Kurangi fitur, gunakan tipe data lebih kecil |

---

## HUBUNGAN DENGAN MODUL LAIN

- **Modul 01-06** (sourcing, workspace, package): tetap diperlukan untuk menjalankan agent
- **Modul 07** (callback/timer): timer dan callback di Arduino mirip dengan ROS2
- **explore/02 (pub-sub)**: pola komunikasi yang sama, bedanya Arduino pakai C++
- **explore/07**: praktek langsung dengan Arduino UNO

## KETERBATASAN ARDUINO UNO

Arduino UNO bisa menjalankan micro-ROS, tapi dengan keterbatasan:

| Fitur | Bisa? |
|-------|-------|
| Publisher (Float32, Int32, Bool) | ✅ |
| Subscriber (1-2 topic) | ✅ |
| Service server | ⚠️ Terbatas |
| Action | ❌ Tidak cukup RAM |
| WiFi/Internet | ❌ (butuh ESP32) |
| Banyak topic | ⚠️ Maks 3-4 topic |

**Rekomendasi:** Untuk proyek serius, gunakan ESP32 atau STM32 yang punya RAM lebih besar dan WiFi bawaan.

---

## 📁 PRAKTIK

Praktik ini menjalankan **micro-ROS** dengan Arduino UNO dari folder explore.

### Langkah 1: Buka folder explore
```
cd /mnt/e/Learn ROS2 from Scratch/Dasar ROS2/explore/07-arduino-uno/
```

### Langkah 2: Buka folder kode Arduino
Folder ini berisi dua program:
- `publisher_suhu/` — Arduino mengirim data suhu ke topic `/suhu`
- `subscriber_led/` — Arduino menerima perintah dari topic `/led`

### Langkah 3: Upload ke Arduino
1. Buka file `.ino` di Arduino IDE
2. Pilih Board: **Arduino UNO**
3. Pilih Port: `/dev/ttyACM0` atau `/dev/ttyUSB0`
4. Klik **Upload**

### Langkah 4: Terminal 1 — Jalankan micro-ROS Agent
```bash
source ~/microros_ws/install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0
```

### Langkah 5: Terminal 2 — Cek topic dari Arduino
```bash
source /opt/ros/humble/setup.bash
ros2 topic list
```

**Output yang diharapkan:**
```
/suhu
/parameter_events
/rosout
```

### Langkah 6: Terminal 2 — Lihat data suhu
```bash
ros2 topic echo /suhu
```

**Output yang diharapkan:**
```
data: 27.5
---
data: 27.6
---
...
```

### Langkah 7: Terminal 3 — Kirim perintah LED
```bash
ros2 topic pub /led std_msgs/msg/Bool "data: true" --once
```

LED di Arduino akan menyala.

**Kesimpulan:** Dengan micro-ROS, Arduino UNO bisa menjadi node ROS2 yang mempublish sensor dan menerima perintah.
