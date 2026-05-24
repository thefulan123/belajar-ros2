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

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/bool.h>

// ============================================================
// Deklarasi variable ROS2
// ============================================================
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__Bool msg;

// Pin LED
const int LED_PIN = LED_BUILTIN;  // Arduino UNO: pin 13

// ============================================================
// CALLBACK — dipanggil setiap ada pesan masuk di /led
// ============================================================
void subscription_callback(const void *msgin) {
  // Ambil pesan
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;

  // Nyalakan/matikan LED sesuai data
  if (msg->data) {
    digitalWrite(LED_PIN, HIGH);  // Nyala
  } else {
    digitalWrite(LED_PIN, LOW);   // Mati
  }
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Konfigurasi pin LED sebagai OUTPUT
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // Mulai dengan LED mati

  // Inisialisasi serial untuk micro-ROS
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Inisialisasi ROS2
  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);

  // Buat node: arduino_led
  rclc_node_init_default(&node, "arduino_led", "", &support);

  // Subscribe ke topic /led
  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
    "led"
  );

  // Executor
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_subscription(
    &executor,
    &subscriber,
    &msg,
    &subscription_callback,
    ON_NEW_DATA  // Callback dipanggil SETIAP ada data baru
  );
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  // Proses event ROS2
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
