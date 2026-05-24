/*
 * speaker.ino — putar MP3 via ROS2 (DFPlayer Mini)
 * 
 * Subscribe ke topic /speaker (Int32)
 * >0  = putar track nomor itu
 * 0   = stop
 * -1  = next track
 * -2  = previous
 * -3  = volume up
 * -4  = volume down
 * 
 * Board: Arduino UNO (SoftwareSerial) / ESP32 (UART2)
 * 
 * BUTUH LIBRARY: DFRobotDFPlayerMini
 * 
 * Koneksi: lihat wiring.md
 * 
 * DFPlayer Mini adalah modul MP3 player yang membaca file dari microSD
 * Komunikasi via UART (Serial) — di UNO pakai SoftwareSerial
 */

// micro_ros_arduino: library micro-ROS untuk komunikasi ROS2
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/int32.h>

// SoftwareSerial: library Arduino untuk membuat port serial virtual di pin digital
// Digunakan karena DFPlayer butuh UART tambahan (Serial utama dipakai micro-ROS)
#include <SoftwareSerial.h>
// DFRobotDFPlayerMini: library khusus untuk mengontrol modul DFPlayer Mini
// Menyediakan fungsi play(), stop(), next(), volume(), dll
#include <DFRobotDFPlayerMini.h>

// Pin untuk komunikasi serial dengan DFPlayer Mini
#define DF_RX 2  // RX Arduino → TX DFPlayer (terima data dari DFPlayer)
#define DF_TX 3  // TX Arduino → RX DFPlayer (kirim perintah ke DFPlayer)

// SoftwareSerial(rxPin, txPin): buat port serial virtual di pin D2 dan D3
SoftwareSerial softSerial(DF_RX, DF_TX);
// DFPlayer: objek untuk mengontrol modul DFPlayer Mini
DFRobotDFPlayerMini dfPlayer;

// Executor — penjadwal callback
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
// Subscription — menerima perintah dari topic "/speaker"
rcl_subscription_t subscriber;
std_msgs__msg__Int32 msg;
// Menyimpan volume saat ini (default 15 dari skala 0-30)
int current_volume = 15;

// subscription_callback: dipanggil setiap kali ada pesan baru di topic "speaker"
// msgin: pointer ke data mentah, di-cast ke Int32 untuk dibaca
void subscription_callback(const void *msgin) {
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  int cmd = msg->data;

  // Perintah positif: putar track nomor tertentu
  if (cmd > 0) {
    dfPlayer.play(cmd);  // dfPlayer.play(1) = putar file 001.mp3
  } else if (cmd == 0) {
    dfPlayer.stop();     // Hentikan pemutaran
  } else if (cmd == -1) {
    dfPlayer.next();     // Lompat ke track berikutnya
  } else if (cmd == -2) {
    dfPlayer.previous(); // Kembali ke track sebelumnya
  } else if (cmd == -3) {
    // min(30, current_volume + 2): naikkan volume, maks 30
    current_volume = min(30, current_volume + 2);
    dfPlayer.volume(current_volume);  // Set volume DFPlayer
  } else if (cmd == -4) {
    // max(0, current_volume - 2): turunkan volume, min 0
    current_volume = max(0, current_volume - 2);
    dfPlayer.volume(current_volume);
  }
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Inisialisasi SoftwareSerial pada 9600 baud (baud rate default DFPlayer)
  softSerial.begin(9600);
  // dfPlayer.begin(softSerial): coba koneksi ke DFPlayer via SoftwareSerial
  if (!dfPlayer.begin(softSerial)) {
    // Jika DFPlayer tidak merespon, cetak error ke Serial monitor
    Serial.println("ERROR: DFPlayer tidak terdeteksi!");
  }
  // Set volume awal DFPlayer
  dfPlayer.volume(current_volume);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "speaker_node", "", &support);

  // rclc_subscription_init_default: daftarkan subscriber untuk topic "speaker"
  // Menerima pesan Int32 untuk kontrol pemutaran
  rclc_subscription_init_default(&subscriber, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), "speaker");

  // Executor: 1 handle untuk subscription
  rclc_executor_init(&executor, &support, 1, &allocator);
  // Daftarkan subscription dengan callback — ON_NEW_DATA = panggil saat ada data baru
  rclc_executor_add_subscription(&executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
