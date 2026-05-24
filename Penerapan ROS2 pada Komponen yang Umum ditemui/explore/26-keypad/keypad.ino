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
 * Koneksi: lihat wiring.md
 */

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
