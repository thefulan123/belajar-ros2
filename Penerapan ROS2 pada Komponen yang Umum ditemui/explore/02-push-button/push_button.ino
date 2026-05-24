/*
 * push_button.ino — baca push button via ROS2
 * 
 * Publish ke topic /button (Bool)
 * true  → button ditekan
 * false → button dilepas
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>  // Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2
#include <rcl/rcl.h>            // Library ROS2 Client Library — API inti ROS2 di C
#include <rclc/rclc.h>          // Library RCLC — helper untuk memudahkan inisialisasi ROS2
#include <rclc/executor.h>      // Library executor RCLC — menjalankan callback secara periodik
#include <std_msgs/msg/bool.h>  // Tipe pesan Bool (true/false) — standar ROS2 untuk data boolean

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define BUTTON_PIN 26        // Pin GPIO 26 untuk ESP32
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define BUTTON_PIN 4         // Pin digital 4 untuk Arduino UNO
#endif

rcl_publisher_t publisher;       // Publisher — mengirim pesan ke topic ROS2
rclc_executor_t executor;        // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;          // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;       // Allocator — pengelola memori ROS2
rcl_node_t node;                 // Node — entitas utama ROS2 untuk komunikasi
rcl_timer_t timer;               // Timer — memicu callback secara periodik

std_msgs__msg__Bool msg;         // Variabel pesan Bool — data yang akan dipublish
int last_state = HIGH;           // State terakhir button (HIGH = tidak ditekan, LOW = ditekan)

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {  // Callback timer — dipanggil setiap 50ms
  (void)last_call_time;                                            // Hindari warning parameter tidak dipakai
  if (timer != NULL) {                                             // Pastikan timer valid
    int current_state = digitalRead(BUTTON_PIN);                   // Baca kondisi button (LOW = ditekan)
    // Hanya publish jika state berubah — mengurangi trafik network
    if (current_state != last_state) {
      last_state = current_state;
      msg.data = (current_state == LOW); // LOW karena internal pull-up — button aktif LOW
      rcl_publish(&publisher, &msg, NULL);                         // Kirim pesan ke topic "button"
    }
  }
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  pinMode(BUTTON_PIN, INPUT_PULLUP);               // Set pin button sebagai INPUT dengan internal pull-up
  last_state = digitalRead(BUTTON_PIN);             // Baca state awal button

  Serial.begin(115200);                             // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);           // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                      // Tunggu 2 detik agar micro-ROS siap

  allocator = rcl_get_default_allocator();          // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator); // Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "button_node", "", &support);  // Buat node ROS2 bernama "button_node"

  rclc_publisher_init_default(                     // Inisialisasi publisher untuk topic "button"
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Bool),  // Dapatkan type support untuk pesan Bool
    "button"                                        // Nama topic yang akan dipublish
  );

  // Publish tiap 50ms untuk mendeteksi perubahan — 20 Hz cukup untuk button
  rclc_timer_init_default(                         // Buat timer periodik 50ms
    &timer, &support, RCL_MS_TO_NS(50),
    timer_callback                                  // Callback yang dipanggil tiap 50ms
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_timer(&executor, &timer);      // Daftarkan timer ke executor
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
