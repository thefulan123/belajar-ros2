/*
 * water_pump.ino — kontrol pompa air via ROS2 (via relay)
 * 
 * Subscribe ke topic /pompa (Bool)
 * true  = pompa ON
 * false = pompa OFF
 * 
 * Board: Arduino UNO / ESP32
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   IN             | D6               | D33           (Kuning)
 *   VCC            | 5V               | 3.3V          (Merah)
 *   GND            | GND              | GND           (Hitam)
 *
 *   Lihat wiring.md untuk diagram lengkap.
 * 
 * Catatan:
 * - Pompa DC dikontrol via relay module
 * - Relay aktif LOW atau HIGH tergantung modul
 * - Gunakan pin yang bisa memberikan arus cukup via transistor/relay
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


// micro_ros_arduino: library inti untuk menjalankan ROS2 client di Arduino
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
// std_msgs/msg/bool.h: tipe pesan Boolean untuk ROS2
#include <std_msgs/msg/bool.h>

// Definisi pin pompa — berbeda antara ESP32 dan Arduino UNO
// ESP32: GPIO 33; UNO: pin D6
#if defined(ESP32)
  #define PUMP_PIN 33
#else
  #define PUMP_PIN 6
#endif

// Executor — mengatur eksekusi callback
rclc_executor_t executor;
// Support — wadah untuk inisialisasi
rclc_support_t support;
// Allocator — pengelola memori
rcl_allocator_t allocator;
// Node — identitas node di ROS2
rcl_node_t node;
// Subscription — penerima pesan dari topic "/pompa"
rcl_subscription_t subscriber;
// Pesan ROS2 bertipe Bool — .data menyimpan perintah ON/OFF
std_msgs__msg__Bool msg;

// subscription_callback: dipanggil setiap ada pesan baru di topic "/pompa"
// const void *msgin: pointer ke data mentah, harus di-cast ke tipe yang benar
void subscription_callback(const void *msgin) {
  // Cast pointer void → pointer ke std_msgs__msg__Bool
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;
  // digitalWrite: atur output pin pompa
  // Jika msg->data == true → HIGH (ON); jika false → LOW (OFF)
  digitalWrite(PUMP_PIN, msg->data ? HIGH : LOW);
}

void setup() {
  // pinMode: set pin pompa sebagai OUTPUT untuk mengontrol relay
  pinMode(PUMP_PIN, OUTPUT);
  // digitalWrite: atur output ke LOW (pompa mati saat startup)
  digitalWrite(PUMP_PIN, LOW);

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "water_pump_node", "", &support);

  // rclc_subscription_init_default: daftarkan subscriber ke topic "pompa"
  // Berbeda dengan publisher, subscriber menerima (bukan mengirim) pesan
  rclc_subscription_init_default(&subscriber, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool), "pompa");

  // rclc_executor_init: inisialisasi executor dengan kapasitas 1 handle
  rclc_executor_init(&executor, &support, 1, &allocator);
  // rclc_executor_add_subscription: daftarkan subscription ke executor
  // Setiap ada pesan baru → panggil subscription_callback
  // ON_NEW_DATA: hanya proses saat ada data baru (bukan setiap spin)
  rclc_executor_add_subscription(&executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA);
}

void loop() {
  // rclc_executor_spin_some: proses callback yang tersedia
  // Untuk subscriber, ini akan memanggil subscription_callback jika ada data
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
