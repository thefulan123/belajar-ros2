/*
 * pir_motion.ino — deteksi gerakan via ROS2
 * 
 * Publish ke topic /gerakan (Bool)
 * true  = gerakan terdeteksi
 * false = tidak ada gerakan
 * 
 * Board: Arduino UNO / ESP32
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   VCC            | 5V               | 5V (via Vin)  (Merah)
 *   OUT            | D9               | D12           (Kuning)
 *   GND            | GND              | GND           (Hitam)
 *
 *   Lihat wiring.md untuk diagram lengkap.
 * 
 * CATATAN: PIR butuh stabilisasi 30-60 detik setelah power ON
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


#include <micro_ros_arduino.h>  // Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2
#include <rcl/rcl.h>            // Library ROS2 Client Library — API inti ROS2 di C
#include <rclc/rclc.h>          // Library RCLC — helper untuk memudahkan inisialisasi ROS2
#include <rclc/executor.h>      // Library executor RCLC — menjalankan callback secara periodik
#include <std_msgs/msg/bool.h>  // Tipe pesan Bool (true/false) — deteksi gerakan ya/tidak

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define PIR_PIN 12           // Pin GPIO 12 untuk ESP32
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define PIR_PIN 9            // Pin digital 9 untuk Arduino UNO
#endif

rcl_publisher_t publisher;       // Publisher — mengirim status deteksi gerakan
rclc_executor_t executor;        // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;          // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;       // Allocator — pengelola memori ROS2
rcl_node_t node;                 // Node — entitas utama ROS2 untuk komunikasi
rcl_timer_t timer;               // Timer — memicu callback secara periodik

std_msgs__msg__Bool msg;         // Variabel pesan Bool — true = gerakan terdeteksi
bool last_motion = false;        // Status gerakan sebelumnya (untuk deteksi perubahan)
unsigned long start_time = 0;    // Waktu mulai — untuk stabilisasi PIR 30 detik

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {  // Callback timer — dipanggil tiap 50ms
  (void)last_call_time;                                            // Hindari warning parameter tidak dipakai
  if (timer == NULL) return;                                       // Pastikan timer valid

  // Skip 30 detik pertama (stabilisasi PIR) — sensor butuh kalibrasi
  if (millis() < 30000) return;

  int reading = digitalRead(PIR_PIN);                              // Baca pin sensor PIR
  bool motion = (reading == HIGH);                                 // HIGH = gerakan terdeteksi

  if (motion != last_motion) {                                     // Hanya publish jika ada perubahan
    last_motion = motion;
    msg.data = motion;
    rcl_publish(&publisher, &msg, NULL);                           // Kirim ke topic "gerakan"
  }
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  pinMode(PIR_PIN, INPUT);                         // Set pin sensor PIR sebagai INPUT

  Serial.begin(115200);                            // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);          // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                     // Tunggu 2 detik agar micro-ROS siap

  allocator = rcl_get_default_allocator();         // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator);// Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "pir_node", "", &support);  // Buat node ROS2 bernama "pir_node"

  rclc_publisher_init_default(                    // Inisialisasi publisher untuk topic "gerakan"
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),  // Type support untuk Bool
    "gerakan"                                      // Nama topic
  );

  rclc_timer_init_default(                        // Buat timer periodik 50ms (20 Hz)
    &timer, &support, RCL_MS_TO_NS(50),
    timer_callback                                 // Callback pembacaan PIR
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_timer(&executor, &timer);      // Daftarkan timer ke executor
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
