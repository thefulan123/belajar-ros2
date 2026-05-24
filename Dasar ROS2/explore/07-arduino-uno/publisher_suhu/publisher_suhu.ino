/*
 * publisher_suhu.ino — Arduino sebagai Publisher ROS2
 * 
 * Mengirim data suhu dari sensor LM35 ke topic /suhu
 * setiap 2 detik melalui micro-ROS.
 * 
 * Koneksi:
 *   LM35 pin VCC → Arduino 5V
 *   LM35 pin OUT → Arduino A0
 *   LM35 pin GND → Arduino GND
 * 
 * Cara jalankan:
 *   1. Upload sketch ini ke Arduino UNO
 *   2. Jalankan micro-ROS agent di PC (lihat run-agent.sh)
 *   3. Cek data: ros2 topic echo /suhu
 * 
 * Board: Arduino UNO
 * Library: micro_ros_arduino (install via Arduino IDE)
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/float32.h>

// ============================================================
// Deklarasi variable ROS2
// ============================================================
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_publisher_t publisher;
rcl_timer_t timer;
std_msgs__msg__Float32 msg;

// Pin sensor suhu
const int SENSOR_PIN = A0;

// ============================================================
// CALLBACK TIMER — dipanggil setiap 2 detik
// ============================================================
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  // Baca nilai analog dari LM35 (0-1023)
  int analog_value = analogRead(SENSOR_PIN);

  // Konversi ke suhu Celsius
  // LM35: 10mV per °C, referensi ADC 5V = 5000mV
  // suhu = (analogValue * 5000 / 1024) / 10
  float suhu = (analog_value * 5000.0 / 1024.0) / 10.0;

  // Isi pesan
  msg.data = suhu;

  // Publikasikan ke topic /suhu
  rcl_publish(&publisher, &msg, NULL);
}

// ============================================================
// SETUP — dijalankan sekali saat Arduino menyala
// ============================================================
void setup() {
  // Inisialisasi serial untuk micro-ROS (baud: 115200)
  Serial.begin(115200);
  set_microros_serial_transports(Serial);

  // Tunggu agent terhubung (maks 2 detik)
  delay(2000);

  // Inisialisasi allocator
  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);

  // Buat node dengan nama: arduino_sensor
  rclc_node_init_default(&node, "arduino_sensor", "", &support);

  // Buat publisher ke topic /suhu (tipe: Float32)
  rclc_publisher_init_default(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
    "suhu"
  );

  // Timer 2 detik
  rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(2000),  // 2000 ms = 2 detik
    timer_callback
  );

  // Executor — mengelola callback
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

// ============================================================
// LOOP — dijalankan terus-menerus
// ============================================================
void loop() {
  // Proses event ROS2 (timer callback akan dipanggil)
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
