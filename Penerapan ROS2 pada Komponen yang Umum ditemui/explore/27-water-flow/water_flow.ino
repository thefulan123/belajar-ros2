/*
 * water_flow.ino — baca debit air YF-S201 via ROS2
 * 
 * Publish:
 * /debit_air (Float64)  — L/min
 * /volume_air (Float64) — total Liter
 * 
 * Board: Arduino UNO / ESP32
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   Red (VCC)      | 5V               | 5V (Vin)      (Merah)
 *   Black (GND)    | GND              | GND           (Hitam)
 *   Yellow (Signal) | D2 (interrupt)   | D14 (interrupt)  (Kuning)
 *
 *   Lihat wiring.md untuk diagram lengkap.
 * 
 * Rumus: Setiap pulse = 2.25 mL
 *        Frekuensi (Hz) / 7.5 = L/min
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


// Include library micro-ROS Arduino — menyediakan semua fungsi ROS2 untuk board Arduino
#include <micro_ros_arduino.h>
// RCL: ROS Client Library — API inti untuk node, publisher, subscriber
#include <rcl/rcl.h>
// RCLC: convenience layer di atas RCL — memudahkan inisialisasi
#include <rclc/rclc.h>
// Executor: mengatur eksekusi callback (timer, subscription) secara bergantian
#include <rclc/executor.h>
// Tipe pesan Float64 — digunakan untuk publish data desimal (debit & volume)
#include <std_msgs/msg/float64.h>

// #if defined(ESP32) →预处理: mengecek apakah board yang digunakan adalah ESP32
// Jika ESP32, pakai pin GPIO 14; jika UNO, pakai pin D2
// Ini membuat sketch kompatibel dengan dual board tanpa perlu edit manual
#if defined(ESP32)
  #define FLOW_PIN 14
#else
  #define FLOW_PIN 2
#endif

// Deklarasi publisher ROS2 — objek untuk mengirim pesan ke topic tertentu
rcl_publisher_t pub_debit;
rcl_publisher_t pub_volume;
// Executor — menjadwalkan kapan timer_callback dipanggil
rclc_executor_t executor;
// Support — wadah untuk inisialisasi rclc (menampung allocator, dll)
rclc_support_t support;
// Allocator — pengelola memori untuk rclc (menggunakan default)
rcl_allocator_t allocator;
// Node — identitas unik di jaringan ROS2, semua pub/sub terdaftar di sini
rcl_node_t node;
// Timer — memicu callback secara periodik (di sini setiap 1 detik)
rcl_timer_t timer;

// Variabel pesan ROS2 untuk Float64 — .data menampung nilai float yang akan dikirim
std_msgs__msg__Float64 msg_debit;
std_msgs__msg__Float64 msg_volume;

// volatile: memberitahu compiler bahwa variabel ini bisa berubah dari ISR (interrupt)
// Tanpa volatile, compiler bisa mengoptimasi (cache) nilai dan menyebabkan bug
volatile long pulse_count = 0;
// Menyimpan pulse_count dari pembacaan sebelumnya untuk menghitung delta
long last_pulse_count = 0;
// Timestamp terakhir kali callback dijalankan (millis)
unsigned long last_time = 0;
// Volume total yang sudah mengalir, dalam satuan Liter
float total_volume = 0;

// IRAM_ATTR: untuk ESP32, fungsi interrupt harus ditaruh di IRAM (RAM instruksi)
// Ini adalah Interrupt Service Routine (ISR) — dipanggil setiap ada pulsa dari sensor
// Hanya increment counter — ISR harus singkat!
void IRAM_ATTR pulse_counter() {
  pulse_count++;
}

// timer_callback: fungsi yang dipanggil oleh timer setiap 1000 ms
// rcl_timer_t *timer: pointer ke timer yang memicu callback
// int64_t last_call_time: waktu terakhir callback dipanggil (dalam nanodetik)
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  // (void)last_call_time: casting ke void untuk menghilangkan warning unused parameter
  (void)last_call_time;
  // Safety check: jika timer NULL, keluar (mencegah crash)
  if (timer == NULL) return;

  // millis(): fungsi Arduino yang mengembalikan jumlah ms sejak board menyala
  unsigned long now = millis();
  // Pastikan jeda minimal 1 detik sebelum menghitung ulang
  if (now - last_time < 1000) return;

  // Hitung jumlah pulse yang terjadi sejak pembacaan terakhir
  long pulses = pulse_count - last_pulse_count;
  // Update nilai referensi untuk siklus berikutnya
  last_pulse_count = pulse_count;
  last_time = now;

  // Flow rate: setiap pulse = 2.25 mL
  // Freq (Hz) = pulses per second
  // L/min = (pulses * 2.25 / 1000) * 60 = pulses * 0.135
  float flow = pulses * 0.135; // L/min

  // Total volume
  // 1 pulse = 2.25 mL = 0.00225 Liter
  total_volume += pulses * 0.00225;

  // Isi pesan ROS2 dengan data yang akan dipublish
  msg_debit.data = flow;
  msg_volume.data = total_volume;

  // rcl_publish: kirim pesan ke topic melalui publisher
  // Parameter: publisher, pointer ke message, pointer ke allocation (NULL = default)
  rcl_publish(&pub_debit, &msg_debit, NULL);
  rcl_publish(&pub_volume, &msg_volume, NULL);
}

void setup() {
  // pinMode: konfigurasi pin sebagai INPUT, OUTPUT, atau INPUT_PULLUP
  // INPUT_PULLUP: mengaktifkan resistor pull-up internal agar tidak floating
  pinMode(FLOW_PIN, INPUT_PULLUP);
  // attachInterrupt: mendaftarkan fungsi ISR ke pin tertentu
  // digitalPinToInterrupt: konversi nomor pin ke nomor interrupt
  // RISING: interrupt dipicu saat sinyal naik dari LOW ke HIGH
  attachInterrupt(digitalPinToInterrupt(FLOW_PIN), pulse_counter, RISING);

  // Serial.begin(115200): inisialisasi komunikasi serial dengan baud rate 115200
  // micro-ROS menggunakan Serial sebagai transport data ROS2
  Serial.begin(115200);
  // set_microros_serial_transports: memberitahu micro-ROS untuk pakai Serial
  // Fungsi ini menghubungkan ROS2 node dengan physical Serial port
  set_microros_serial_transports(Serial);
  // delay(2000): tunggu 2 detik agar Serial siap dan agent micro-ROS terhubung
  delay(2000);

  // rcl_get_default_allocator: ambil allocator default (biasanya malloc/free)
  allocator = rcl_get_default_allocator();
  // rclc_support_init: inisialisasi support structure dengan allocator
  rclc_support_init(&support, 0, NULL, &allocator);
  // rclc_node_init_default: buat node ROS2 dengan nama "water_flow_node"
  // Parameter: pointer node, nama node, namespace ("" = root), pointer support
  rclc_node_init_default(&node, "water_flow_node", "", &support);

  // rclc_publisher_init_default: buat publisher untuk topic
  // Parameter: publisher, node, tipe message (via ROSIDL), nama topic
  // ROSIDL_GET_MSG_TYPE_SUPPORT: macro untuk mendapatkan type support dari pesan
  rclc_publisher_init_default(&pub_debit, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "debit_air");
  rclc_publisher_init_default(&pub_volume, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "volume_air");

  // rclc_timer_init_default: buat timer periodik (1 detik = RCL_MS_TO_NS(1000))
  // RCL_MS_TO_NS: konversi milidetik ke nanodetik (waktu ROS2 internal)
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(1000), timer_callback);
  // rclc_executor_init: inisialisasi executor dengan kapasitas 1 handle
  rclc_executor_init(&executor, &support, 1, &allocator);
  // rclc_executor_add_timer: daftarkan timer ke executor agar dijalankan periodik
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  // rclc_executor_spin_some: proses callback yang tersedia (non-blocking)
  // Berbeda dengan rclpy.spin() yang blocking, spin_some hanya sekali jalan
  // RCL_MS_TO_NS(100): timeout 100 ms — tunggu callback maks 100 ms
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  // delay(10): jeda 10 ms — memberi waktu bagi microcontroller untuk hal lain
  // Juga membantu stabilitas komunikasi serial micro-ROS
  delay(10);
}
