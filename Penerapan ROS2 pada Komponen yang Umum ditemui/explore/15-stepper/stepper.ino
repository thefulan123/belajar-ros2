/*
 * stepper.ino — kontrol stepper motor 28BYJ-48 via ROS2
 * 
 * Subscribe ke topic /stepper (Int32)
 * > 0 = step CW, < 0 = step CCW, 0 = stop
 * 2048 step = 1 putaran (dengan gearbox 64:1)
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


#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

// Stepper.h: library bawaan Arduino untuk stepper motor.
// Mengontrol 4-phase stepper dengan urutan tertentu.
#include <Stepper.h>

#if defined(ESP32)
  #define IN1 14  // Input 1 — coil A+
  #define IN2 27  // Input 2 — coil A-
  #define IN3 26  // Input 3 — coil B+
  #define IN4 25  // Input 4 — coil B-
#else
  #define IN1 8
  #define IN2 9
  #define IN3 10
  #define IN4 11
#endif

// 28BYJ-48: 2048 steps per revolution (dengan gearbox 64:1)
const int stepsPerRev = 2048;
// Buat objek Stepper: parameter = stepsPerRev, pin IN1..IN4.
// NOTE: urutan pin IN1,IN3,IN2,IN4 sesuai driver ULN2003.
Stepper stepper(stepsPerRev, IN1, IN3, IN2, IN4);

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__Int32 msg;
int target_steps = 0;  // Jumlah step yang harus dijalankan.

void subscription_callback(const void *msgin) {
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  target_steps = msg->data;  // >0 = CW, <0 = CCW
}

void setup() {
  // setSpeed(10): kecepatan dalam RPM (revolutions per minute).
  stepper.setSpeed(10); // RPM — makin tinggi makin cepat

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "stepper_node", "", &support);

  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "stepper"
  );

  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_subscription(
    &executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA
  );
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);

  // Jika ada step yang harus dijalankan, eksekusi.
  // stepper.step() bersifat blocking — tunggu sampai selesai.
  if (target_steps != 0) {
    stepper.step(target_steps);
    target_steps = 0;  // Reset setelah selesai.
  }
}
