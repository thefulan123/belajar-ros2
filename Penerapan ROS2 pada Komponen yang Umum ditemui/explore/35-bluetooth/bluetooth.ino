/*
 * bluetooth.ino — bridge Bluetooth HC-05 via ROS2
 * 
 * Menjembatani komunikasi antara ROS2 dan perangkat Bluetooth (HC-05).
 * 
 * Subscribe: /bluetooth_out (String) — kirim data dari ROS2 ke Bluetooth
 * Publish: /bluetooth_in (String) — terima data dari Bluetooth ke ROS2
 * 
 * Board: Arduino UNO (SoftwareSerial) / ESP32 (UART2)
 * 
 * Koneksi: lihat wiring.md
 * 
 * Alur data:
 *   ROS2 → topic /bluetooth_out → Arduino → HC-05 → device Bluetooth
 *   Device Bluetooth → HC-05 → Arduino → topic /bluetooth_in → ROS2
 */

// micro_ros_arduino: library micro-ROS untuk Arduino/ESP32
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
// std_msgs/msg/string.h: tipe pesan String untuk ROS2
// Berisi field .data.data (char*) dan .data.size (panjang string)
#include <std_msgs/msg/string.h>

// SoftwareSerial: port serial virtual untuk komunikasi dengan HC-05
// Serial utama (pada pin D0/D1) sudah dipakai micro-ROS
#include <SoftwareSerial.h>

#define BT_RX 2  // RX Arduino ← TX HC-05 (terima dari Bluetooth)
#define BT_TX 3  // TX Arduino → RX HC-05 (kirim ke Bluetooth)
// Inisialisasi SoftwareSerial untuk HC-05
SoftwareSerial btSerial(BT_RX, BT_TX);

// Publisher: kirim data Bluetooth → ROS2 (topic /bluetooth_in)
rcl_publisher_t pub_in;
// Subscription: terima data ROS2 → Bluetooth (topic /bluetooth_out)
rcl_subscription_t sub_out;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Pesan untuk data masuk (Bluetooth → ROS2)
std_msgs__msg__String msg_in;
// Pesan untuk data keluar (ROS2 → Bluetooth)
std_msgs__msg__String msg_out;
// Buffer untuk menampung data dari Bluetooth sebelum dipublish
char bt_buffer[64];
// Index buffer — posisi penulisan karakter berikutnya
int bt_idx = 0;

// sub_callback: dipanggil saat ada pesan baru di topic "bluetooth_out"
// Mengirim data dari ROS2 ke perangkat Bluetooth via HC-05
void sub_callback(const void *msgin) {
  const std_msgs__msg__String *msg = (const std_msgs__msg__String *)msgin;
  // Kirim string ke HC-05 via SoftwareSerial
  btSerial.print(msg->data.data);
  btSerial.print('\n');  // Tambah newline sebagai terminator
}

// timer_callback: dipanggil setiap 100 ms
// Membaca data dari Bluetooth dan mempublish-nya ke ROS2
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // Baca data dari Bluetooth HC-05
  // btSerial.available(): jumlah byte tersedia di buffer serial
  while (btSerial.available() && bt_idx < 63) {
    char c = btSerial.read();  // Baca satu karakter
    // Newline atau carriage return = akhir satu pesan
    if (c == '\n' || c == '\r') {
      if (bt_idx > 0) {  // Ada data yang terkumpul
        bt_buffer[bt_idx] = '\0';  // Null-terminator untuk string C
        msg_in.data.data = bt_buffer;  // Pointer ke buffer
        msg_in.data.size = bt_idx;     // Panjang data
        rcl_publish(&pub_in, &msg_in, NULL);  // Publish ke ROS2
        bt_idx = 0;  // Reset buffer untuk pesan berikutnya
      }
    } else {
      bt_buffer[bt_idx++] = c;  // Simpan karakter di buffer
    }
  }
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Inisialisasi HC-05 pada baud rate 9600 (default pabrik)
  btSerial.begin(9600);

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "bluetooth_node", "", &support);

  // Publisher untuk data dari Bluetooth → topic /bluetooth_in
  rclc_publisher_init_default(&pub_in, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String), "bluetooth_in");
  // Subscriber untuk data dari ROS2 → Bluetooth via topic /bluetooth_out
  rclc_subscription_init_default(&sub_out, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String), "bluetooth_out");

  // Executor dengan 2 handle: 1 subscription + 1 timer
  rclc_executor_init(&executor, &support, 2, &allocator);
  // Daftarkan subscription untuk menerima perintah dari ROS2
  rclc_executor_add_subscription(&executor, &sub_out, &msg_out, &sub_callback, ON_NEW_DATA);
  // Timer 100 ms untuk polling data dari Bluetooth
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(100), timer_callback);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
