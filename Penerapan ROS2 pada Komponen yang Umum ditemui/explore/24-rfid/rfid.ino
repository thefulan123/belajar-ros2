/*
 * rfid.ino — baca RFID tag (RC522) via ROS2
 * 
 * Publish ke topic /rfid (String)
 * Format UID: "A1:B2:C3:D4"
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: MFRC522 by GithubCommunity
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/string.h>

// SPI.h: komunikasi SPI — digunakan oleh modul RFID RC522.
#include <SPI.h>
// MFRC522.h: library untuk reader RFID RC522 (13.56 MHz).
#include <MFRC522.h>

#if defined(ESP32)
  #define SS_PIN  5   // SPI Chip Select (SDA)
  #define RST_PIN 4   // Reset pin
#else
  #define SS_PIN  10
  #define RST_PIN 9
#endif

// Objek MFRC522: parameter = pin SS (SDA) dan RST.
MFRC522 rfid(SS_PIN, RST_PIN);
// Key default untuk autentikasi (pabrik).
MFRC522::MIFARE_Key key;

rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

std_msgs__msg__String msg;
char uid_str[20];    // Buffer string UID (contoh: "A1:B2:C3:D4").
String last_uid = ""; // UID terakhir — hindari publish duplikat.

// timer_callback: cek kartu RFID setiap 200ms.
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // PICC_IsNewCardPresent(): apakah ada kartu baru?
  if (!rfid.PICC_IsNewCardPresent()) return;
  // PICC_ReadCardSerial(): baca UID kartu.
  if (!rfid.PICC_ReadCardSerial()) return;

  // Build UID string dengan format hex: "A1:B2:C3:D4".
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (i > 0) uid += ":";
    if (rfid.uid.uidByte[i] < 0x10) uid += "0";  // Leading zero.
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  uid.toUpperCase();  // Huruf kapital.

  // Hanya publish jika UID berbeda dari terakhir (mencegah spam).
  if (uid != last_uid) {
    last_uid = uid;
    uid.toCharArray(uid_str, sizeof(uid_str));
    msg.data.data = uid_str;
    msg.data.size = strlen(uid_str);
    rcl_publish(&publisher, &msg, NULL);
  }

  // Hentikan komunikasi dengan kartu.
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // SPI.begin(): inisialisasi bus SPI (SCK, MOSI, MISO, SS).
  SPI.begin();
  // PCD_Init(): inisialisasi modul RC522.
  rfid.PCD_Init();

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "rfid_node", "", &support);

  // Publisher untuk topic /rfid (String).
  rclc_publisher_init_default(
    &publisher, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String),
    "rfid"
  );

  // Timer 200ms — periksa kartu 5x per detik.
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(200), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
