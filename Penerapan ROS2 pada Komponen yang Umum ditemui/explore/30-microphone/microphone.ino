/*
 * microphone.ino — baca level suara via ROS2
 * 
 * Publish ke topic /suara (Int32) — 0 (senyap) s/d 100 (keras)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   VCC            | 5V               | 3.3V          (Merah)
 *   GND            | GND              | GND           (Hitam)
 *   AOUT (analog)  | A0               | GPIO36        (Kuning)
 *   DOUT (digital) | —                | —             (—)
 *
 *   Lihat wiring.md untuk diagram lengkap.
 * 
 * Cara kerja:
 * - Mikrofon electret dengan amplifier LM393 menghasilkan tegangan analog
 * - Nilai analog proporsional dengan amplitudo suara
 * - Dilakukan peak detection (ambil nilai maks dari 10 sampel)
 * - Hasil dipetakan ke skala 0-100%
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


// micro_ros_arduino.h: library utama micro-ROS untuk board Arduino
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
// std_msgs/msg/int32.h: tipe pesan integer 32-bit untuk ROS2
#include <std_msgs/msg/int32.h>

// #if defined(ESP32): pengecekan board saat kompilasi
// ESP32: GPIO 36 (ADC1_CH0, input analog); UNO: pin A0
// ESP32 punya ADC 12-bit (0-4095), UNO punya ADC 10-bit (0-1023)
#if defined(ESP32)
  #define MIC_PIN 36
#else
  #define MIC_PIN A0
#endif

// Publisher — mengirim data ke topic "/suara"
rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;
// Pesan bertipe Int32 — cocok untuk nilai 0-100
std_msgs__msg__Int32 msg;
// last_val: menyimpan nilai sebelumnya untuk deteksi perubahan
// Diinisialisasi -1 agar publish pertama selalu terjadi
int last_val = -1;

// Fungsi sample_peak: mengambil sampel 10 kali dan mengembalikan nilai maksimum
// Teknik peak detection — berguna untuk menangkap puncak suara (seperti tepukan)
int sample_peak() {
  int max_val = 0;
  for (int i = 0; i < 10; i++) {
    // analogRead: baca nilai analog dari pin (0-1023 UNO, 0-4095 ESP32)
    int v = analogRead(MIC_PIN);
    if (v > max_val) max_val = v;
    // delayMicroseconds: jeda 100 mikrodetik antar sampel
    delayMicroseconds(100);
  }
  return max_val;
}

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  int raw = sample_peak();
  // map: memetakan nilai dari satu rentang ke rentang lain
  // map(value, fromLow, fromHigh, toLow, toHigh)
  // ESP32: 0-4095 → 0-100; UNO: 0-1023 → 0-100
  #if defined(ESP32)
    int pct = map(raw, 0, 4095, 0, 100);
  #else
    int pct = map(raw, 0, 1023, 0, 100);
  #endif
  // constrain: membatasi nilai agar tetap dalam rentang 0-100
  // Jika nilai < 0 → 0; jika > 100 → 100
  pct = constrain(pct, 0, 100);

  // abs: nilai absolut dari selisih — cek apakah perubahan signifikan
  // Hanya publish jika perubahan >= 3% (mencegah noise/fluktuasi kecil)
  if (abs(pct - last_val) >= 3) {
    last_val = pct;
    msg.data = pct;
    rcl_publish(&publisher, &msg, NULL);
  }
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "mic_node", "", &support);

  rclc_publisher_init_default(&publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "suara");

  // Timer interval 50 ms — setara dengan 20 Hz pembacaan
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(50), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
