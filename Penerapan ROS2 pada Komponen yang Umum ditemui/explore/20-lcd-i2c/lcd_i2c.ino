/*
 * lcd_i2c.ino — tampilkan teks di LCD 16x2 via ROS2
 * 
 * Subscribe ke topic /lcd (String)
 * Format: "baris1\nbaris2"
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: LiquidCrystal I2C by Frank de Brabander
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/string.h>

#include <Wire.h>
// LiquidCrystal_I2C.h: library LCD 16x2 dengan antarmuka I2C
// (hanya perlu 2 kabel: SDA + SCL).
#include <LiquidCrystal_I2C.h>

// Ganti 0x27 jika LCD Anda punya alamat berbeda (coba 0x3F).
// Parameter: (alamat I2C, jumlah kolom, jumlah baris).
LiquidCrystal_I2C lcd(0x27, 16, 2);

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_subscription_t subscriber;
std_msgs__msg__String msg;

// subscription_callback: terima teks dari topic /lcd, tampilkan di LCD.
void subscription_callback(const void *msgin) {
  const std_msgs__msg__String *msg = (const std_msgs__msg__String *)msgin;
  // Konversi pesan ROS2 (char*) ke String Arduino.
  String data = String(msg->data.data);

  lcd.clear();  // Hapus tampilan LCD.

  // Cari newline (\n) pemisah baris 1 dan 2.
  int newline_pos = data.indexOf('\n');
  if (newline_pos >= 0) {
    // Ada 2 baris: substring sebelum \n = baris1, sesudah = baris2.
    String baris1 = data.substring(0, newline_pos);
    String baris2 = data.substring(newline_pos + 1);
    lcd.setCursor(0, 0);  // Kursor ke baris 1, kolom 1.
    lcd.print(baris1.substring(0, 16));  // Maks 16 karakter.
    lcd.setCursor(0, 1);  // Kursor ke baris 2, kolom 1.
    lcd.print(baris2.substring(0, 16));
  } else {
    // 1 baris saja.
    lcd.setCursor(0, 0);
    lcd.print(data.substring(0, 16));
  }
}

void setup() {
  // lcd.init(): inisialisasi LCD via I2C.
  lcd.init();
  lcd.backlight();  // Nyalakan backlight.
  lcd.clear();
  lcd.print("ROSMic ready...");  // Pesan startup.

  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "lcd_node", "", &support);

  rclc_subscription_init_default(
    &subscriber, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
    "lcd"
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
