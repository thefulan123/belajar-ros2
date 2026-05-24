/*
 * load_cell.ino — baca berat dari load cell + HX711 via ROS2
 * 
 * Publish ke topic /berat (Float64) dalam gram
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: HX711 by Bogdan Necula
 * 
 * Koneksi: lihat wiring.md
 * 
 * KALIBRASI: Ganti KALIBRASI_FAKTOR setelah kalibrasi
 * Cara: letakkan beban 100g, hitung faktor = raw / 100
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/float64.h>

// HX711.h: library untuk ADC HX711 (24-bit) dari load cell.
#include <HX711.h>

#if defined(ESP32)
  #define DT_PIN 14   // Data pin (DOUT)
  #define SCK_PIN 12  // Clock pin (SCK)
#else
  #define DT_PIN 3
  #define SCK_PIN 2
#endif

// GANTI dengan hasil kalibrasi Anda.
// Contoh: jika raw=50000 untuk 100g, maka faktor = 500.
#define KALIBRASI_FAKTOR 500.0

// Objek HX711 untuk komunikasi dengan modul.
HX711 hx711;
rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;
std_msgs__msg__Float64 msg;

// timer_callback: dipanggil setiap 200ms → baca & publish berat.
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // is_ready(): cek apakah HX711 siap mengirim data.
  if (hx711.is_ready()) {
    // get_units(5): ambil rata-rata dari 5 sampel (filter noise).
    float berat = hx711.get_units(5); // rata-rata 5 sampel
    if (berat < 0) berat = 0;  // Tidak ada berat negatif.
    msg.data = berat;
    rcl_publish(&publisher, &msg, NULL);
  }
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // begin(): inisialisasi pin DT dan SCK untuk HX711.
  hx711.begin(DT_PIN, SCK_PIN);
  // set_scale(): terapkan faktor kalibrasi.
  hx711.set_scale(KALIBRASI_FAKTOR);
  // tare(): zero-out — anggap beban saat ini sebagai 0.
  hx711.tare(); // zero-out

  if (!hx711.is_ready()) {
    Serial.println("ERROR: HX711 tidak terdeteksi!");
  }

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "load_cell_node", "", &support);

  // Publisher untuk topic /berat (Float64).
  rclc_publisher_init_default(
    &publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64),
    "berat"
  );

  // Timer 200ms → 5 publish per detik.
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(200), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
