/*
 * gps.ino — baca GPS NEO-6M via ROS2
 * 
 * Publish:
 * /gps_lat (Float64) — latitude (garis lintang)
 * /gps_lng (Float64) — longitude (garis bujur)
 * /gps_alt (Float64) — altitude (meter)
 * /gps_sats (Int32)  — jumlah satelit yang terdeteksi
 * 
 * Board: Arduino UNO (SoftwareSerial) / ESP32 (UART2)
 * 
 * BUTUH LIBRARY: TinyGPSPlus
 * 
 * Koneksi: lihat wiring.md
 * 
 * GPS NEO-6M mengirim data NMEA 0183 via UART pada 9600 baud
 * Library TinyGPSPlus memparse data NMEA menjadi koordinat yang mudah dibaca
 */

// ═══════════════════════════════════════════════════════════════
// PENJELASAN DATA STRUCTURE — micro-ROS
// ═══════════════════════════════════════════════════════════════
//
// Berikut adalah data structure inti micro-ROS yang dipakai:
//
// 1. rcl_node_t
//    - Struktur yang merepresentasikan node ROS2 di C/C++.
//    - Setiap node punya nama unik (contoh: "led_node").
//    - Semua komunikasi ROS2 (pub/sub) terikat pada node.
//
// 2. rcl_publisher_t
//    - Struktur untuk MENGIRIM data ke topic ROS2.
//    - Diinisialisasi dengan rclc_publisher_init_default().
//    - Parameter: tipe pesan, nama topic, node.
//    - Method: rcl_publish() — kirim data.
//
// 3. rcl_subscription_t
//    - Struktur untuk MENERIMA data dari topic ROS2.
//    - Diinisialisasi dengan rclc_subscription_init_default().
//    - Parameter: tipe pesan, nama topic, callback function.
//    - Callback dipanggil OTOMATIS saat ada data masuk.
//
// 4. rclc_executor_t
//    - Struktur yang mengatur eksekusi callback.
//    - "Jantung" program micro-ROS — mirip rclpy.spin() di Python.
//    - Method: rclc_executor_spin_some() — proses callback yang pending.
//    - WAJIB ditambahkan publisher/subscriber/timer dengan add_*().
//
// 5. rclc_support_t
//    - Struktur untuk inisialisasi micro-ROS.
//    - Wajib dipanggil PERTAMA KALI di setup().
//    - rclc_support_init() — siapkan memory, allocator, dll.
//
// 6. rcl_allocator_t
//    - Struktur alokator memori untuk ROS2.
//    - rcl_get_default_allocator() — pakai default (heap).
//    - Digunakan saat inisialisasi node, publisher, subscriber.
//
// 7. rcl_timer_t
//    - Struktur timer untuk eksekusi periodik.
//    - rclc_timer_init_default() — buat timer dengan interval ms.
//    - Callback dipanggil setiap interval.
//
// 8. std_msgs__msg__*
//    - Tipe pesan ROS2 standar di C:
//      Bool    → bool data        (true/false)
//      Int32   → int32_t data     (angka bulat)
//      Float32 → float data       (angka desimal)
//      Float64 → double data      (angka desimal presisi ganda)
//      String  → char[] data      (teks)
//════════════════════════════════════════════════════════════════


// micro_ros_arduino: library dasar micro-ROS
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/float64.h>  // Untuk latitude, longitude, altitude (desimal)
#include <std_msgs/msg/int32.h>    // Untuk jumlah satelit (integer)

// SoftwareSerial: membuat port serial tambahan untuk GPS
// Serial utama dipakai micro-ROS, jadi GPS perlu port terpisah
#include <SoftwareSerial.h>
// TinyGPSPlus: library parsing NMEA — mengubah "$GPGGA,..." jadi data koordinat
#include <TinyGPSPlus.h>

// Pin SoftwareSerial untuk GPS
#define GPS_RX 2  // RX Arduino → TX GPS (menerima data NMEA)
#define GPS_TX 3  // TX Arduino → RX GPS (opsional, jarang dipakai)

// Objek GPS — melakukan parsing data NMEA dan menyimpan hasilnya
TinyGPSPlus gps;
// Port serial virtual untuk komunikasi dengan modul GPS
SoftwareSerial softSerial(GPS_RX, GPS_TX);

// Empat publisher untuk data GPS
rcl_publisher_t pub_lat, pub_lng, pub_alt, pub_sats;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Pesan ROS2 untuk masing-masing data
std_msgs__msg__Float64 msg_lat, msg_lng, msg_alt;  // Koordinat desimal
std_msgs__msg__Int32 msg_sats;                      // Jumlah satelit

// timer_callback: dipanggil setiap 1 detik
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // Baca semua data yang tersedia dari port serial GPS
  // softSerial.available(): jumlah byte yang masuk di buffer
  while (softSerial.available()) {
    // gps.encode(): parsing satu karakter NMEA — secara bertahap membangun data
    gps.encode(softSerial.read());
  }

  // Cek apakah data lokasi valid (already fix dari satelit)
  if (gps.location.isValid()) {
    msg_lat.data = gps.location.lat();   // Latitude dalam derajat desimal
    msg_lng.data = gps.location.lng();   // Longitude dalam derajat desimal
    rcl_publish(&pub_lat, &msg_lat, NULL);
    rcl_publish(&pub_lng, &msg_lng, NULL);
  }

  // Cek apakah data altitude valid
  if (gps.altitude.isValid()) {
    msg_alt.data = gps.altitude.meters();  // Altitude dalam meter
    rcl_publish(&pub_alt, &msg_alt, NULL);
  }

  // Jumlah satelit — selalu publish (meskipun 0)
  msg_sats.data = gps.satellites.value();
  rcl_publish(&pub_sats, &msg_sats, NULL);
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Inisialisasi SoftwareSerial: GPS NEO-6M menggunakan baud rate 9600 default
  softSerial.begin(9600);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "gps_node", "", &support);

  // Daftarkan 4 publisher untuk tiap data GPS
  rclc_publisher_init_default(&pub_lat, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "gps_lat");
  rclc_publisher_init_default(&pub_lng, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "gps_lng");
  rclc_publisher_init_default(&pub_alt, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "gps_alt");
  rclc_publisher_init_default(&pub_sats, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "gps_sats");

  // Timer 1 detik — GPS tidak perlu dibaca terlalu cepat (update rate 1-10 Hz)
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(1000), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
