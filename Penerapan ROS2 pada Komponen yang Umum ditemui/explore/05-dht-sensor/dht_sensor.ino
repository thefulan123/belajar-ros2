/*
 * dht_sensor.ino — baca DHT11/DHT22 suhu & kelembapan via ROS2
 * 
 * Publish ke topic /suhu (Float64) dan /kelembapan (Float64)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: DHT sensor library by Adafruit
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>  // Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2
#include <rcl/rcl.h>            // Library ROS2 Client Library — API inti ROS2 di C
#include <rclc/rclc.h>          // Library RCLC — helper untuk memudahkan inisialisasi ROS2
#include <rclc/executor.h>      // Library executor RCLC — menjalankan callback secara periodik
#include <std_msgs/msg/float64.h> // Tipe pesan Float64 (desimal) — untuk suhu & kelembapan

#include <DHT.h>  // Library DHT sensor by Adafruit — membaca DHT11/DHT22

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define DHTPIN 32            // Pin GPIO 32 untuk ESP32
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define DHTPIN 7             // Pin digital 7 untuk Arduino UNO
#endif

#define DHTTYPE DHT11          // Tipe sensor: DHT11. Ganti ke DHT22 jika pakai DHT22

DHT dht(DHTPIN, DHTTYPE);      // Buat objek DHT dengan pin dan tipe yang ditentukan

rcl_publisher_t pub_suhu;            // Publisher untuk topic suhu
rcl_publisher_t pub_kelembapan;      // Publisher untuk topic kelembapan
rclc_executor_t executor;            // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;              // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;           // Allocator — pengelola memori ROS2
rcl_node_t node;                     // Node — entitas utama ROS2 untuk komunikasi
rcl_timer_t timer;                   // Timer — memicu callback secara periodik

std_msgs__msg__Float64 msg_suhu;     // Variabel pesan Float64 untuk suhu
std_msgs__msg__Float64 msg_kelembapan; // Variabel pesan Float64 untuk kelembapan
unsigned long last_read = 0;         // Waktu terakhir baca sensor (millis)
const unsigned long interval = 2000; // Interval minimal 2 detik — DHT11 max 1 Hz (1x per detik)

void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {  // Callback timer — dipanggil periodik
  (void)last_call_time;                                            // Hindari warning parameter tidak dipakai
  if (timer == NULL) return;                                       // Pastikan timer valid

  // DHT butuh jeda minimal 1 detik antar pembacaan — agar tidak error
  if (millis() - last_read < interval) return;                     // Lewati jika terlalu cepat
  last_read = millis();                                            // Catat waktu pembacaan

  float h = dht.readHumidity();                                    // Baca kelembapan (%)
  float t = dht.readTemperature();                                 // Baca suhu (Celcius)

  if (isnan(h) || isnan(t)) {                                      // Cek apakah pembacaan gagal (NaN)
    Serial.println("ERROR: Gagal baca DHT");                       // Cetak error ke Serial
    return;                                                        // Jangan publish data invalid
  }

  msg_suhu.data = t;                                               // Set data suhu
  msg_kelembapan.data = h;                                         // Set data kelembapan

  rcl_publish(&pub_suhu, &msg_suhu, NULL);                        // Kirim suhu ke topic "suhu"
  rcl_publish(&pub_kelembapan, &msg_kelembapan, NULL);             // Kirim kelembapan ke topic "kelembapan"
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  Serial.begin(115200);                            // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);          // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                     // Tunggu 2 detik agar micro-ROS siap

  dht.begin();                                     // Inisialisasi sensor DHT

  allocator = rcl_get_default_allocator();         // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator);// Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "dht_node", "", &support);  // Buat node ROS2 bernama "dht_node"

  rclc_publisher_init_default(                    // Inisialisasi publisher untuk topic "suhu"
    &pub_suhu,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64),  // Type support untuk Float64
    "suhu"                                         // Nama topic suhu
  );

  rclc_publisher_init_default(                    // Inisialisasi publisher untuk topic "kelembapan"
    &pub_kelembapan,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64),  // Type support untuk Float64
    "kelembapan"                                   // Nama topic kelembapan
  );

  rclc_timer_init_default(                        // Buat timer periodik 1000ms (1Hz)
    &timer, &support, RCL_MS_TO_NS(1000),
    timer_callback                                 // Callback pembacaan DHT
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_timer(&executor, &timer);      // Daftarkan timer ke executor
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
