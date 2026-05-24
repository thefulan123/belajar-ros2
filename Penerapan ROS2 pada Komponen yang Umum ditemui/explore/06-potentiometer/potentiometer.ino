/*
 * potentiometer.ino — baca potensiometer via ROS2
 * 
 * Publish ke topic /potensiometer (Int32)
 * Nilai 0 - 100 (persentase putaran)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>  // Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2
#include <rcl/rcl.h>            // Library ROS2 Client Library — API inti ROS2 di C
#include <rclc/rclc.h>          // Library RCLC — helper untuk memudahkan inisialisasi ROS2
#include <rclc/executor.h>      // Library executor RCLC — menjalankan callback secara periodik
#include <std_msgs/msg/int32.h> // Tipe pesan Int32 (integer) — untuk nilai potensiometer 0-100

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define POT_PIN 36           // Pin ADC1 (GPIO 36) untuk ESP32 — input analog
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define POT_PIN A0           // Pin analog A0 untuk Arduino UNO
#endif

rcl_publisher_t publisher;       // Publisher — mengirim nilai potensiometer ke topic ROS2
rclc_executor_t executor;        // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;          // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;       // Allocator — pengelola memori ROS2
rcl_node_t node;                 // Node — entitas utama ROS2 untuk komunikasi
rcl_timer_t timer;               // Timer — memicu callback secara periodik

std_msgs__msg__Int32 msg;        // Variabel pesan Int32 — nilai 0-100
int last_value = -1;             // Nilai terakhir yang dipublish (untuk deteksi perubahan)

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {  // Callback timer — dipanggil tiap 50ms
  (void)last_call_time;                                            // Hindari warning parameter tidak dipakai
  if (timer == NULL) return;                                       // Pastikan timer valid

  int raw = analogRead(POT_PIN);                                   // Baca nilai analog dari potensiometer

  #if defined(ESP32)
    // ESP32 ADC: 12-bit (0-4095) — resolusi lebih tinggi
    int pct = map(raw, 0, 4095, 0, 100);
  #else
    // Arduino UNO ADC: 10-bit (0-1023) — resolusi standar
    int pct = map(raw, 0, 1023, 0, 100);
  #endif

  // Batasi 0-100 — pastikan nilai dalam rentang
  pct = constrain(pct, 0, 100);

  // Hanya publish jika berubah (min 2% perubahan) — kurangi trafik network
  if (abs(pct - last_value) >= 2) {
    last_value = pct;
    msg.data = pct;
    rcl_publish(&publisher, &msg, NULL);                           // Kirim pesan ke topic "potensiometer"
  }
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  Serial.begin(115200);                            // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);          // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                     // Tunggu 2 detik agar micro-ROS siap

  allocator = rcl_get_default_allocator();         // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator);// Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "potentiometer_node", "", &support);  // Buat node ROS2

  rclc_publisher_init_default(                    // Inisialisasi publisher untuk topic "potensiometer"
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),  // Type support untuk Int32
    "potensiometer"                                // Nama topic
  );

  rclc_timer_init_default(                        // Buat timer periodik 50ms (20 Hz)
    &timer, &support, RCL_MS_TO_NS(50),
    timer_callback                                 // Callback pembacaan potensiometer
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_timer(&executor, &timer);      // Daftarkan timer ke executor
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
