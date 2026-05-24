/*
 * joystick.ino — baca joystick analog + button via ROS2
 * 
 * Publish:
 * /joystick_x (Int32)   -100 (kiri)  s/d 100 (kanan)
 * /joystick_y (Int32)   -100 (bawah) s/d 100 (atas)
 * /joystick_button (Bool)  true = ditekan
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
#include <std_msgs/msg/bool.h>

// Dual board pin mapping:
// ESP32: VRX=GPIO36, VRY=GPIO39 (ADC), SW=GPIO26
// UNO:  VRX=A0, VRY=A1 (analog), SW=pin4 (digital)
#if defined(ESP32)
  #define VRX_PIN 36  // Sumbu X (analog input)
  #define VRY_PIN 39  // Sumbu Y (analog input)
  #define SW_PIN  26  // Tombol (digital input, pull-up)
#else
  #define VRX_PIN A0
  #define VRY_PIN A1
  #define SW_PIN  4
#endif

// 3 publisher: X, Y, dan tombol.
rcl_publisher_t pub_x, pub_y, pub_btn;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Buffer pesan.
std_msgs__msg__Int32 msg_x, msg_y;
std_msgs__msg__Bool msg_btn;
// Nilai sebelumnya — untuk mendeteksi perubahan (hanya publish jika berubah).
int last_x = 0, last_y = 0;
bool last_btn = false;

// timer_callback: baca joystick setiap 50ms.
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // Baca nilai analog sumbu X dan Y.
  int raw_x = analogRead(VRX_PIN);
  int raw_y = analogRead(VRY_PIN);
  // Tombol: LOW = ditekan (karena pull-up internal).
  bool btn = (digitalRead(SW_PIN) == LOW);

  // Map ke -100..100 (dengan deadzone ±10 di tengah).
  // ESP32: ADC 12-bit (0-4095), UNO: ADC 10-bit (0-1023).
  int val_x, val_y;
  #if defined(ESP32)
    val_x = map(raw_x, 0, 4095, 100, -100);
    val_y = map(raw_y, 0, 4095, -100, 100);
  #else
    val_x = map(raw_x, 0, 1023, 100, -100);
    val_y = map(raw_y, 0, 1023, -100, 100);
  #endif

  // Deadzone: abaikan nilai kecil di sekitar 0 (joystick tidak presisi).
  if (abs(val_x) < 10) val_x = 0;
  if (abs(val_y) < 10) val_y = 0;

  // Hanya publish jika nilai berubah (hemat bandwidth).
  if (val_x != last_x) {
    last_x = val_x;
    msg_x.data = val_x;
    rcl_publish(&pub_x, &msg_x, NULL);
  }
  if (val_y != last_y) {
    last_y = val_y;
    msg_y.data = val_y;
    rcl_publish(&pub_y, &msg_y, NULL);
  }
  if (btn != last_btn) {
    last_btn = btn;
    msg_btn.data = btn;
    rcl_publish(&pub_btn, &msg_btn, NULL);
  }
}

void setup() {
  // INPUT_PULLUP: aktifkan resistor pull-up internal untuk tombol.
  pinMode(SW_PIN, INPUT_PULLUP);

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "joystick_node", "", &support);

  // Inisialisasi 3 publisher.
  rclc_publisher_init_default(&pub_x, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "joystick_x");
  rclc_publisher_init_default(&pub_y, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "joystick_y");
  rclc_publisher_init_default(&pub_btn, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool), "joystick_button");

  // Timer 50ms = baca joystick 20x per detik.
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(50), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
