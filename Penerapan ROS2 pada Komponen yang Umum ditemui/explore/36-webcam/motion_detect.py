#!/usr/bin/env python3
"""
motion_detect.py — deteksi gerakan dari webcam

Membandingkan frame webcam saat ini dengan frame sebelumnya.
Jika ada perbedaan signifikan (area > threshold), publish true.
Menggunakan Gaussian blur, absolute difference, threshold, dan contour analysis.

Publish Bool ke /gerakan_deteksi jika ada perubahan frame.

Cara pakai:
  python3 motion_detect.py
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool  # Tipe pesan Boolean ROS2
import cv2  # OpenCV — library computer vision

class MotionDetect(Node):
    def __init__(self):
        # super().__init__: inisialisasi node ROS2 dengan nama 'motion_detect'
        super().__init__('motion_detect')
        # Publisher: kirim Bool ke topic /gerakan_deteksi (queue size 10)
        self.pub = self.create_publisher(Bool, 'gerakan_deteksi', 10)
        # Buka webcam default (index 0)
        self.cap = cv2.VideoCapture(0)
        # Baca frame pertama sebagai referensi (background)
        self.ret, self.prev_frame = self.cap.read()
        # Konversi frame ke grayscale — deteksi gerakan lebih mudah di 1 channel
        self.prev_gray = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
        # GaussianBlur: mengurangi noise pada gambar agar deteksi lebih stabil
        # (21,21): ukuran kernel blur; 0: sigma dihitung otomatis
        self.prev_gray = cv2.GaussianBlur(self.prev_gray, (21, 21), 0)
        # Threshold luas contour (dalam pixel) — jika > 5000 = ada gerakan
        # Nilai ini perlu disesuaikan dengan kamera dan jarak objek
        self.threshold = 5000
        # Timer 0.1 detik (10 FPS) — panggil self.detect setiap 100 ms
        self.timer = self.create_timer(0.1, self.detect)
        self.get_logger().info('Motion detect aktif!')

    def detect(self):
        """Callback timer: deteksi gerakan dengan frame differencing"""
        ret, frame = self.cap.read()
        if not ret:
            return  # Skip jika gagal baca frame

        # 1. Konversi frame saat ini ke grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 2. Blur untuk mengurangi noise
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # 3. absdiff: hitung perbedaan absolut antara frame sebelumnya dan sekarang
        diff = cv2.absdiff(self.prev_gray, gray)
        # 4. threshold: ubah diff menjadi biner (hitam-putih)
        # Jika pixel > 25 → 255 (putih), jika ≤ 25 → 0 (hitam)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        # 5. dilate: melebarkan area putih — menggabungkan region yang berdekatan
        thresh = cv2.dilate(thresh, None, iterations=2)

        # 6. findContours: cari kontur dari area putih (area yang berubah)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 7. Analisis kontur — jika ada kontur dengan luas > threshold → motion = True
        motion = False
        for c in contours:
            # contourArea: hitung luas area contour dalam pixel
            if cv2.contourArea(c) > self.threshold:
                motion = True
                break  # Cukup satu kontur besar untuk mendeteksi gerakan

        # Update frame sebelumnya untuk iterasi berikutnya
        self.prev_gray = gray

        # Buat dan publish pesan Bool
        msg = Bool()
        msg.data = motion
        self.pub.publish(msg)

    def __del__(self):
        """Destructor: bebaskan webcam"""
        self.cap.release()

def main():
    # rclpy.init: inisialisasi ROS2
    rclpy.init()
    node = MotionDetect()
    try:
        # rclpy.spin: loop utama — proses callback selamanya
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
