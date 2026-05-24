#!/usr/bin/env python3
"""
logger_node.py — logging data suhu & kelembapan ke CSV

Cara pakai:
  python3 logger_node.py
  # Data otomatis tersimpan ke dht_log.csv
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
from std_msgs.msg import Float64   # Tipe pesan Float64 (desimal) — untuk suhu & kelembapan
from datetime import datetime      # Library datetime — untuk timestamp logging
import csv                         # Library CSV — menyimpan data ke file CSV

class LoggerNode(Node):                                  # Node ROS2 untuk logging data sensor ke CSV
    def __init__(self):
        super().__init__('logger_node')                  # Inisialisasi node dengan nama "logger_node"
        self.suhu = 0.0                                  # Variabel menyimpan suhu terbaru
        self.kelembapan = 0.0                            # Variabel menyimpan kelembapan terbaru

        self.sub_suhu = self.create_subscription(        # Subscribe ke topic "suhu"
            Float64, 'suhu', self.cb_suhu, 10)
        self.sub_kelembapan = self.create_subscription(  # Subscribe ke topic "kelembapan"
            Float64, 'kelembapan', self.cb_kelembapan, 10)

        self.file = open('dht_log.csv', 'a', newline='') # Buka file CSV untuk append
        self.writer = csv.writer(self.file)               # Buat CSV writer
        # Header CSV — tulis hanya jika file kosong
        self.file.seek(0, 2)                             # Pindah ke akhir file
        if self.file.tell() == 0:                        # Jika file kosong (0 bytes)
            self.writer.writerow(['timestamp', 'suhu', 'kelembapan'])  # Tulis header

        self.timer = self.create_timer(5.0, self.log_data)  # Timer periodik 5 detik untuk log
        print("Logger aktif. Data disimpan tiap 5 detik ke dht_log.csv")

    def cb_suhu(self, msg):                              # Callback — dipanggil saat ada data suhu masuk
        self.suhu = msg.data                             # Simpan nilai suhu

    def cb_kelembapan(self, msg):                        # Callback — dipanggil saat ada data kelembapan masuk
        self.kelembapan = msg.data                       # Simpan nilai kelembapan

    def log_data(self):                                  # Method — tulis data ke CSV setiap 5 detik
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Buat timestamp sekarang
        self.writer.writerow([ts, self.suhu, self.kelembapan])  # Tulis baris CSV
        self.file.flush()                                # Paksa penulisan ke disk
        print(f"Logged: {ts} | Suhu: {self.suhu:.1f}C | RH: {self.kelembapan:.1f}%")

    def __del__(self):                                   # Destructor — dipanggil saat objek dihapus
        self.file.close()                                # Tutup file CSV

def main():                                         # Fungsi utama program
    rclpy.init()                                    # Inisialisasi ROS2
    node = LoggerNode()                             # Buat instance node LoggerNode
    try:
        rclpy.spin(node)                            # Loop forever — proses callback terus
    except KeyboardInterrupt:                       # Tangani Ctrl+C
        pass
    finally:
        node.destroy_node()                         # Bersihkan node
        rclpy.shutdown()                            # Matikan ROS2

if __name__ == '__main__':                          # Entry point ketika script dijalankan langsung
    main()
