/*
 * motor_dc.ino — kontrol motor DC via ROS2 (driver L298N)
 * 
 * Subscribe ke topic /motor_kecepatan (Int32) dan /motor_arah (Bool)
 * Kecepatan: 0 (stop) - 100 (full)
 * Arah: true = maju, false = mundur
 * 
 * Board: Arduino UNO / ESP32
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   IN1            | D7               | D32           (Kuning)
 *   IN2            | D6               | D33           (Hijau)
 *   ENA (PWM)      | D5 (PWM)         | D25           (Biru)
 *   VCC (12V)      | —                | —             (Merah)
 *   GND            | GND              | GND           (Hitam)
 *   5V output      | (optional)       | (optional)    (—)
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


// micro_ros_arduino.h: library utama micro-ROS untuk Arduino.
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
// std_msgs/msg/int32.h: tipe pesan Int32 untuk kecepatan (0–100).
#include <std_msgs/msg/int32.h>
// std_msgs/msg/bool.h: tipe pesan Bool untuk arah (true/false).
#include <std_msgs/msg/bool.h>

// Dual board pin mapping:
// ESP32 → GPIO 25,32,33 | Arduino UNO → pin 5,7,6
#if defined(ESP32)
  #define ENA_PIN 25   // Enable/PWM — mengatur kecepatan
  #define IN1_PIN 32   // Input 1 — kontrol arah motor
  #define IN2_PIN 33   // Input 2 — kontrol arah motor
#else
  #define ENA_PIN 5
  #define IN1_PIN 7
  #define IN2_PIN 6
#endif

// Variabel global ROS2
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

// Dua subscriber: satu untuk kecepatan, satu untuk arah.
rcl_subscription_t sub_kecepatan;
rcl_subscription_t sub_arah;
std_msgs__msg__Int32 msg_kecepatan;
std_msgs__msg__Bool msg_arah;

// State motor saat ini.
int current_speed = 0;          // 0–100 (persentase)
bool current_direction = true;  // true = maju, false = mundur

// update_motor(): terapkan kecepatan & arah ke driver L298N.
void update_motor() {
  // map(): skala 0–100 → 0–255 (PWM 8-bit).
  int pwm = map(current_speed, 0, 100, 0, 255);
  pwm = constrain(pwm, 0, 255);
  // analogWrite(): kirim sinyal PWM ke pin Enable.
  analogWrite(ENA_PIN, pwm);

  // Kontrol H-Bridge: IN1 HIGH + IN2 LOW = maju, kebalikannya = mundur.
  if (current_direction) {
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
  } else {
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, HIGH);
  }
}

// cb_kecepatan: callback saat ada pesan baru di /motor_kecepatan.
void cb_kecepatan(const void *msgin) {
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  current_speed = constrain(msg->data, 0, 100);
  update_motor();
}

// cb_arah: callback saat ada pesan baru di /motor_arah.
void cb_arah(const void *msgin) {
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;
  current_direction = msg->data;
  update_motor();
}

void setup() {
  // Set pin mode: OUTPUT untuk semua pin motor.
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  // Pastikan motor mati saat startup.
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENA_PIN, 0);

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "motor_node", "", &support);

  // Inisialisasi subscriber untuk /motor_kecepatan (Int32).
  rclc_subscription_init_default(
    &sub_kecepatan, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "motor_kecepatan"
  );

  // Inisialisasi subscriber untuk /motor_arah (Bool).
  rclc_subscription_init_default(
    &sub_arah, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
    "motor_arah"
  );

  // Executor dengan 2 handler (1 untuk setiap subscriber).
  rclc_executor_init(&executor, &support, 2, &allocator);
  rclc_executor_add_subscription(
    &executor, &sub_kecepatan, &msg_kecepatan,
    &cb_kecepatan, ON_NEW_DATA
  );
  rclc_executor_add_subscription(
    &executor, &sub_arah, &msg_arah,
    &cb_arah, ON_NEW_DATA
  );
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
