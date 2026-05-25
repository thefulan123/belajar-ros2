/*
 * fingerprint.ino — baca sidik jari via ROS2
 * 
 * Publish ke topic /sidikjari (Int32)
 * -1 = tidak dikenali
 * >0 = ID sidik jari
 * 
 * Board: Arduino UNO (SoftwareSerial) / ESP32 (UART2)
 * 
 * BUTUH LIBRARY: Adafruit Fingerprint Sensor Library
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   VCC            | 5V               | 3.3V          (Merah)
 *   GND            | GND              | GND           (Hitam)
 *   TX             | D2 (SoftwareSerial RX) | D16 (RX2)     (Hijau)
 *   RX             | D3 (SoftwareSerial TX) | D17 (TX2)     (Kuning)
 *
 *   Lihat wiring.md untuk diagram lengkap.
 * 
 * ENROLL: Upload contoh File→Examples→Adafruit Fingerprint→enroll
 *         Sebelum pakai sketch ini
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


#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

// Adafruit_Fingerprint.h: library untuk sensor sidik jari
// (contoh: ZFM-20, R307, AS608) via UART serial.
#include <Adafruit_Fingerprint.h>

// Dual board: ESP32 punya HardwareSerial tambahan,
// Arduino UNO perlu SoftwareSerial untuk UART kedua.
#if defined(ESP32)
  #define FP_RX 16          // ESP32 UART2 RX
  #define FP_TX 17          // ESP32 UART2 TX
  HardwareSerial fserial(2); // UART2 pada ESP32
  Adafruit_Fingerprint finger(&fserial);
#else
  #include <SoftwareSerial.h>
  #define FP_RX 2   // RX pin (ke TX sensor)
  #define FP_TX 3   // TX pin (ke RX sensor)
  SoftwareSerial fserial(FP_RX, FP_TX);
  Adafruit_Fingerprint finger(&fserial);
#endif

rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;
std_msgs__msg__Int32 msg;
int last_id = -2;  // Nilai awal tidak valid.

// timer_callback: cek sidik jari setiap 500ms.
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // getImage(): ambil gambar sidik jari dari sensor.
  int id = finger.getImage();
  if (id != FINGERPRINT_OK) return;  // Tidak ada jari.

  // image2Tz(): konversi gambar ke template (buffered).
  id = finger.image2Tz();
  if (id != FINGERPRINT_OK) return;

  // fingerSearch(): cari template di database sensor.
  id = finger.fingerSearch();
  if (id == FINGERPRINT_OK) {
    // Cocok: ambil ID sidik jari yang terdaftar.
    id = finger.fingerID;
  } else {
    id = -1;  // Tidak dikenali — sidik jari tidak terdaftar.
  }

  // Hanya publish jika berubah (mencegah spam).
  if (id != last_id) {
    last_id = id;
    msg.data = id;
    rcl_publish(&publisher, &msg, NULL);
  }
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Inisialisasi serial untuk sensor fingerprint (57600 baud).
  #if defined(ESP32)
    fserial.begin(57600, SERIAL_8N1, FP_RX, FP_TX);
  #else
    fserial.begin(57600);
  #endif
  finger.begin(57600);

  // verifyPassword(): tes komunikasi dengan sensor.
  if (finger.verifyPassword()) {
    Serial.println("Fingerprint sensor ready!");
  } else {
    Serial.println("ERROR: Fingerprint tidak terdeteksi!");
  }

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "fingerprint_node", "", &support);

  // Publisher ke topic /sidikjari (Int32).
  rclc_publisher_init_default(
    &publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),
    "sidikjari"
  );

  // Timer 500ms — periksa sidik jari 2x per detik.
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(500), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
