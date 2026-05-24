/*
 * encoder.ino — baca rotary encoder KY-040 via ROS2
 * 
 * Publish:
 * /encoder (Int32) — posisi counter
 * /encoder_button (Bool) — true = ditekan
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 * 
 * Cara kerja rotary encoder:
 * - CLK (clock) dan DT (data) adalah dua pin output quadrature
 * - Memutar ke kanan: CLK berubah duluan sebelum DT
 * - Memutar ke kiri: DT berubah duluan sebelum CLK
 * - SW (switch): tombol internal yang aktif LOW
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


#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>   // Untuk posisi encoder (counter)
#include <std_msgs/msg/bool.h>    // Untuk status tombol

// Konfigurasi pin untuk dual board
// ESP32: GPIO 14 (CLK), 27 (DT), 26 (SW)
// UNO: pin 2 (CLK), 3 (DT), 4 (SW)
// Hanya CLK yang bisa interrupt di UNO (pin 2-3)
#if defined(ESP32)
  #define CLK_PIN 14
  #define DT_PIN 27
  #define SW_PIN 26
#else
  #define CLK_PIN 2
  #define DT_PIN 3
  #define SW_PIN 4
#endif

rcl_publisher_t pub_enc;     // Publisher untuk topic "/encoder"
rcl_publisher_t pub_btn;     // Publisher untuk topic "/encoder_button"
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

std_msgs__msg__Int32 msg_enc;  // Pesan untuk posisi (Int32)
std_msgs__msg__Bool msg_btn;   // Pesan untuk tombol (Bool)

// volatile: nilai bisa berubah dari ISR kapan saja — jangan di-cache compiler
volatile int counter = 0;      // Posisi encoder (diubah dari interrupt)
volatile int last_clk = HIGH;  // State CLK sebelumnya (diubah dari interrupt)
bool last_btn = false;         // State tombol sebelumnya (untuk edge detection)
int last_counter = 0;          // Counter sebelumnya (untuk deteksi perubahan)

// IRAM_ATTR: untuk ESP32, fungsi ISR harus di IRAM
// handle_encoder: ISR yang dipanggil saat CLK berubah (CHANGE)
// Membaca DT untuk menentukan arah putaran
void IRAM_ATTR handle_encoder() {
  int clk = digitalRead(CLK_PIN);  // Baca state CLK saat ini
  if (clk != last_clk) {           // Ada perubahan pada CLK (edge)
    // Prinsip quadrature: jika DT != CLK → clockwise, jika sama → counter-clockwise
    if (digitalRead(DT_PIN) != clk) {
      counter++;  // Putar ke kanan (clockwise)
    } else {
      counter--;  // Putar ke kiri (counter-clockwise)
    }
  }
  last_clk = clk;  // Update state untuk deteksi edge berikutnya
}

// timer_callback: dipanggil setiap 50 ms untuk publish data ke ROS2
// ISR hanya mengupdate counter — publish dilakukan di sini (bukan di ISR)
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // Publish posisi encoder hanya jika berubah
  if (counter != last_counter) {
    last_counter = counter;
    msg_enc.data = counter;
    rcl_publish(&pub_enc, &msg_enc, NULL);
  }

  // Baca tombol — LOW = ditekan (INPUT_PULLUP)
  bool btn = (digitalRead(SW_PIN) == LOW);
  if (btn != last_btn) {  // Edge detection: hanya publish saat berubah
    last_btn = btn;
    msg_btn.data = btn;
    rcl_publish(&pub_btn, &msg_btn, NULL);
  }
}

void setup() {
  // Konfigurasi pin CLK dan DT sebagai INPUT
  pinMode(CLK_PIN, INPUT);
  pinMode(DT_PIN, INPUT);
  // SW pakai INPUT_PULLUP — tombol mengkoneksikan ke GND (active LOW)
  pinMode(SW_PIN, INPUT_PULLUP);
  // Inisialisasi last_clk dengan state awal
  last_clk = digitalRead(CLK_PIN);
  // attachInterrupt: panggil handle_encoder setiap ada perubahan pada CLK
  // CHANGE: interrupt dipicu saat pin berubah (LOW→HIGH atau HIGH→LOW)
  attachInterrupt(digitalPinToInterrupt(CLK_PIN), handle_encoder, CHANGE);

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "encoder_node", "", &support);

  // Daftarkan dua publisher: "/encoder" (Int32) dan "/encoder_button" (Bool)
  rclc_publisher_init_default(&pub_enc, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "encoder");
  rclc_publisher_init_default(&pub_btn, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool), "encoder_button");

  // Timer interval 50 ms — cukup responsif untuk deteksi putaran
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(50), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
