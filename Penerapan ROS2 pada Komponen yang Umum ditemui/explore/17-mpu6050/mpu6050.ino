/*
 * mpu6050.ino — baca accel + gyro via ROS2 (I2C)
 * 
 * Publish ke 6 topic Float64:
 * /accel_x, /accel_y, /accel_z
 * /gyro_x, /gyro_y, /gyro_z
 * 
 * Board: Arduino UNO / ESP32
 * 
 * BUTUH LIBRARY: MPU6050 by Electronic Cats
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
#include <std_msgs/msg/float64.h>

// Wire.h: library I2C bawaan Arduino — untuk komunikasi dengan MPU6050.
#include <Wire.h>
// MPU6050.h: library untuk sensor IMU MPU6050 (accel + gyro).
#include <MPU6050.h>

// Objek MPU6050 (alamat I2C default: 0x68).
MPU6050 mpu;

// 6 publisher untuk accel (x,y,z) dan gyro (x,y,z).
rcl_publisher_t pub_ax, pub_ay, pub_az;
rcl_publisher_t pub_gx, pub_gy, pub_gz;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
// timer: pemicu periodik untuk membaca sensor.
rcl_timer_t timer;

// Buffer pesan Float64 untuk setiap topic.
std_msgs__msg__Float64 msg_ax, msg_ay, msg_az;
std_msgs__msg__Float64 msg_gx, msg_gy, msg_gz;

// timer_callback: dipanggil setiap 50ms oleh timer.
void timer_callback(rcl_timer_t *timer, int64_t last_call_time) {
  (void)last_call_time;
  if (timer == NULL) return;

  // Variabel untuk data mentah dari sensor.
  int16_t ax, ay, az, gx, gy, gz;
  // getMotion6(): baca accelerometer (ax,ay,az) dan gyroscope (gx,gy,gz).
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Konversi ke G dan deg/s:
  //   Accelerometer: ±2g → 16384 LSB/g
  //   Gyroscope:     ±250°/s → 131 LSB/(°/s)
  msg_ax.data = ax / 16384.0;
  msg_ay.data = ay / 16384.0;
  msg_az.data = az / 16384.0;
  msg_gx.data = gx / 131.0;
  msg_gy.data = gy / 131.0;
  msg_gz.data = gz / 131.0;

  // rcl_publish(): kirim data ke setiap topic ROS2.
  rcl_publish(&pub_ax, &msg_ax, NULL);
  rcl_publish(&pub_ay, &msg_ay, NULL);
  rcl_publish(&pub_az, &msg_az, NULL);
  rcl_publish(&pub_gx, &msg_gx, NULL);
  rcl_publish(&pub_gy, &msg_gy, NULL);
  rcl_publish(&pub_gz, &msg_gz, NULL);
}

void setup() {
  Serial.begin(115200);
  set_microros_serial_transports(Serial);
  delay(2000);

  // Wire.begin(): inisialisasi bus I2C (SDA = A4, SCL = A5 di UNO).
  Wire.begin();
  // mpu.initialize(): inisialisasi sensor MPU6050.
  mpu.initialize();
  // testConnection(): verifikasi sensor merespon.
  if (!mpu.testConnection()) {
    Serial.println("ERROR: MPU6050 tidak terdeteksi!");
    while (1);  // Hentikan program jika sensor tidak ada.
  }

  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "mpu6050_node", "", &support);

  // Inisialisasi 6 publisher untuk accel_x/y/z dan gyro_x/y/z.
  rclc_publisher_init_default(&pub_ax, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "accel_x");
  rclc_publisher_init_default(&pub_ay, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "accel_y");
  rclc_publisher_init_default(&pub_az, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "accel_z");
  rclc_publisher_init_default(&pub_gx, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "gyro_x");
  rclc_publisher_init_default(&pub_gy, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "gyro_y");
  rclc_publisher_init_default(&pub_gz, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float64), "gyro_z");

  // Timer 50ms → publish data sensor 20 kali per detik.
  rclc_timer_init_default(&timer, &support, RCL_MS_TO_NS(50), timer_callback);
  rclc_executor_init(&executor, &support, 1, &allocator);
  rclc_executor_add_timer(&executor, &timer);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
  delay(10);
}
