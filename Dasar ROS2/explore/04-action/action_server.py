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

# ═══════════════════════════════════════════════════════════════
# PENJELASAN DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════
#
# Berikut adalah data structure / objek ROS2 yang dipakai di file ini:
#
# 1. rclpy
#    - Library utama ROS2 Python. Wajib untuk semua program.
#    - rclpy.init() = inisialisasi, rclpy.spin() = loop utama.
#
# 2. Node
#    - Kelas dasar node ROS2. Setiap node punya nama unik.
#    - Bisa memiliki action server, publisher, subscriber, dll.
#
# 3. ActionServer (dibuat dengan create_action_server())
#    - Menyediakan action yang bisa dipanggil client.
#    - Action = Service + Feedback + Cancel.
#    - Cocok untuk tugas lama: navigasi, gerakan robot, dll.
#
# 4. example_interfaces.action.Fibonacci
#    - Tipe action untuk deret Fibonacci.
#    - Struktur 3 bagian:
#      Goal:     int32 order
#      Feedback: int32[] sequence
#      Result:   int32[] sequence
#
# 5. Execute Callback (async execute_callback)
#    - Fungsi async untuk eksekusi goal di background.
#    - async/await = tidak memblokir node lain.
#    - Bisa mendeteksi cancel request dari client.
#
# 6. GoalHandle
#    - Objek yang mengontrol status goal.
#    - Method: is_canceling(), publish_feedback(), succeed().
#
# 7. Feedback
#    - Dikirim selama eksekusi (fitur eksklusif Action).
#    - Memberi tahu client progres saat ini.
#
# ═══════════════════════════════════════════════════════════════
# ============================================================

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.
from rclpy.action import ActionServer  # (3) Class untuk membuat Action Server ROS2.

# (4) Fibonacci — tipe action bawaan ROS2 dari package example_interfaces.
# Action memiliki 3 komponen:
#   Goal: int32 order          — input dari client (urutan ke berapa)
#   Feedback: int32[] sequence — progress selama proses (dikirim berkala)
#   Result: int32[] sequence   — output akhir (deret lengkap)
from example_interfaces.action import Fibonacci


class ActionServerNode(Node):
    # (5) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah action server node.
    
    Tugasnya:
    - Menerima goal dari client
    - Memproses (dengan feedback berkala)
    - Mengembalikan result
    """

    def __init__(self):
        # (6) Panggil constructor parent dengan nama node UNIK.
        super().__init__('action_server_node')

        # (7) MEMBUAT ACTION SERVER — menyediakan layanan action.
        # Sintaks ROS2: ActionServer(self, TipeAction, 'nama_action', callback)
        # Parameter:
        #   1. Node reference: self (node tempat server berada)
        #   2. Tipe action: Fibonacci — menentukan format goal/feedback/result
        #   3. Nama action: 'fibonacci' — client menggunakan nama INI
        #   4. Execute callback: fungsi async yang memproses goal
        # Action berbeda dengan Service:
        #   Service: request-response langsung, TIDAK ada feedback
        #   Action: menerima goal, memberi feedback, mengembalikan result
        self.action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

        # (8) Log bahwa server sudah siap menerima goal.
        self.get_logger().info('Action server /fibonacci siap!')

    async def execute_callback(self, goal_handle):
        # (9) CALLBACK EKSEKUSI — fungsi ASYNC (harus pakai async/await).
        # Dipanggil OTOMATIS saat client mengirim goal.
        # goal_handle: objek untuk mengontrol eksekusi goal.
        #   - goal_handle.request → goal dari client
        #   - goal_handle.publish_feedback() → kirim progress
        #   - goal_handle.is_cancel_requested → cek apakah client batalkan
        #   - goal_handle.succeed() → tandai goal selesai
        #   - goal_handle.canceled() → tandai goal dibatalkan
        """
        Fungsi ini dipanggil saat client mengirim goal.
        
        Parameter:
        - goal_handle: objek yang mengontrol eksekusi goal
        
        Selama proses, kita bisa:
        - Mengirim feedback ke client
        - Mengecek apakah client meminta cancel
        - Mengembalikan result
        """

        # (10) Ambil goal dari client.
        # goal_handle.request.order — field int32 dari Fibonacci.Goal.
        order = goal_handle.request.order
        self.get_logger().info(f'Menerima goal: Fibonacci ke-{order}')

        # (11) Buat objek FEEDBACK untuk mengirim progress ke client.
        # Fibonacci.Feedback memiliki field: sequence (int32[]).
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]  # (12) Dua angka pertama Fibonacci.

        # (13) Loop untuk menghitung deret Fibonacci.
        for i in range(1, order):
            # (14) CEK CANCEL — apakah client membatalkan goal?
            # Action bisa dibatalkan, Service TIDAK bisa.
            if goal_handle.is_cancel_requested:
                self.get_logger().info('Goal dibatalkan oleh client')
                goal_handle.canceled()  # (15) Tandai sebagai dibatalkan.
                return Fibonacci.Result()  # (16) Kembalikan result kosong.

            # (17) Hitung nilai Fibonacci berikutnya.
            fib_n = feedback_msg.sequence[i] + feedback_msg.sequence[i - 1]
            feedback_msg.sequence.append(fib_n)

            # (18) KIRIM FEEDBACK ke client — progress terkini.
            # Ini fitur yang TIDAK dimiliki Service.
            self.get_logger().info(f'Feedback: {feedback_msg.sequence}')
            goal_handle.publish_feedback(feedback_msg)

            # (19) Simulasi proses yang memakan waktu.
            # await asyncio.sleep() — jeda tanpa memblokir program.
            import asyncio
            await asyncio.sleep(0.5)

        # (20) Goal selesai — tandai sebagai berhasil.
        goal_handle.succeed()
        # (21) Buat objek RESULT dengan deret Fibonacci lengkap.
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence

        # (22) Log result akhir.
        self.get_logger().info(f'Selesai! Result: {result.sequence}')
        # (23) Kembalikan result ke client.
        return result


def main():
    # (24) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    # (25) Membuat instance node ActionServerNode.
    node = ActionServerNode()
    
    try:
        # (26) rclpy.spin(node) — loop utama, tunggu goal dari client.
        rclpy.spin(node)
    except KeyboardInterrupt:
        # (27) Tangani Ctrl+C.
        print("\nAction server dihentikan.")
    finally:
        # (28) Bersihkan node dan shutdown ROS2.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    # (29) Entry point.
    main()
