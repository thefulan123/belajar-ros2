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

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci

import sys


class ActionClientNode(Node):
    """
    Sebuah action client node.
    
    Tugasnya:
    - Mengirim goal ke action server
    - Menerima feedback (progres)
    - Menerima result saat selesai
    """

    def __init__(self):
        super().__init__('action_client_node')

        # Buat Action Client
        self.client = ActionClient(self, Fibonacci, 'fibonacci')

        self.get_logger().info('Menunggu action server...')

        # Tunggu server tersedia
        self.client.wait_for_server()

        self.get_logger().info('Action server ditemukan!')

        # Buat goal
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10  # Minta Fibonacci sampai urutan ke-10

        self.get_logger().info(f'Mengirim goal: Fibonacci ke-{goal_msg.order}')

        # Kirim goal, daftarkan callback
        self.send_goal_future = self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # Timer untuk cek apakah goal sudah diterima
        self.timer = self.create_timer(0.1, self.check_goal_accepted)

    def check_goal_accepted(self):
        """Cek apakah goal sudah diterima oleh server."""
        if self.send_goal_future.done():
            goal_handle = self.send_goal_future.result()

            if goal_handle.accepted:
                self.get_logger().info('Goal diterima oleh server!')
                # Tunggu result
                self.result_future = goal_handle.get_result_async()
                self.result_future.add_done_callback(self.result_callback)
            else:
                self.get_logger().error('Goal ditolak oleh server!')
                rclpy.shutdown()
                sys.exit(1)

            # Hentikan timer
            self.timer.cancel()

    def feedback_callback(self, feedback_msg):
        """
        CALLBACK — dipanggil setiap kali server mengirim feedback.
        Ini fitur yang TIDAK dimiliki service biasa.
        """
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.sequence}')

    def result_callback(self, future):
        """Dipanggil saat action selesai."""
        result = future.result().result
        self.get_logger().info(f'Result akhir: {result.sequence}')
        rclpy.shutdown()
        sys.exit(0)


def main():
    rclpy.init()
    node = ActionClientNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nAction client dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
