#!/usr/bin/env python3
# ============================================================
# action_client.py — Action Client ROS2
#
# Node ini mengirim goal ke action server /fibonacci.
# Menerima feedback (progress) selama proses berjalan.
#
# Cara jalankan:
#   (Pastikan action_server.py sudah jalan)
#   python3 action_client.py
# ============================================================

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.
from rclpy.action import ActionClient  # (3) Class untuk membuat Action Client ROS2.
from example_interfaces.action import Fibonacci  # (4) Tipe action Fibonacci — sama dengan server.

import sys  # (5) Library Python standar untuk sys.exit().


class ActionClientNode(Node):
    # (6) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah action client node.
    
    Tugasnya:
    - Mengirim goal ke action server
    - Menerima feedback (progres)
    - Menerima result saat selesai
    """

    def __init__(self):
        # (7) Panggil constructor parent dengan nama node UNIK.
        super().__init__('action_client_node')

        # (8) MEMBUAT ACTION CLIENT — untuk mengirim goal ke server.
        # Sintaks ROS2: ActionClient(self, TipeAction, 'nama_action')
        # Parameter:
        #   1. Node reference: self
        #   2. Tipe action: Fibonacci
        #   3. Nama action: 'fibonacci' — harus SAMA dengan server
        self.client = ActionClient(self, Fibonacci, 'fibonacci')

        # (9) Log bahwa client sedang mencari server.
        self.get_logger().info('Menunggu action server...')

        # (10) MENUNGGU SERVER TERSEDIA — mirip service client.
        # wait_for_server() memblokir sampai server terhubung.
        self.client.wait_for_server()

        # (11) Log bahwa server ditemukan.
        self.get_logger().info('Action server ditemukan!')

        # (12) MEMBUAT GOAL — objek yang dikirim ke server.
        # Fibonacci.Goal memiliki field: order (int32).
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10  # (13) Minta deret Fibonacci sampai urutan ke-10.

        # (14) Log goal yang akan dikirim.
        self.get_logger().info(f'Mengirim goal: Fibonacci ke-{goal_msg.order}')

        # (15) MENGIRIM GOAL SECARA ASYNCHRONOUS.
        # Sintaks: self.client.send_goal_async(goal, feedback_callback)
        # Parameter:
        #   1. goal_msg: objek Goal yang sudah diisi
        #   2. feedback_callback: fungsi yang dipanggil SETIAP ada feedback
        # send_goal_async() langsung kembali, hasilnya di future.
        self.send_goal_future = self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # (16) Timer untuk mengecek apakah goal sudah diterima server.
        self.timer = self.create_timer(0.1, self.check_goal_accepted)

    def check_goal_accepted(self):
        # (17) CALLBACK TIMER — cek apakah server sudah menerima goal.
        """Cek apakah goal sudah diterima oleh server."""
        # (18) Cek apakah future sudah selesai (server sudah merespon).
        if self.send_goal_future.done():
            # (19) Ambil goal_handle dari future.
            goal_handle = self.send_goal_future.result()
            # (20) goal_handle.accepted — True jika goal diterima.
            if goal_handle.accepted:
                self.get_logger().info('Goal diterima oleh server!')
                # (21) Minta result secara async.
                self.result_future = goal_handle.get_result_async()
                # (22) Daftarkan callback untuk result.
                self.result_future.add_done_callback(self.result_callback)
            else:
                # (23) Goal ditolak server.
                self.get_logger().error('Goal ditolak oleh server!')
                rclpy.shutdown()
                sys.exit(1)

            # (24) Hentikan timer — tidak perlu cek lagi.
            self.timer.cancel()

    def feedback_callback(self, feedback_msg):
        # (25) CALLBACK FEEDBACK — dipanggil SETIAP ada feedback dari server.
        # Ini fitur UNIK Action — Service TIDAK punya feedback.
        """
        CALLBACK — dipanggil setiap kali server mengirim feedback.
        Ini fitur yang TIDAK dimiliki service biasa.
        """
        # (26) Ambil feedback (progress deret Fibonacci).
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.sequence}')

    def result_callback(self, future):
        # (27) CALLBACK RESULT — dipanggil saat action selesai.
        """Dipanggil saat action selesai."""
        # (28) Ambil result akhir dari future.
        result = future.result().result
        self.get_logger().info(f'Result akhir: {result.sequence}')
        # (29) Hentikan node — action selesai.
        rclpy.shutdown()
        sys.exit(0)


def main():
    # (30) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    # (31) Membuat instance node ActionClientNode.
    node = ActionClientNode()
    
    try:
        # (32) rclpy.spin(node) — loop utama, jalankan timer & callback.
        rclpy.spin(node)
    except KeyboardInterrupt:
        # (33) Tangani Ctrl+C.
        print("\nAction client dihentikan.")
    finally:
        # (34) Bersihkan node dan shutdown ROS2.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    # (35) Entry point.
    main()
