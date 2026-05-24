#!/usr/bin/env python3
"""
teleop_keyboard.py — kontrol robot via keyboard

Node ROS2 untuk mengontrol robot secara manual dari keyboard.
Membaca input keyboard secara langsung (tanpa menunggu Enter)
dan mempublikasikannya ke topic /robot_cmd.

Tombol:
  W = MAJU    S = MUNDUR    A = KIRI    D = KANAN
  Spasi = STOP
  M = Mode MANUAL    Z = Mode AUTO
  Q = QUIT

Cara pakai:
  python3 teleop_keyboard.py
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
from std_msgs.msg import String  # Tipe pesan String ROS2
import sys
import termios   # Library untuk mengontrol terminal (mode raw input)
import tty       # Library untuk set terminal ke mode raw

class TeleopKeyboard(Node):
    def __init__(self):
        # super().__init__: inisialisasi node ROS2 dengan nama 'teleop_keyboard'
        super().__init__('teleop_keyboard')
        # Publisher: kirim perintah String ke topic /robot_cmd (queue 10)
        # Topic ini disubscribe oleh robot_monitor node (micro-ROS) di Arduino
        self.pub = self.create_publisher(String, 'robot_cmd', 10)
        self.get_logger().info("Teleop keyboard aktif!")
        self.print_help()

    def print_help(self):
        """Tampilkan petunjuk tombol di terminal"""
        print("\nKontrol Robot:")
        print("  W = MAJU     S = MUNDUR")
        print("  A = KIRI     D = KANAN")
        print("  Spasi = STOP")
        print("  M = Mode MANUAL    Z = Mode AUTO")
        print("  Q = QUIT\n")

    def get_key(self):
        """
        Baca satu karakter dari keyboard tanpa menunggu Enter.

        Cara kerja:
        1. Dapatkan file descriptor stdin (0)
        2. Simpan pengaturan terminal saat ini (termios)
        3. Set terminal ke mode 'raw' — input langsung tanpa buffering
        4. Baca 1 karakter
        5. Kembalikan pengaturan terminal ke semula
        """
        fd = sys.stdin.fileno()                   # File descriptor stdin
        old = termios.tcgetattr(fd)               # Simpan atribut terminal
        try:
            tty.setraw(fd)                         # Set mode raw
            key = sys.stdin.read(1)                # Baca 1 karakter
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)  # Kembalikan mode
        return key

    def run(self):
        """Loop utama: baca keyboard dan publish perintah"""
        # rclpy.ok(): cek apakah ROS2 masih berjalan
        while rclpy.ok():
            key = self.get_key().lower()  # Konversi ke lowercase
            msg = String()

            # Mapping tombol → perintah robot
            if key == 'w':
                msg.data = "MAJU"
            elif key == 's':
                msg.data = "MUNDUR"
            elif key == 'a':
                msg.data = "KIRI"
            elif key == 'd':
                msg.data = "KANAN"
            elif key == ' ':               # Spasi
                msg.data = "STOP"
            elif key == 'm':
                msg.data = "MANUAL"        # Ganti ke mode manual
                self.get_logger().info('Mode: MANUAL')
            elif key == 'z':
                msg.data = "AUTO"          # Ganti ke mode auto
                self.get_logger().info('Mode: AUTO')
            elif key == 'q':
                break                      # Keluar program
            else:
                continue                   # Abaikan tombol lain

            # Publish perintah ke topic /robot_cmd
            self.pub.publish(msg)

def main():
    # rclpy.init: inisialisasi ROS2
    rclpy.init()
    node = TeleopKeyboard()
    try:
        # run() bukan spin() — karena kita pakai loop manual untuk baca keyboard
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
