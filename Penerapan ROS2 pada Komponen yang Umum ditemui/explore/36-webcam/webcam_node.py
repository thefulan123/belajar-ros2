#!/usr/bin/env python3
"""
webcam_node.py — publish gambar webcam ke ROS2

Mengambil frame dari webcam laptop/PC dan mempublikasikannya
sebagai pesan sensor_msgs/Image ke topic /webcam.

Cara pakai:
  python3 webcam_node.py
  # Buka rqt_image_view untuk lihat hasil

Dependencies:
  pip3 install opencv-python
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

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # Tipe pesan ROS2 untuk gambar
from cv_bridge import CvBridge  # Konverter: OpenCV ↔ ROS Image
import cv2  # OpenCV — library computer vision

class WebcamNode(Node):
    def __init__(self):
        # super().__init__: panggil konstruktor Node ROS2 dengan nama 'webcam_node'
        super().__init__('webcam_node')
        # create_publisher: buat publisher untuk topic 'webcam' dengan queue size 10
        # Tipe pesan: Image (sensor_msgs/Image) — standar ROS2 untuk gambar
        self.pub = self.create_publisher(Image, 'webcam', 10)
        # CvBridge: objek untuk konversi antara OpenCV Mat dan ROS Image
        self.bridge = CvBridge()
        # cv2.VideoCapture(0): buka webcam default (index 0)
        self.cap = cv2.VideoCapture(0)

        # Cek apakah webcam berhasil dibuka
        if not self.cap.isOpened():
            # get_logger(): sistem logging ROS2 — output ke terminal
            self.get_logger().error('Tidak bisa buka webcam!')
            return

        # create_timer: panggil self.capture_frame setiap 0.05 detik (~20 FPS)
        self.timer = self.create_timer(0.05, self.capture_frame)
        self.get_logger().info('Webcam node aktif! Topic: /webcam')

    def capture_frame(self):
        """Callback timer: tangkap frame webcam dan publish ke ROS2"""
        # cap.read(): baca frame dari webcam — return (ret, frame)
        # ret: True jika berhasil, frame: gambar dalam format BGR (numpy array)
        ret, frame = self.cap.read()
        if ret:
            # cv2_to_imgmsg: konversi frame OpenCV (numpy) → ROS Image message
            # 'bgr8': encoding warna (OpenCV default: Blue-Green-Red, 8-bit)
            msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
            # publish: kirim image message ke topic /webcam
            self.pub.publish(msg)

    def __del__(self):
        # Destructor: release webcam saat node dihentikan
        self.cap.release()

def main():
    # rclpy.init(): inisialisasi ROS2 — harus dipanggil sebelum membuat node
    rclpy.init()
    # Buat instance node WebcamNode
    node = WebcamNode()
    try:
        # rclpy.spin(): loop utama ROS2 — blocking, terus proses callback
        # Tidak akan kembali sampai node di-shutdown (Ctrl+C)
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Tangkap Ctrl+C agar exit gracefully
        pass
    finally:
        # node.destroy_node(): bersihkan resource node
        node.destroy_node()
        # rclpy.shutdown(): matikan ROS2 dan bersihkan semua resource
        rclpy.shutdown()

if __name__ == '__main__':
    main()
