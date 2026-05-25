/*
 * keypad.ino — baca keypad 4x4 via ROS2
 * 
 * Publish ke topic /keypad (String)
 * Karakter tombol yang ditekan
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: Keypad by Mark Stanley
 * 
 * KONEKSI FISIK:
 *
 *   Komponen       | Arduino UNO      | ESP32       
 *   ------------------------------------------------
 *   R1 (row 1)     | D7               | D13           (—)
 *   R2 (row 2)     | D6               | D12           (—)
 *   R3 (row 3)     | D5               | D14           (—)
 *   R4 (row 4)     | D4               | D27           (—)
 *   C1 (col 1)     | D3               | D26           (—)
 *   C2 (col 2)     | D2               | D25           (—)
 *   C3 (col 3)     | D1               | D33           (—)
 *   C4 (col 4)     | D0               | D32           (—)
 *
 *   Lihat wiring.md untuk diagram lengkap.
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


// micro_ros_arduino.h: library utama micro-ROS untuk Arduino.
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/string.h>

// Keypad.h: library untuk keypad matriks (baris x kolom).
#include <Keypad.h>

#if defined(ESP32)
  #define R1 13
  #define R2 12
  #define R3 14
  #define R4 27
  #define C1 26
  #define C2 25
  #define C3 33
  #define C4 32
#else
  #define R1 7
  #define R2 6
  #define R3 5
  #define R4 4
  #define C1 3
  #define C2 2
  #define C3 1
  #define C4 0
#endif

// Layout keypad 4x4.
const byte ROWS = 4;  // Jumlah baris.
const byte COLS = 4;  // Jumlah kolom.
// keys: mapping posisi [baris][kolom] ke karakter.
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
// Pin baris dan kolom (diatur oleh #define di atas).
byte rowPins[ROWS] = {R1, R2, R3, R4};
byte colPins[COLS] = {C1, C2, C3, C4};

// Buat objek Keypad: parameter = layout tombol, pin baris, pin kolom.
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;
std_msgs__msg__String msg;
char char_buf[2] = {0, 0};  // Buffer 2 char: karakter + null terminator.

// timer_callback: baca keypad setiap 50ms.
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // getKey(): baca tombol yang ditekan. Kembali char jika ada, 0 jika tidak.
  char key = keypad.getKey();
  if (key) {
    char_buf[0] = key;           // Masukkan karakter ke buffer.
    msg.data.data = char_buf;    // Pointer ke string.
    msg.data.size = 1;           // Panjang data = 1 karakter.
    rcl_publish(&publisher, &msg, NULL);
  }
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "keypad_node", "", &support);

  // Publisher untuk topic /keypad (String) — berisi karakter tombol.
  rclc_publisher_init_default(
    &publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
    "keypad"
  );

  // Timer 50ms — baca keypad 20x per detik (responsif).
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(50), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  // rclc_executor_spin_some(): proses timer callback (baca keypad).
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
