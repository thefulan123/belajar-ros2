/*
 * relay.ino — kontrol relay via ROS2
 * 
 * Subscribe ke topic /relay (Bool)
 * true  → relay ON (COM terhubung NO)
 * false → relay OFF
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
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
#include <std_msgs/msg/bool.h>  // Tipe pesan Bool (true/false) — untuk ON/OFF relay

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define RELAY_PIN 33         // Pin GPIO 33 untuk ESP32
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define RELAY_PIN 6          // Pin digital 6 untuk Arduino UNO
#endif

rclc_executor_t executor;         // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;           // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;        // Allocator — pengelola memori ROS2
rcl_node_t node;                  // Node — entitas utama ROS2 untuk komunikasi
rcl_subscription_t subscriber;    // Subscriber — penerima pesan dari topic
std_msgs__msg__Bool msg;          // Variabel pesan Bool — menampung perintah ON/OFF

void subscription_callback(const void *msgin) {              // Callback — dipanggil otomatis saat ada pesan masuk
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;  // Cast pointer ke tipe Bool
  digitalWrite(RELAY_PIN, msg->data ? HIGH : LOW);          // true → relay ON (HIGH), false → relay OFF (LOW)
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  pinMode(RELAY_PIN, OUTPUT);                      // Set pin relay sebagai OUTPUT (mengirim sinyal)
  digitalWrite(RELAY_PIN, LOW);                    // Pastikan relay OFF saat awal

  Serial.begin(115200);                            // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);          // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                     // Tunggu 2 detik agar micro-ROS siap

  allocator = rcl_get_default_allocator();         // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator);// Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "relay_node", "", &support);  // Buat node ROS2 bernama "relay_node"

  rclc_subscription_init_default(                 // Inisialisasi subscriber untuk topic "relay"
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),  // Dapatkan type support untuk pesan Bool
    "relay"                                       // Nama topic yang akan di-subscribe
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_subscription(                 // Daftarkan subscriber ke executor
    &executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA           // Callback dipanggil hanya saat ada data baru
  );
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
