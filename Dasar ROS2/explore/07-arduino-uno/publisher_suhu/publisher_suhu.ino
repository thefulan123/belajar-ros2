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

#include <micro_ros_arduino.h>  // (1) Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2.
#include <rcl/rcl.h>            // (2) Library inti ROS2 C (rcl) — menyediakan node, publisher, dll.
#include <rclc/rclc.h>          // (3) Library rclc — wrapper yang lebih sederhana untuk rcl.
#include <rclc/executor.h>      // (4) Executor — mengelola callback (timer, subscription).
#include <std_msgs/msg/float32.h>  // (5) Tipe pesan Float32 standar ROS2 — data suhu (float).

// ============================================================
// Deklarasi variable ROS2
// ============================================================
rclc_executor_t executor;  // (6) Executor — memproses event ROS2 (mirip rclpy.spin()).
rclc_support_t support;    // (7) Support object — menyimpan konfigurasi init.
rcl_allocator_t allocator; // (8) Allocator — pengelola memori untuk ROS2.
rcl_node_t node;           // (9) Node ROS2 — identitas di jaringan ROS2.
rcl_publisher_t publisher; // (10) Publisher — untuk mengirim data ke topic.
rcl_timer_t timer;         // (11) Timer — trigger periodik (setiap 2 detik).
std_msgs__msg__Float32 msg; // (12) Pesan Float32 — wadah data suhu yang akan dikirim.

// Pin sensor suhu
const int SENSOR_PIN = A0;  // (13) Pin analog A0 untuk membaca sensor LM35.

// ============================================================
// CALLBACK TIMER — dipanggil setiap 2 detik
// ============================================================
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  // (14) CALLBACK TIMER — dipanggil OTOMATIS oleh executor setiap 2 detik.
  // Parameter: timer (pointer ke timer), last_call_time (timestamp panggilan sebelumnya).
  
  // Baca nilai analog dari LM35 (0-1023)
  int analog_value = analogRead(SENSOR_PIN);  // (15) ADC Arduino: 0-1023 (10-bit).

  // Konversi ke suhu Celsius
  // LM35: 10mV per °C, referensi ADC 5V = 5000mV
  // suhu = (analogValue * 5000 / 1024) / 10
  float suhu = (analog_value * 5000.0 / 1024.0) / 10.0;  // (16) Rumus konversi LM35 ke °C.

  // Isi pesan
  msg.data = suhu;  // (17) Masukkan nilai suhu ke field data pesan Float32.

  // Publikasikan ke topic /suhu
  rcl_publish(&publisher, &msg, NULL);  // (18) PUBLISH — kirim data ke topic /suhu.
  // rcl_publish(publisher_ptr, msg_ptr, NULL) — NULL berarti tanpa opsi khusus.
}

// ============================================================
// SETUP — dijalankan sekali saat Arduino menyala
// ============================================================
void setup() {
  // (19) Inisialisasi serial untuk micro-ROS (baud: 115200).
  // micro-ROS berkomunikasi via Serial USB ke PC yang menjalankan agent.
  Serial.begin(115200);
  set_microros_serial_transports(Serial);  // (20) Set Serial sebagai transport micro-ROS.

  // Tunggu agent terhubung (maks 2 detik)
  delay(2000);  // (21) Delay agar agent punya waktu konek.

  // Inisialisasi allocator
  allocator = rcl_get_default_allocator();  // (22) Dapatkan allocator default.
  rclc_support_init(&support, 0, NULL, &allocator);  // (23) Init support object.

  // Buat node dengan nama: arduino_sensor
  rclc_node_init_default(&node, "arduino_sensor", "", &support);
  // (24) MEMBUAT NODE — nama node: "arduino_sensor".
  // Sintaks: rclc_node_init_default(&node, "nama_node", "namespace", &support)

  // Buat publisher ke topic /suhu (tipe: Float32)
  rclc_publisher_init_default(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),  // (25) Makro untuk mendapatkan tipe message.
    "suhu"  // (26) Nama topic: "suhu" (tanpa slash di micro-ROS).
  );
  // (27) MEMBUAT PUBLISHER — mirip self.create_publisher() di Python.

  // Timer 2 detik
  rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(2000),  // (28) RCL_MS_TO_NS(2000) — konversi 2000 ms ke nanodetik.
    timer_callback        // (29) Callback timer: fungsi timer_callback().
  );
  // (30) MEMBUAT TIMER — mirip self.create_timer() di Python.

  // Executor — mengelola callback
  rclc_executor_init(&executor, &support, 1, &allocator);  // (31) Init executor dengan 1 timer.
  rclc_executor_add_timer(&executor, &timer);               // (32) Daftarkan timer ke executor.
  // (33) EXECUTOR — mirip rclpy.spin(), tapi di Arduino dipanggil manual di loop().
}

// ============================================================
// LOOP — dijalankan terus-menerus
// ============================================================
void loop() {
  // Proses event ROS2 (timer callback akan dipanggil)
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  // (34) SPIN SOME — proses event ROS2 yang tersedia (non-blocking).
  // Parameter: executor, timeout 100 ms.
  // Jika ada timer yang siap, callback_timer() dipanggil.
  delay(10);  // (35) Jeda kecil agar tidak memonopoli CPU Arduino.
}
