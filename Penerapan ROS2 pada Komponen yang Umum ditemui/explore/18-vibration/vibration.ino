/*
 * vibration.ino — kontrol vibration motor via ROS2
 * 
 * Subscribe ke topic /vibrasi (Int32)
 * 0   = mati
 * 100 = getaran maksimal
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

// Dual board: ESP32 → GPIO 15, Arduino UNO → pin 10 (PWM).
#if defined(ESP32)
  #define VIB_PIN 15
#else
  #define VIB_PIN 10
#endif

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__Int32 msg;

// subscription_callback: terima intensitas getaran (0–100).
void subscription_callback(const void *msgin) {
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  // constrain(): batasi nilai 0–100.
  int intensity = constrain(msg->data, 0, 100);
  // map(): skala 0–100 → 0–255 (PWM 8-bit).
  int pwm = map(intensity, 0, 100, 0, 255);
  // analogWrite(): kirim PWM ke motor vibration.
  analogWrite(VIB_PIN, pwm);
}

void setup() {
  pinMode(VIB_PIN, OUTPUT);
  analogWrite(VIB_PIN, 0);  // Mati saat startup.

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "vibration_node", "", &support);

  rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "vibrasi"
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
