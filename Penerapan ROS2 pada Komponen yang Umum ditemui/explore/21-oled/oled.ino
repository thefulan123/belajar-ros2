/*
 * oled.ino — tampilkan teks di OLED 128x64 via ROS2
 * 
 * Subscribe ke topic /oled (String)
 * Format: teks, \n untuk baris baru (maks 4 baris)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: Adafruit SSD1306 + Adafruit GFX
 * 
 * Koneksi: lihat wiring.md
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
#include <std_msgs/msg/string.h>

#include <Wire.h>
// Adafruit_GFX.h: library grafis dasar (teks, garis, bentuk).
#include <Adafruit_GFX.h>
// Adafruit_SSD1306.h: library untuk OLED SSD1306 (128x64) via I2C.
#include <Adafruit_SSD1306.h>

// Resolusi OLED: 128 pixel lebar, 64 pixel tinggi.
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Ganti 0x3C atau 0x3D sesuai OLED Anda.
// Parameter: (lebar, tinggi, koneksi I2C, reset pin).
// -1 = reset tidak terhubung (gunakan internal reset).
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__String msg;

// subscription_callback: terima teks dari topic /oled, tampilkan.
void subscription_callback(const void *msgin) {
  const std_msgs__msg__String *msg = (const std_msgs__msg__String *)msgin;
  String data = String(msg->data.data);

  display.clearDisplay();             // Hapus buffer display.
  display.setTextSize(1);             // Ukuran teks normal (1:1).
  display.setTextColor(SSD1306_WHITE);// Teks putih di OLED hitam.
  display.setCursor(0, 0);            // Mulai dari pojok kiri atas.

  // Bagi berdasarkan \n, maks 4 baris (keterbatasan layar).
  int baris = 0;
  int start = 0;
  while (baris < 4) {
    int idx = data.indexOf('\n', start);
    String line;
    if (idx >= 0) {
      // Potong dari start hingga newline.
      line = data.substring(start, idx);
      start = idx + 1;  // Loncat setelah newline.
    } else {
      // Baris terakhir (tanpa newline).
      line = data.substring(start);
      display.println(line);
      break;
    }
    display.println(line);
    baris++;
  }
  display.display();  // Kirim buffer ke OLED agar tampil.
}

void setup() {
  // Inisialisasi OLED dengan alamat I2C 0x3C.
  // SSD1306_SWITCHCAPVCC: mode power internal.
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("ERROR: OLED tidak terdeteksi di 0x3C!");
    // Coba 0x3D (beberapa OLED versi lama).
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) {
      Serial.println("ERROR: OLED tidak terdeteksi!");
    }
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("ROS2 OLED ready");
  display.display();

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "oled_node", "", &support);

  rclc_subscription_init_default(
    &subscriber, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
    "oled"
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
