/*
 * esp32_wifi.ino — contoh micro-ROS via WiFi (ESP32 only)
 * 
 * Berbeda dengan explore lain yang pakai Serial (kabel USB),
 * sketch ini menggunakan koneksi WiFi untuk komunikasi micro-ROS.
 * 
 * Ganti SSID, PASSWORD, dan AGENT_IP sesuai jaringan Anda.
 * 
 * Board: ESP32 (tidak support Arduino UNO)
 * 
 * Prasyarat:
 * - ESP32 harus terhubung ke WiFi yang sama dengan ROS2 agent
 * - Jalankan micro-ROS agent di PC: ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

// WiFi.h: library ESP32 untuk koneksi WiFi — hanya tersedia di board ESP32
#include <WiFi.h>

// ===== GANTI INI =====
#define SSID      "WIFI_ANDA"       // Nama jaringan WiFi Anda
#define PASSWORD  "PASSWORD_WIFI"   // Password WiFi
#define AGENT_IP  "192.168.1.100"   // IP address PC yang menjalankan micro-ROS agent
#define AGENT_PORT 8888             // Port UDP agent (default 8888)
// =====================

rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;
std_msgs__msg__Int32 msg;
int counter = 0;  // Counter yang dikirim setiap detik

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;
  msg.data = counter++;  // Increment counter setiap detik
  rcl_publish(&publisher, &msg, NULL);
}

void setup() {
  Serial.begin(115200);

  // set_microros_wifi_transports: transport micro-ROS via WiFi (UDP)
  // Berbeda dengan set_microros_serial_transports yang pakai kabel USB
  // Fungsi ini:
  //   1. Menghubungkan ESP32 ke WiFi (SSID/PASSWORD)
  //   2. Membuat koneksi UDP ke AGENT_IP:AGENT_PORT
  //   3. Mengirim data ROS2 serial melalui UDP
  set_microros_wifi_transports(SSID, PASSWORD, AGENT_IP, AGENT_PORT);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "esp32_wifi_node", "", &support);

  rclc_publisher_init_default(&publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "wifi_counter");

  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(1000), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
