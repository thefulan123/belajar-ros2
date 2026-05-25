/*
 * robot_monitor.ino — robot monitoring rumah
 * 
 * PROYEK AKHIR — Menggabungkan semua komponen dari explore 01-38
 * Robot dengan sensor + aktuator terintegrasi dalam satu sistem.
 * 
 * ARSITEKTUR SISTEM:
 * ┌─────────────────────────────────────────────────────┐
 * │  PC (Python ROS2 nodes)                             │
 * │  ┌─ dashboard.py ─┐  ┌─ teleop_keyboard.py ─┐      │
 * │  │  /jarak        │  │  /robot_cmd           │      │
 * │  │  /suhu         │  │  String: MAJU/MUNDUR  │      │
 * │  │  /gas          │  │         KIRI/KANAN    │      │
 * │  │  /api          │  │         STOP/AUTO     │      │
 * │  │  /robot_status │  │         MANUAL        │      │
 * │  └────────────────┘  └───────────────────────┘      │
 * └────────────────────┬────────────────────────────────┘
 *                      │ micro-ROS (Serial)
 * ┌────────────────────▼────────────────────────────────┐
 * │  Arduino/ESP32 (robot_monitor.ino)                  │
 * │  ┌──────────┐ ┌───────┐ ┌────┐ ┌───────┐ ┌──────┐ │
 * │  │ HC-SR04  │ │ DHT11 │ │MQ-2│ │Flame  │ │Buzzer│ │
 * │  │ Jarak    │ │ Suhu  │ │Gas │ │ Api   │ │Alarm │ │
 * │  └──────────┘ └───────┘ └────┘ └───────┘ └──────┘ │
 * │  ┌──────────┐ ┌───────────────┐ ┌────────────────┐ │
 * │  │ Motor DC │ │ LCD I2C 16x2  │ │ Dua Mode:      │ │
 * │  │ L298N    │ │ Status display│ │ AUTO / MANUAL  │ │
 * │  └──────────┘ └───────────────┘ └────────────────┘ │
 * └─────────────────────────────────────────────────────┘
 * 
 * Fitur:
 * - Motor DC (L298N) — gerak maju/mundur/belok
 * - Ultrasonic HC-SR04 — hindari rintangan
 * - DHT11 — suhu ruangan
 * - MQ-2 — gas LPG/asap
 * - Flame sensor — deteksi api
 * - Buzzer — alarm
 * - LCD I2C — display status
 * 
 * Subscribe: /robot_cmd (String) — kontrol manual
 * Publish: /jarak, /suhu, /gas, /api, /robot_status
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: DHT, LiquidCrystal_I2C
 * 
 * KONEKSI FISIK (gabungan dari explore 01-38):
 * 
 *   HC-SR04   | TRIG=D2, ECHO=D3
 *   DHT11     | DATA=D7
 *   MQ-2      | AOUT=A0
 *   Flame     | DOUT=D4
 *   Buzzer    | SIG=D5
 *   Motor DC  | ENA=D9, IN1=D10, IN2=D11
 *   LCD I2C   | SDA=A4, SCL=A5
 *   
 *   Catatan: Sesuaikan pin jika terjadi konflik.
 *            Untuk ESP32, pin dapat dikustomisasi.
 * 
 * CATATAN:
 * - Kode ini PADUAN dari semua explore sebelumnya
 * - Beberapa pin mungkin conflict — sesuaikan dengan board Anda
 * - Untuk UNO, prioritaskan sensor yang paling penting
 * - Untuk ESP32, semua bisa jalan bersamaan
 */

// ═══════════════════════════════════════════════════════════════
// PENJELASAN DATA STRUCTURE — micro-ROS
// ═══════════════════════════════════════════════════════════════
//
// Berikut adalah data structure inti micro-ROS yang dipakai:
//
// 1. rcl_node_t
//    - Struktur yang merepresentasikan node ROS2 di C/C++.
//    - Setiap node punya nama unik (contoh: "led_node").
//    - Semua komunikasi ROS2 (pub/sub) terikat pada node.
//
// 2. rcl_publisher_t
//    - Struktur untuk MENGIRIM data ke topic ROS2.
//    - Diinisialisasi dengan rclc_publisher_init_default().
//    - Parameter: tipe pesan, nama topic, node.
//    - Method: rcl_publish() — kirim data.
//
// 3. rcl_subscription_t
//    - Struktur untuk MENERIMA data dari topic ROS2.
//    - Diinisialisasi dengan rclc_subscription_init_default().
//    - Parameter: tipe pesan, nama topic, callback function.
//    - Callback dipanggil OTOMATIS saat ada data masuk.
//
// 4. rclc_executor_t
//    - Struktur yang mengatur eksekusi callback.
//    - "Jantung" program micro-ROS — mirip rclpy.spin() di Python.
//    - Method: rclc_executor_spin_some() — proses callback yang pending.
//    - WAJIB ditambahkan publisher/subscriber/timer dengan add_*().
//
// 5. rclc_support_t
//    - Struktur untuk inisialisasi micro-ROS.
//    - Wajib dipanggil PERTAMA KALI di setup().
//    - rclc_support_init() — siapkan memory, allocator, dll.
//
// 6. rcl_allocator_t
//    - Struktur alokator memori untuk ROS2.
//    - rcl_get_default_allocator() — pakai default (heap).
//    - Digunakan saat inisialisasi node, publisher, subscriber.
//
// 7. rcl_timer_t
//    - Struktur timer untuk eksekusi periodik.
//    - rclc_timer_init_default() — buat timer dengan interval ms.
//    - Callback dipanggil setiap interval.
//
// 8. std_msgs__msg__*
//    - Tipe pesan ROS2 standar di C:
//      Bool    → bool data        (true/false)
//      Int32   → int32_t data     (angka bulat)
//      Float32 → float data       (angka desimal)
//      Float64 → double data      (angka desimal presisi ganda)
//      String  → char[] data      (teks)
//════════════════════════════════════════════════════════════════


// ===== LIBRARY ROS2 =====
// micro_ros_arduino: library micro-ROS untuk komunikasi ROS2 via Serial
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
// Tipe pesan ROS2 yang digunakan
#include <std_msgs/msg/float64.h>  // Untuk jarak dan suhu
#include <std_msgs/msg/int32.h>    // Untuk kadar gas
#include <std_msgs/msg/bool.h>     // Untuk status api
#include <std_msgs/msg/string.h>   // Untuk status robot dan perintah

// ===== LIBRARY KOMPONEN =====
// DHT.h: library untuk sensor suhu dan kelembaban DHT11/DHT22
#include <DHT.h>
// LiquidCrystal_I2C: library untuk LCD 16x2 dengan I2C backpack (alamat 0x27)
#include <LiquidCrystal_I2C.h>
// Wire.h: library I2C untuk komunikasi dengan LCD
#include <Wire.h>

// ===== PIN DEFINITIONS =====
// Motor DC driver L298N — kontrol motor dengan H-bridge
#define ENA_PIN 5   // PWM — kecepatan motor (analogWrite untuk speed control)
#define IN1_PIN 7   // Input 1 — arah motor (HIGH/LOW)
#define IN2_PIN 6   // Input 2 — arah motor (HIGH/LOW)
// Kombinasi: IN1=HIGH,IN2=LOW → maju; IN1=LOW,IN2=HIGH → mundur
// IN1=LOW,IN2=LOW → stop (brake)

// Ultrasonic HC-SR04 — mengukur jarak via sonar
#define TRIG_PIN 10  // Trigger — kirim pulsa ultrasonik (OUTPUT)
#define ECHO_PIN 11  // Echo — terima pantulan ultrasonik (INPUT)

// DHT11 — sensor suhu dan kelembaban
#define DHTPIN 8
#define DHTTYPE DHT11  // Tipe sensor (DHT11 atau DHT22)

// Gas MQ-2 — sensor gas LPG, asap, metana (output analog)
#define GAS_PIN A3

// Flame sensor — mendeteksi api (digital, LOW = api terdeteksi)
#define FLAME_PIN 9

// Buzzer — alarm suara (aktif dengan tone())
#define BUZZER_PIN 4

// ===== OBJEK KOMPONEN =====
// LCD I2C: alamat 0x27, 16 kolom x 2 baris
LiquidCrystal_I2C lcd(0x27, 16, 2);

// DHT: inisialisasi dengan pin dan tipe sensor
DHT dht(DHTPIN, DHTTYPE);

// ===== ROS2 SETUP =====
// 5 Publisher untuk mengirim data sensor ke ROS2
rcl_publisher_t pub_jarak, pub_suhu, pub_gas, pub_api, pub_status;
// 1 Subscription untuk menerima perintah dari ROS2
rcl_subscription_t sub_cmd;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Pesan ROS2 untuk masing-masing data
std_msgs__msg__Float64 msg_jarak, msg_suhu;  // Float64 untuk desimal
std_msgs__msg__Int32 msg_gas;                // Int32 untuk integer
std_msgs__msg__Bool msg_api;                 // Bool untuk true/false
std_msgs__msg__String msg_status, msg_cmd;   // String untuk teks
char status_buf[32];  // Buffer untuk menyusun pesan status

// ===== ROBOT STATE =====
// enum: tipe data dengan nilai terbatas — AUTO atau MANUAL
enum Mode { AUTO, MANUAL };
Mode mode = AUTO;         // Mode default: otomatis
String manual_cmd = "";   // Perintah manual terakhir (MAJU/MUNDUR/STOP)

// ===== FUNGSI SENSOR =====
// baca_jarak(): mengukur jarak dengan HC-SR04 menggunakan pulseIn
// Prinsip: kirim pulsa 10µs di TRIG, ukur durasi HIGH di ECHO
// Jarak (cm) = durasi (µs) * 0.0343 / 2 (kecepatan suara 343 m/s)
float baca_jarak() {
  digitalWrite(TRIG_PIN, LOW);            // Pastikan TRIG LOW
  delayMicroseconds(2);                    // Tunggu 2 µs
  digitalWrite(TRIG_PIN, HIGH);           // Kirim pulsa 10 µs
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);            // Akhiri pulsa
  // pulseIn: ukur panjang pulsa HIGH di ECHO_PIN, timeout 25000 µs
  long duration = pulseIn(ECHO_PIN, HIGH, 25000);
  if (duration == 0) return -1;           // Timeout / tidak ada pantulan
  return duration * 0.0343 / 2.0;         // Konversi ke cm
}

// motor_kiri(): kontrol motor kiri via L298N
// true = maju, false = mundur
void motor_kiri(bool maju) {
  if (maju) { digitalWrite(IN1_PIN, HIGH); digitalWrite(IN2_PIN, LOW); }
  else { digitalWrite(IN1_PIN, LOW); digitalWrite(IN2_PIN, HIGH); }
}

void motor_kanan(bool maju) {
  // Untuk differential steering, gunakan pin yang sama
  // Asumsi: motor kiri = IN1/IN2, motor kanan = pin lain
  // Sederhanakan: kedua motor jalan bersamaan
}

// stop_motor(): hentikan motor (IN1=IN2=LOW)
void stop_motor() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

// ===== ROS2 CALLBACKS =====

// cmd_callback: dipanggil saat ada perintah baru dari topic /robot_cmd
// Callback ini menerima perintah dari teleop_keyboard.py
// Mengatur mode AUTO/MANUAL atau perintah gerakan manual
void cmd_callback(const void *msgin) {
  // Cast dari void* ke std_msgs__msg__String
  const std_msgs__msg__String *msg = (const std_msgs__msg__String *)msgin;
  String cmd = String(msg->data.data);  // Konversi ke String Arduino
  cmd.toUpperCase();                    // Case-insensitive

  if (cmd == "AUTO") {
    mode = AUTO;          // Ganti ke mode otomatis
  } else if (cmd == "MANUAL") {
    mode = MANUAL;        // Ganti ke mode manual
  } else if (mode == MANUAL) {
    // Hanya di mode MANUAL: simpan perintah gerakan
    manual_cmd = cmd;     // "MAJU", "MUNDUR", "STOP", dll
  }
}

// lcd_display(): helper untuk menampilkan teks di LCD I2C 16x2
// lcd.clear() → hapus semua; setCursor(kolom, baris) → posisi kursor
// line1 = baris 1 (0), line2 = baris 2 (1)
void lcd_display(const char *line1, const char *line2) {
  lcd.clear();              // Hapus tampilan LCD
  lcd.setCursor(0, 0);      // Kursor ke baris 1, kolom 1
  lcd.print(line1);         // Cetak baris 1
  lcd.setCursor(0, 1);      // Kursor ke baris 2, kolom 1
  lcd.print(line2);         // Cetak baris 2
}

// timer_callback: fungsi utama yang dipanggil setiap 200 ms
// INI ADALAH JANTUNG ROBOT — semua logika kontrol ada di sini
// Membaca sensor → publish → kontrol motor/logika → update LCD → publish status
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // =================================================
  // === TAHAP 1: BACA SEMUA SENSOR ===
  // =================================================
  float jarak = baca_jarak();                    // Ultrasonic (cm)
  float suhu = dht.readTemperature();            // DHT11 (°C)
  int gas_raw = analogRead(GAS_PIN);             // MQ-2 (nilai analog mentah)
  // map: 0-1023 (ADC 10-bit) → 0-100%; constrain: batasi 0-100
  int gas_pct = constrain(map(gas_raw, 0, 1023, 0, 100), 0, 100);
  bool api = (digitalRead(FLAME_PIN) == LOW);    // Flame: LOW = api terdeteksi

  // =================================================
  // === TAHAP 2: PUBLISH DATA SENSOR KE ROS2 ===
  // =================================================
  if (jarak > 0) {                               // Validasi jarak valid
    msg_jarak.data = jarak;
    rcl_publish(&pub_jarak, &msg_jarak, NULL);   // → topic /jarak
  }
  if (!isnan(suhu)) {                            // isNaN(): cek apakah suhu valid
    msg_suhu.data = suhu;
    rcl_publish(&pub_suhu, &msg_suhu, NULL);     // → topic /suhu
  }
  msg_gas.data = gas_pct;
  rcl_publish(&pub_gas, &msg_gas, NULL);         // → topic /gas
  msg_api.data = api;
  rcl_publish(&pub_api, &msg_api, NULL);         // → topic /api

  // =================================================
  // === TAHAP 3: KONTROL ROBOT ===
  // =================================================
  // Logika bahaya: jika ada rintangan <20cm ATAU gas >70% ATAU api terdeteksi
  bool bahaya = (jarak > 0 && jarak < 20) || gas_pct > 70 || api;

  if (mode == AUTO) {
    // === MODE AUTOMATIC — robot bergerak sendiri ===
    if (bahaya) {
      // Kondisi berbahaya: STOP + alarm + tampilkan peringatan
      stop_motor();                               // Hentikan motor
      tone(BUZZER_PIN, 2000);                     // Bunyi buzzer 2 kHz
      lcd_display("! BAHAYA !", "Robot STOP");    // Tampilkan di LCD
      snprintf(status_buf, sizeof(status_buf),
               "BAHAYA: jarak=%.0f gas=%d", jarak, gas_pct);
    } else {
      // Aman: jalan maju
      motor_kiri(true);                           // Motor maju
      noTone(BUZZER_PIN);                         // Matikan buzzer
      lcd_display("Robot Monitor", "BERJALAN...");// Tampilkan di LCD
      snprintf(status_buf, sizeof(status_buf),
               "BERJALAN: %.0fcm", jarak);
    }
  } else {
    // === MODE MANUAL — robot dikendalikan dari keyboard ===
    // Perintah manual dikirim dari teleop_keyboard.py via /robot_cmd
    if (manual_cmd == "MAJU") motor_kiri(true);         // Maju
    else if (manual_cmd == "MUNDUR") motor_kiri(false); // Mundur
    else if (manual_cmd == "STOP") stop_motor();        // Berhenti
    // Status: tampilkan perintah manual terakhir
    snprintf(status_buf, sizeof(status_buf),
             "MANUAL: %s", manual_cmd.c_str());
  }

  // =================================================
  // === TAHAP 4: PUBLISH STATUS KE ROS2 ===
  // =================================================
  msg_status.data.data = status_buf;     // Pointer ke string status
  msg_status.data.size = strlen(status_buf);  // Panjang string
  rcl_publish(&pub_status, &msg_status, NULL);  // → topic /robot_status
}

// ===== SETUP =====
void setup() {
  // ===== INISIALISASI PIN =====
  // Motor pin: semua OUTPUT
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  // Ultrasonic: TRIG = OUTPUT, ECHO = INPUT
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  // Flame sensor: INPUT (membaca sinyal digital)
  pinMode(FLAME_PIN, INPUT);
  // Buzzer: OUTPUT
  pinMode(BUZZER_PIN, OUTPUT);
  // analogWrite: atur kecepatan motor via PWM (0-255), 200 = ~78%
  analogWrite(ENA_PIN, 200);
  stop_motor();  // Pastikan motor mati saat startup

  // ===== LCD I2C =====
  lcd.init();               // Inisialisasi LCD
  lcd.backlight();          // Nyalakan backlight
  lcd_display("Robot Monitor", "ROSmicro v1.0");  // Tampilkan splash screen

  // ===== SENSOR DHT =====
  dht.begin();  // Inisialisasi sensor DHT11

  // ===== SERIAL + MICRO-ROS =====
  Serial.begin(115200);                    // Inisialisasi Serial pada 115200 baud
  set_microros_serial_transports(Serial);  // Transport micro-ROS via Serial
  delay(2000);                             // Tunggu micro-ROS agent siap

  // ===== ROS2 NODE =====
  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "robot_node", "", &support);

  // ===== PUBLISHER (5 topic) =====
  rclc_publisher_init_default(&pub_jarak, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "jarak");
  rclc_publisher_init_default(&pub_suhu, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "suhu");
  rclc_publisher_init_default(&pub_gas, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "gas");
  rclc_publisher_init_default(&pub_api, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool), "api");
  rclc_publisher_init_default(&pub_status, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String), "robot_status");

  // ===== SUBSCRIBER (1 topic) =====
  // Menerima perintah dari teleop_keyboard.py
  rclc_subscription_init_default(&sub_cmd, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String), "robot_cmd");

  // ===== TIMER + EXECUTOR =====
  // Timer 200 ms — interval pembacaan sensor dan kontrol robot
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(200), timer_callback);
  // Executor dengan 2 handle: 1 subscription + 1 timer
  rclc_executor_init(&executor, &support, 2, &allocator);
  rclc_executor_add_subscription(&executor, &sub_cmd, &msg_cmd,
    &cmd_callback, ON_NEW_DATA);
  rclc_executor_add_timer(&executor, &timer);
}

// ===== LOOP =====
void loop() {
  // rclc_executor_spin_some: proses callback yang siap jalan (non-blocking)
  // Timeout 100 ms — tidak memblokir loop Arduino
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);  // Jeda kecil untuk stabilitas serial
}
