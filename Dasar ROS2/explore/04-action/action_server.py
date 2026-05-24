#!/usr/bin/env python3
# ============================================================
# action_server.py — Action Server ROS2
#
# Action mirip service, tapi:
# - Bisa memberikan feedback selama proses
# - Bisa di-cancel (dibatalkan)
# - Cocok untuk tugas yang butuh waktu lama
#
# Contoh: robot jalan ke titik tujuan.
#
# Action yang digunakan: Fibonacci
# - Goal: urutan ke-n (order)
# - Feedback: progress saat ini
# - Result: deret Fibonacci lengkap
#
# Cara jalankan:
#   python3 action_server.py
#
# Lalu di terminal lain:
#   python3 action_client.py
# ============================================================

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

# Fibonacci adalah tipe action bawaan ROS2
# Goal: int32 order
# Feedback: int32[] sequence (sebagian)
# Result: int32[] sequence (lengkap)
from example_interfaces.action import Fibonacci


class ActionServerNode(Node):
    """
    Sebuah action server node.
    
    Tugasnya:
    - Menerima goal dari client
    - Memproses (dengan feedback berkala)
    - Mengembalikan result
    """

    def __init__(self):
        super().__init__('action_server_node')

        # Buat Action Server
        # Parameter:
        #   1. Tipe action: Fibonacci
        #   2. Nama action: 'fibonacci'
        #   3. Execute callback: fungsi yang memproses goal
        self.action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

        self.get_logger().info('Action server /fibonacci siap!')

    async def execute_callback(self, goal_handle):
        """
        Fungsi ini dipanggil saat client mengirim goal.
        
        Parameter:
        - goal_handle: objek yang mengontrol eksekusi goal
        
        Selama proses, kita bisa:
        - Mengirim feedback ke client
        - Mengecek apakah client meminta cancel
        - Mengembalikan result
        """

        # Ambil goal request
        order = goal_handle.request.order
        self.get_logger().info(f'Menerima goal: Fibonacci ke-{order}')

        # Kirim feedback: proses dimulai
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        # Hitung deret Fibonacci
        for i in range(1, order):
            # Cek apakah client meminta cancel
            if goal_handle.is_cancel_requested:
                self.get_logger().info('Goal dibatalkan oleh client')
                goal_handle.canceled()
                return Fibonacci.Result()

            # Hitung nilai Fibonacci berikutnya
            fib_n = feedback_msg.sequence[i] + feedback_msg.sequence[i - 1]
            feedback_msg.sequence.append(fib_n)

            # Kirim feedback ke client (progress)
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)

            # Simulasi proses yang memakan waktu
            import asyncio
            await asyncio.sleep(0.5)

        # Goal selesai — kirim result
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence

        self.get_logger().info(f'Selesai! Result: {result.sequence}')
        return result


def main():
    rclpy.init()
    node = ActionServerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nAction server dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
