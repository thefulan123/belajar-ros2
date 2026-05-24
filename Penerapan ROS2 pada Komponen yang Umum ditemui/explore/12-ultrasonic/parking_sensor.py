#!/usr/bin/env python3
"""
parking_sensor.py — simulasi parking sensor mobil

Makin dekat jarak, makin cepat bunyi buzzer.

Cara pakai:
  python3 parking_sensor.py
"""


# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE — rclpy (ROS2 Python)
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai:
#
# 1. rclpy
#    - Library utama ROS2 Python. WAJIB untuk semua program.
#    - rclpy.init() = inisialisasi, rclpy.spin() = loop utama.
#
# 2. Node (dari rclpy.node)
#    - Kelas dasar node ROS2. Setiap node punya nama unik.
#    - Bisa memiliki publisher, subscriber, timer, service, dll.
#
# 3. Publisher (create_publisher())
#    - Mengirim data ke topic ROS2 secara periodik.
#    - Parameter: tipe_msg, nama_topic, queue_size.
#    - Method: publish(msg) — kirim ke semua subscriber.
#
# 4. Subscription (create_subscription())
#    - Menerima data dari topic ROS2.
#    - Parameter: tipe_msg, nama_topic, callback, qos.
#    - Callback dipanggil otomatis saat ada data masuk.
#
# 5. Timer (create_timer())
#    - Eksekusi fungsi callback secara periodik.
#    - Parameter: interval_detik, callback_function.
#
# 6. Callback
#    - Fungsi yang dipanggil OTOMATIS oleh ROS2.
#    - Bisa dari: timer, subscriber, service, action.
#    - Tidak dipanggil langsung oleh kode kita.
#
# 7. Tipe pesan standar:
#    - std_msgs.msg.Bool     → bool (true/false)
#    - std_msgs.msg.Int32    → int (angka bulat)
#    - std_msgs.msg.Float64  → float (angka desimal)
#    - std_msgs.msg.String   → string (teks)
# ═══════════════════════════════════════════════════════════════

import rclpy                       # Library ROS2 Python — menghubungkan script ke ROS2
from rclpy.node import Node        # Class Node — membuat node ROS2 di Python
from std_msgs.msg import Float64, Int32  # Tipe pesan: Float64 (jarak) dan Int32 (frekuensi buzzer)
from threading import Lock         # Thread Lock — amankan akses data antar thread

class ParkingSensor(Node):                               # Node ROS2 — simulasi parking sensor mobil
    def __init__(self):
        super().__init__('parking_sensor')               # Inisialisasi node dengan nama "parking_sensor"
        self.pub = self.create_publisher(Int32, 'buzzer', 10)  # Publisher ke topic "buzzer"
        self.sub = self.create_subscription(             # Subscribe ke topic "jarak"
            Float64, 'jarak', self.cb_jarak, 10)
        self.current_distance = 400.0                    # Jarak saat ini (default: jauh)
        self.lock = Lock()                                # Lock untuk akses thread-safe
        self.timer = self.create_timer(0.1, self.beep_timer)  # Timer 100ms untuk pola beep
        self.beep_count = 0                               # Counter untuk pola beep warning
        print("Parking sensor aktif!")

    def cb_jarak(self, msg):                             # Callback — dipanggil saat ada data jarak
        with self.lock:                                   # Amankan akses dengan Lock
            self.current_distance = msg.data              # Simpan jarak terbaru

    def beep_timer(self):                                # Method — bunyikan buzzer sesuai jarak
        with self.lock:
            d = self.current_distance                     # Ambil jarak terbaru (thread-safe)

        if d < 10:                                        # Jarak sangat dekat — danger!
            # Beep terus menerus — frekuensi makin tinggi makin dekat
            freq = (10 - d) * 300 + 1000
            buzzer_msg = Int32()
            buzzer_msg.data = int(freq)
            self.pub.publish(buzzer_msg)                  # Bunyi terus
            self.get_logger().warn(f'DANGER: {d:.0f} cm')
        elif d < 30:                                      # Jarak menengah — warning
            # Beep cepat — interval beep makin rapat makin dekat
            interval = int(d / 30 * 5) + 1
            if self.beep_count % interval == 0:
                buzzer_msg = Int32()
                buzzer_msg.data = 1500                    # Frekuensi beep 1500 Hz
                self.pub.publish(buzzer_msg)
                self.get_logger().info(f'Warning: {d:.0f} cm')
            else:
                buzzer_msg = Int32()
                buzzer_msg.data = 0                       # Mati di antara beep
                self.pub.publish(buzzer_msg)
            self.beep_count += 1
        else:                                             # Jarak aman
            # Silent — tidak ada bunyi
            buzzer_msg = Int32()
            buzzer_msg.data = 0
            self.pub.publish(buzzer_msg)
            self.beep_count = 0

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = ParkingSensor()                          # Buat instance node ParkingSensor
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
