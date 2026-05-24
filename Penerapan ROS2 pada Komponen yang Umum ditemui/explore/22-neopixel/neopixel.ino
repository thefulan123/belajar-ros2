/*
 * neopixel.ino — kontrol NeoPixel WS2812B via ROS2
 * 
 * Subscribe ke topic /neopixel (String)
 * Format: "index,R,G,B"
 * Contoh: "0,255,0,0" = LED 0 merah
 *         "all,0,0,255" = semua LED biru
 *         "all,0,0,0" = matikan semua
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: Adafruit NeoPixel
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/string.h>

// Adafruit_NeoPixel.h: library untuk LED strip WS2812B/NeoPixel.
// Setiap LED berisi IC driver sendiri — cukup 1 pin data.
#include <Adafruit_NeoPixel.h>

#if defined(ESP32)
  #define NEO_PIN 14  // Pin data ke NeoPixel
#else
  #define NEO_PIN 6
#endif

#define NUM_LEDS 8  // Jumlah LED dalam strip.

// Buat objek strip NeoPixel.
// Parameter: (jumlah LED, pin data, tipe LED + kecepatan).
// NEO_GRB: urutan warna Green-Red-Blue (umum).
// NEO_KHZ800: kecepatan komunikasi 800KHz.
Adafruit_NeoPixel strip(NUM_LEDS, NEO_PIN, NEO_GRB + NEO_KHZ800);

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__String msg;

// set_all(): atur semua LED ke warna yang sama, lalu tampilkan.
void set_all(uint8_t r, uint8_t g, uint8_t b) {
  for (int i = 0; i < NUM_LEDS; i++) {
    // setPixelColor(index, warna) — siapkan warna di buffer.
    strip.setPixelColor(i, strip.Color(r, g, b));
  }
  // show(): kirim buffer ke seluruh strip LED.
  strip.show();
}

// subscription_callback: parse string "index,R,G,B" → kontrol LED.
void subscription_callback(const void *msgin) {
  const std_msgs__msg__String *msg = (const std_msgs__msg__String *)msgin;
  String data = String(msg->data.data);

  // Cari posisi 3 koma pemisah index, R, G, B.
  int comma1 = data.indexOf(',');
  int comma2 = data.indexOf(',', comma1 + 1);
  int comma3 = data.indexOf(',', comma2 + 1);

  // Jika format salah (kurang koma), abaikan.
  if (comma1 < 0 || comma2 < 0 || comma3 < 0) return;

  // Ekstrak bagian-bagian string.
  String idx_str = data.substring(0, comma1);
  int r = data.substring(comma1 + 1, comma2).toInt();
  int g = data.substring(comma2 + 1, comma3).toInt();
  int b = data.substring(comma3 + 1).toInt();

  // Jika index = "all", set semua LED. Jika tidak, set satu LED.
  if (idx_str == "all") {
    set_all(r, g, b);
  } else {
    int led_idx = idx_str.toInt();
    if (led_idx >= 0 && led_idx < NUM_LEDS) {
      strip.setPixelColor(led_idx, strip.Color(r, g, b));
      strip.show();
    }
  }
}

void setup() {
  // begin(): alokasi buffer dan siapkan pin data.
  strip.begin();
  strip.show();  // show pertama → semua LED mati.
  strip.setBrightness(50);  // Kecerahan 50/255 (~20%).

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "neopixel_node", "", &support);

  rclc_subscription_init_default(
    &subscriber, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
    "neopixel"
  );

  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_subscription(
    &executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA
  );
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
