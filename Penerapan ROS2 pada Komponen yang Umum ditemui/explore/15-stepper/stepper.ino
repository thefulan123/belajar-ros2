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
