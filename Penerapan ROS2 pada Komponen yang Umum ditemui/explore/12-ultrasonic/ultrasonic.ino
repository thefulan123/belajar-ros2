/*
 * ultrasonic.ino — baca jarak HC-SR04 via ROS2
 * 
 * Publish ke topic /jarak (Float64)
 * Jarak dalam cm (2 - 400)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>  // Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2
#include <rcl/rcl.h>            // Library ROS2 Client Library — API inti ROS2 di C
#include <rclc/rclc.h>          // Library RCLC — helper untuk memudahkan inisialisasi ROS2
#include <rclc/executor.h>      // Library executor RCLC — menjalankan callback secara periodik
#include <std_msgs/msg/float64.h> // Tipe pesan Float64 (desimal) — untuk jarak dalam cm

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define TRIG_PIN 26          // Pin GPIO 26 untuk TRIG (pemicu ultrasonik)
  #define ECHO_PIN 27          // Pin GPIO 27 untuk ECHO (penerima pantulan)
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define TRIG_PIN 10          // Pin digital 10 untuk TRIG
  #define ECHO_PIN 11          // Pin digital 11 untuk ECHO
#endif

rcl_publisher_t publisher;       // Publisher — mengirim jarak ke topic ROS2
rclc_executor_t executor;        // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;          // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;       // Allocator — pengelola memori ROS2
rcl_node_t node;                 // Node — entitas utama ROS2 untuk komunikasi
rcl_timer_t timer;               // Timer — memicu callback secara periodik

std_msgs__msg__Float64 msg;      // Variabel pesan Float64 — jarak dalam cm

float baca_jarak() {                                     // Fungsi membaca jarak dari sensor HC-SR04
  digitalWrite(TRIG_PIN, LOW);                            // Pastikan TRIG dalam kondisi LOW
  delayMicroseconds(2);                                   // Tunggu 2 mikrodetik
  digitalWrite(TRIG_PIN, HIGH);                           // Kirim pulsa HIGH ke TRIG
  delayMicroseconds(10);                                  // Pulsa selama 10 mikrodetik
  digitalWrite(TRIG_PIN, LOW);                            // Kembalikan TRIG ke LOW

  long duration = pulseIn(ECHO_PIN, HIGH, 25000);         // Ukur panjang pulsa ECHO (timeout 25ms = ~400cm)
  if (duration == 0) return -1.0;                          // Jika timeout, berarti di luar jangkauan

  // Jarak (cm) = duration (μs) * 0.0343 / 2
  // Kecepatan suara 343 m/s → 0.0343 cm/μs, dibagi 2 karena pulsa pergi-pulang
  float distance = duration * 0.0343 / 2.0;
  return distance;
}

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {  // Callback timer — dipanggil tiap 100ms
  (void)last_call_time;                                            // Hindari warning parameter tidak dipakai
  if (timer == NULL) return;                                       // Pastikan timer valid

  float jarak = baca_jarak();                                      // Baca jarak dari sensor ultrasonik
  if (jarak > 0 && jarak < 400) {                                  // Validasi: 0-400 cm adalah rentang HC-SR04
    msg.data = jarak;
    rcl_publish(&publisher, &msg, NULL);                           // Kirim ke topic "jarak"
  }
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  pinMode(TRIG_PIN, OUTPUT);                       // Set TRIG sebagai OUTPUT (mengirim pulsa)
  pinMode(ECHO_PIN, INPUT);                        // Set ECHO sebagai INPUT (menerima pantulan)
  digitalWrite(TRIG_PIN, LOW);                     // Pastikan TRIG dalam LOW

  Serial.begin(115200);                            // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);          // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                     // Tunggu 2 detik agar micro-ROS siap

  allocator = rcl_get_default_allocator();         // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator);// Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "ultrasonic_node", "", &support);  // Buat node ROS2

  rclc_publisher_init_default(                    // Inisialisasi publisher untuk topic "jarak"
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64),  // Type support untuk Float64
    "jarak"                                        // Nama topic
  );

  rclc_timer_init_default(                        // Buat timer periodik 100ms (10 Hz)
    &timer, &support, RCL_MS_TO_NS(100),
    timer_callback                                 // Callback pembacaan ultrasonik
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_timer(&executor, &timer);      // Daftarkan timer ke executor
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
