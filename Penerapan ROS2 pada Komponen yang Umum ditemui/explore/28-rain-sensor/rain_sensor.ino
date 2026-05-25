/*
 * rain_sensor.ino — deteksi hujan/air via ROS2
 * 
 * Publish ke topic /hujan (Bool)
 * true  = hujan/air terdeteksi
 * false = kering
 * 
 * Board: Arduino UNO / ESP32
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   VCC            | 5V               | 5V (Vin)      (Merah)
 *   GND            | GND              | GND           (Hitam)
 *   DO (digital)   | D4               | D14           (Kuning)
 *   AO (analog)    | —                | —             (—)
 *
 *   Lihat wiring.md untuk diagram lengkap.
 * 
 * Cara kerja sensor hujan:
 * - Sensor mengeluarkan LOW jika ada air (konduktif)
 * - Sensor mengeluarkan HIGH jika kering
 * - Gunakan pin digital (DO), bukan analog (AO)
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


// Include library micro-ROS Arduino sebagai jembatan antara Arduino dan ROS2
#include <micro_ros_arduino.h>
// RCL adalah ROS Client Library — API inti ROS2 dalam C
#include <rcl/rcl.h>
// RCLC — layer kemudahan di atas RCL untuk inisialisasi
#include <rclc/rclc.h>
// Executor — mengatur eksekusi callback (timer/subscription)
#include <rclc/executor.h>
// Tipe pesan Bool — bernilai true atau false
#include <std_msgs/msg/bool.h>

// #if defined(ESP32): cek apakah board ESP32 atau bukan
// Jika ESP32: pin GPIO 14; jika UNO: pin D4
// Mekanisme kompilasi bersyarat untuk mendukung dual board
#if defined(ESP32)
  #define RAIN_PIN 14
#else
  #define RAIN_PIN 4
#endif

// Publisher ROS2 — mengirim data Bool ke topic "hujan"
rcl_publisher_t publisher;
// Executor — penjadwal callback
rclc_executor_t executor;
// Support — wadah inisialisasi rclc
rclc_support_t support;
// Allocator — pengelola alokasi memori
rcl_allocator_t allocator;
// Node — identitas node di jaringan ROS2
rcl_node_t node;
// Timer — memicu timer_callback setiap 200 ms
rcl_timer_t timer;
// Pesan ROS2 bertipe Bool — field .data berisi true/false
std_msgs__msg__Bool msg;
// Variabel untuk deteksi perubahan state (edge detection)
// Hanya publish jika status hujan berubah, tidak setiap saat
bool last_rain = false;

// timer_callback: dipanggil oleh executor setiap 200 ms
// rcl_timer_t *timer: pointer ke timer yang memicu
// int64_t last_call_time: timestamp panggilan sebelumnya (ns)
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // digitalRead: baca nilai digital dari pin sensor
  // LOW = ada air (sensor konduktif menghubungkan ke ground)
  bool rain = (digitalRead(RAIN_PIN) == LOW);
  // Hanya publish jika ada perubahan (mencegah spam ROS2 message)
  if (rain != last_rain) {
    last_rain = rain;
    msg.data = rain;
    // rcl_publish: kirim pesan ke topic melalui publisher
    rcl_publish(&publisher, &msg, NULL);
  }
}

void setup() {
  // pinMode: set pin RAIN_PIN sebagai INPUT (membaca sinyal digital)
  pinMode(RAIN_PIN, INPUT);

  // Serial.begin: inisialisasi komunikasi serial pada 115200 baud
  // micro-ROS menggunakan koneksi serial ini sebagai transport
  Serial.begin(115200);
  // set_microros_serial_transports: konfigurasi transport micro-ROS via Serial
  set_microros_serial_transports(Serial);
  // delay: beri waktu 2 detik untuk inisialisasi micro-ROS
  delay(2000);

  // rcl_get_default_allocator: dapatkan allocator default (malloc)
  allocator = rcl_get_default_allocator();
  // rclc_support_init: inisialisasi support structure
  rclc_support_init(&support, 0, NULL, &allocator);
  // rclc_node_init_default: buat node ROS2 bernama "rain_node"
  rclc_node_init_default(&node, "rain_node", "", &support);

  // rclc_publisher_init_default: daftarkan publisher ke topic "hujan"
  // ROSIDL_GET_MSG_TYPE_SUPPORT: macro untuk mengambil type support pesan
  rclc_publisher_init_default(&publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool), "hujan");

  // rclc_timer_init_default: buat timer dengan interval 200 ms
  // RCL_MS_TO_NS(200): konversi 200 ms ke nanodetik
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(200), timer_callback);
  // rclc_executor_init: inisialisasi executor dengan kapasitas 1 handle
  rclc_executor_init(&executor, &support, 1, &allocator);
  // rclc_executor_add_timer: daftarkan timer ke executor
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  // rclc_executor_spin_some: proses callback yang siap jalan (non-blocking)
  // Timeout 100 ms: jika tidak ada callback, tunggu maks 100 ms lalu lanjut
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  // delay(10): jeda kecil untuk stabilitas sistem dan komunikasi serial
  delay(10);
}
