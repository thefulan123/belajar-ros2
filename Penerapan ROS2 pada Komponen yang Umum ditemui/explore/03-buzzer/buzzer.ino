/*
 * buzzer.ino — kontrol buzzer via ROS2
 * 
 * Subscribe ke topic /buzzer (Int32)
 * 0    → mati
 * >0   → bunyi dengan frekuensi (Hz)
 * 
 * Board: Arduino UNO / ESP32
 * 
 * Koneksi: lihat wiring.md
 */

#include <micro_ros_arduino.h>  // Library micro-ROS untuk Arduino — menghubungkan Arduino ke ROS2
#include <rcl/rcl.h>            // Library ROS2 Client Library — API inti ROS2 di C
#include <rclc/rclc.h>          // Library RCLC — helper untuk memudahkan inisialisasi ROS2
#include <rclc/executor.h>      // Library executor RCLC — menjalankan callback secara periodik
#include <std_msgs/msg/int32.h> // Tipe pesan Int32 (integer 32-bit) — untuk frekuensi buzzer

#if defined(ESP32)             // Dual board support: cek apakah board adalah ESP32
  #define BUZZER_PIN 27        // Pin GPIO 27 untuk ESP32
#else                           // Jika bukan ESP32, berarti Arduino UNO
  #define BUZZER_PIN 5         // Pin digital 5 untuk Arduino UNO
#endif

rclc_executor_t executor;         // Executor — mengelola eksekusi callback ROS2
rclc_support_t support;           // Support structure — wadah inisialisasi ROS2
rcl_allocator_t allocator;        // Allocator — pengelola memori ROS2
rcl_node_t node;                  // Node — entitas utama ROS2 untuk komunikasi
rcl_subscription_t subscriber;    // Subscriber — penerima pesan dari topic
std_msgs__msg__Int32 msg;         // Variabel pesan Int32 — menampung nilai frekuensi
int current_freq = 0;             // Frekuensi buzzer saat ini (0 = mati)

void subscription_callback(const void *msgin) {       // Callback — dipanggil otomatis saat ada pesan masuk
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;  // Cast pointer ke tipe Int32
  current_freq = msg->data;                           // Simpan frekuensi dari pesan

  if (current_freq <= 0) {                            // Jika 0 atau negatif, matikan buzzer
    noTone(BUZZER_PIN);                               // Hentikan tone
    digitalWrite(BUZZER_PIN, LOW);                    // Pastikan pin LOW
  } else {                                            // Jika > 0, bunyikan dengan frekuensi tersebut
    tone(BUZZER_PIN, current_freq);                   // tone() → menghasilkan gelombang PWM suara
  }
}

void setup() {                                     // setup() — dijalankan sekali saat board menyala / reset
  pinMode(BUZZER_PIN, OUTPUT);                     // Set pin buzzer sebagai OUTPUT (mengirim sinyal)
  digitalWrite(BUZZER_PIN, LOW);                   // Pastikan buzzer mati saat awal

  Serial.begin(115200);                            // Inisialisasi Serial USB dengan baud rate 115200
  set_microros_serial_transports(Serial);          // Hubungkan micro-ROS ke Serial USB sebagai transport
  delay(2000);                                     // Tunggu 2 detik agar micro-ROS siap

  allocator = rcl_get_default_allocator();         // Dapatkan memory allocator default ROS2
  rclc_support_init(&support, 0, NULL, &allocator);// Inisialisasi ROS2 support structure
  rclc_node_init_default(&node, "buzzer_node", "", &support);  // Buat node ROS2 bernama "buzzer_node"

  rclc_subscription_init_default(                 // Inisialisasi subscriber untuk topic "buzzer"
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32),  // Dapatkan type support untuk pesan Int32
    "buzzer"                                      // Nama topic yang akan di-subscribe
  );

  rclc_executor_init(&executor, &support, 1, &allocator);  // Buat executor dengan 1 callback
  rclc_executor_add_subscription(                 // Daftarkan subscriber ke executor
    &executor, &subscriber, &msg,
    &subscription_callback, ON_NEW_DATA           // Callback dipanggil hanya saat ada data baru
  );
}

void loop() {                                                       // loop() — dijalankan terus-menerus setelah setup()
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));           // Proses callback ROS2 yang masuk (timeout 100ms)
  delay(10);                                                        // Delay kecil agar CPU tidak 100%
}
