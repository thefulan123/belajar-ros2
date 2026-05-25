/*
 * servo.ino — kontrol servo via ROS2
 * 
 * Subscribe ke topic /servo (Int32)
 * 0 - 180 = sudut servo (derajat)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: Built-in Servo.h
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   Orange (Signal) | D9               | D13           (Kuning)
 *   Red (VCC)      | 5V               | 5V (Vin)      (Merah)
 *   Brown (GND)    | GND              | GND           (Hitam)
 *
 *   Lihat wiring.md untuk diagram lengkap.
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


// --- INCLUDE micro-ROS ---
// micro_ros_arduino.h: library utama micro-ROS untuk Arduino.
// Menyediakan koneksi ROS2 via Serial atau WiFi.
#include <micro_ros_arduino.h>
// rcl/rcl.h: ROS Client Library — API inti ROS2 (node, pub, sub, dll).
#include <rcl/rcl.h>
// rclc/rclc.h: tambahan convenience untuk micro-ROS (init, executor, timer).
#include <rclc/rclc.h>
// rclc/executor.h: executor — mengatur kapan callback dipanggil.
#include <rclc/executor.h>
// std_msgs/msg/int32.h: tipe pesan Int32 (integer 32-bit).
#include <std_msgs/msg/int32.h>

// Servo.h: library bawaan Arduino untuk kontrol servo PWM.
#include <Servo.h>

// #if defined(ESP32): kompilasi bersyarat untuk dual board.
// ESP32 → pin 13 (GPIO13), Arduino UNO → pin 9 (PWM-capable).
#if defined(ESP32)
  #define SERVO_PIN 13
#else
  #define SERVO_PIN 9
#endif

// Objek Servo dari library Servo.h
Servo servo;
// executor: mengelola eksekusi callback (subscriber, timer).
rclc_executor_t executor;
// support: menyimpan context ROS2 (init options, dll).
rclc_support_t support;
// allocator: pengelola memori untuk micro-ROS (default = malloc/free).
rcl_allocator_t allocator;
// node: entitas ROS2 yang berkomunikasi di topic.
rcl_node_t node;
// subscriber: pendengar untuk topic tertentu.
rcl_subscription_t subscriber;
// msg: buffer untuk menyimpan pesan yang diterima.
std_msgs__msg__Int32 msg;

// subscription_callback: dipanggil setiap ada pesan baru di topic /servo.
// msgin: pointer ke data pesan (void* → di-casting ke tipe asli).
void subscription_callback(const void *msgin) {
  // Cast dari void* ke tipe Int32 agar bisa dibaca.
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  // constrain(): batasi nilai antara 0–180 (sudut servo aman).
  int sudut = constrain(msg->data, 0, 180);
  // servo.write(): kirim sudut (derajat) ke servo.
  servo.write(sudut);
}

void setup() {
  // attach(): hubungkan objek Servo ke pin fisik.
  servo.attach(SERVO_PIN);
  // Set posisi awal ke 90° (tengah) saat startup.
  servo.write(90); // Posisi tengah saat startup

  // Serial.begin(115200): inisialisasi Serial USB di 115200 baud.
  // WAJIB sama dengan baud rate di micro-ROS agent.
  Serial.begin(115200);
  // set_microros_serial_transports(Serial): arahkan micro-ROS
  // menggunakan Serial USB sebagai transport.
  set_microros_serial_transports(Serial);
  // delay(2000): tunggu 2 detik agar micro-ROS agent siap.
  delay(2000);

  // rcl_get_default_allocator(): ambil allocator default (malloc-based).
  allocator = rcl_get_default_allocator();
  // rclc_support_init(): inisialisasi ROS2 support structure.
  rclc_support_init(&support, 0, NULL, &allocator);
  // rclc_node_init_default(): buat node ROS2 dengan nama "servo_node".
  rclc_node_init_default(&node, "servo_node", "", &support);

  // rclc_subscription_init_default(): buat subscriber untuk topic /servo.
  // ROSIDL_GET_MSG_TYPE_SUPPORT() menyediakan type support untuk Int32.
  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "servo"
  );

  // rclc_executor_init(): buat executor dengan kapasitas 1 handler.
  rclc_executor_init(&executor, &support, 1, &allocator);
  // rclc_executor_add_subscription(): daftarkan subscriber ke executor.
  // ON_NEW_DATA: callback dipanggil hanya saat ada data baru.
  rclc_executor_add_subscription(
    &executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA
  );
}

void loop() {
  // rclc_executor_spin_some(): proses callback yang tersedia.
  // RCL_MS_TO_NS(100): timeout 100 milidetik (dikonversi ke nanodetik).
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  // delay(10): jeda kecil agar tidak memenuhi CPU.
  delay(10);
}
