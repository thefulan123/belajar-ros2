/*
 * solenoid.ino — kontrol solenoid via ROS2 (via relay)
 * 
 * Subscribe ke topic /solenoid (Bool)
 * true  = solenoid ON (kunci aktif / valve buka)
 * false = solenoid OFF
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
// std_msgs/msg/bool.h: tipe pesan boolean (true/false).
#include <std_msgs/msg/bool.h>

#if defined(ESP32)
  #define SOLENOID_PIN 33  // GPIO33
#else
  #define SOLENOID_PIN 6   // Pin digital 6
#endif

// Variabel ROS2
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__Bool msg;

// subscription_callback: dipanggil saat ada data di topic /solenoid.
// Solenoid biasanya via relay → ON = HIGH, OFF = LOW.
void subscription_callback(const void *msgin) {
  const std_msgs__msg__Bool *msg = (const std_msgs__msg__Bool *)msgin;
  // Ternary: jika msg->data true → HIGH, false → LOW.
  digitalWrite(SOLENOID_PIN, msg->data ? HIGH : LOW);
}

void setup() {
  pinMode(SOLENOID_PIN, OUTPUT);
  digitalWrite(SOLENOID_PIN, LOW);  // Mati saat startup.

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "solenoid_node", "", &support);

  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),
    "solenoid"
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
}
