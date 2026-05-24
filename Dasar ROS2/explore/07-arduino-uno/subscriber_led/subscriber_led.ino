/*
 * subscriber_led.ino — Arduino sebagai Subscriber ROS2
 * 
 * Menerima perintah boolean dari topic /led
 * untuk menyalakan atau mematikan LED bawaan Arduino.
 * 
 * Cara jalankan:
 *   1. Upload sketch ini ke Arduino UNO
 *   2. Jalankan micro-ROS agent di PC (lihat run-agent.sh)
 *   3. Kirim perintah: ros2 topic pub /led std_msgs/msg/Bool "data: true" --once
 * 
 * Board: Arduino UNO
 * Library: micro_ros_arduino
 */

#include <micro_ros_arduino.h>  // (1) Library micro-ROS untuk Arduino.
#include <rcl/rcl.h>            // (2) Library inti ROS2 C.
#include <rclc/rclc.h>          // (3) Wrapper rclc yang lebih sederhana.
#include <rclc/executor.h>      // (4) Executor — mengelola callback ROS2.
#include <std_msgs/msg/bool.h>  // (5) Tipe pesan Bool — untuk perintah true/false.

// ============================================================
// Deklarasi variable ROS2
// ============================================================
rclc_executor_t executor;  // (6) Executor — memproses event (mirip rclpy.spin()).
rclc_support_t support;    // (7) Support object — konfigurasi ROS2.
rcl_allocator_t allocator; // (8) Allocator — manajemen memori.
rcl_node_t node;           // (9) Node ROS2 — identitas node di jaringan.
rcl_subscription_t subscriber;  // (10) Subscription — untuk menerima data dari topic.
std_msgs__msg__Bool msg;   // (11) Pesan Bool — wadah data yang diterima.

// Pin LED
const int LED_PIN = LED_BUILTIN;  // (12) LED_BUILTIN — pin 13 (LED bawaan Arduino UNO).

// ============================================================
// CALLBACK — dipanggil setiap ada pesan masuk di /led
// ============================================================
void subscription_callback(const void *msgin) {
  // (13) CALLBACK SUBSCRIPTION — dipanggil OTOMATIS saat ada data di topic /led.
  // Parameter msgin adalah pointer ke data yang diterima (void*).
  
  // Ambil pesan — cast dari void* ke tipe yang benar.
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;

  // Nyalakan/matikan LED sesuai data
  // msg->data — field boolean: true = nyala, false = mati.
  if (msg->data) {
    digitalWrite(LED_PIN, HIGH);  // (14) LED ON (5V).
  } else {
    digitalWrite(LED_PIN, LOW);   // (15) LED OFF (0V).
  }
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  // (16) Konfigurasi pin LED sebagai OUTPUT.
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // (17) Mulai dengan LED mati.

  // Inisialisasi serial untuk micro-ROS
  Serial.begin(115200);  // (18) Serial USB baud rate 115200.
  set_microros_serial_transports(Serial);  // (19) Set Serial sebagai transport.
  delay(2000);  // (20) Tunggu agent terhubung.

  // Inisialisasi ROS2
  allocator = rcl_get_default_allocator();  // (21) Dapatkan allocator default.
  rclc_support_init(&support, 0, NULL, &allocator);  // (22) Init support.

  // Buat node: arduino_led
  rclc_node_init_default(&node, "arduino_led", "", &support);
  // (23) MEMBUAT NODE — nama node: "arduino_led".

  // Subscribe ke topic /led
  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),  // (24) Makro tipe pesan Bool.
    "led"  // (25) Nama topic: "led".
  );
  // (26) MEMBUAT SUBSCRIPTION — mirip self.create_subscription() di Python.

  // Executor
  rclc_executor_init(&executor, &support, 1, &allocator);  // (27) Init executor.
  rclc_executor_add_subscription(
    &executor,
    &subscriber,
    &msg,               // (28) Pointer ke penyimpanan pesan.
    &subscription_callback,  // (29) Fungsi callback.
    ON_NEW_DATA         // (30) ON_NEW_DATA — callback dipanggil SETIAP ada data baru.
  );
  // (31) Daftarkan subscription ke executor — mirip self.create_subscription().
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  // Proses event ROS2 — subscription_callback akan dipanggil jika ada data.
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));  // (32) SPIN — proses event.
  delay(10);  // (33) Jeda agar tidak memonopoli CPU.
}
