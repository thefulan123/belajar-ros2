#!/usr/bin/env python3
# ============================================================
# service_client.py — Service Client ROS2
#
# Node ini memanggil service /add_two_ints.
# Mengirim dua angka, lalu menunggu response (jumlahnya).
#
# Cara jalankan:
#   (Pastikan service_server.py sudah jalan)
#   python3 service_client.py
# ============================================================

import rclpy  # (1) Library utama ROS2 Python. Wajib untuk semua node.
from rclpy.node import Node  # (2) Kelas dasar Node untuk membuat node ROS2.
from example_interfaces.srv import AddTwoInts  # (3) Tipe service AddTwoInts — sama dengan server.

# (4) sys — library Python standar, digunakan untuk menghentikan program.
import sys


class ServiceClientNode(Node):
    # (5) Semua node ROS2 HARUS mewarisi class Node.
    """
    Sebuah service client node.
    
    Tugasnya:
    - Memanggil service '/add_two_ints'
    - Mengirim request: a=5, b=3
    - Menerima response: sum=8
    """

    def __init__(self):
        # (6) Panggil constructor parent dengan nama node UNIK.
        super().__init__('service_client_node')

        # (7) MEMBUAT SERVICE CLIENT — untuk memanggil service server.
        # Sintaks ROS2: self.create_client(TipeService, 'nama_service')
        # Parameter:
        #   1. Tipe service: AddTwoInts — harus SAMA dengan server
        #   2. Nama service: 'add_two_ints' — harus SAMA dengan server
        # Client hanya bisa MEMANGGIL, bukan menyediakan service.
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        # (8) MENUNGGU SERVICE TERSEDIA — WAJIB sebelum memanggil.
        # wait_for_service() mengembalikan True jika server sudah siap.
        # timeout_sec=1.0: cek setiap 1 detik.
        # Jika server belum jalan, client akan menunggu di sini.
        while not self.client.wait_for_service(timeout_sec=1.0):
            # (9) Peringatan selama menunggu server.
            self.get_logger().warn(
                'Service /add_two_ints belum tersedia, menunggu...'
            )

        # (10) MEMBUAT REQUEST — objek request sesuai tipe AddTwoInts.
        # AddTwoInts.Request() menghasilkan objek dengan field: a, b.
        request = AddTwoInts.Request()
        # (11) Isi field request: a=5, b=3.
        request.a = 5
        request.b = 3

        # (12) Log request yang akan dikirim.
        self.get_logger().info(
            f'Mengirim request: {request.a} + {request.b}'
        )

        # (13) MEMANGGIL SERVICE SECARA ASYNCHRONOUS.
        # Sintaks: self.client.call_async(request)
        # call_async() TIDAK memblokir program — langsung kembali.
        # Hasil panggilan disimpan di 'future' (Future object).
        # future.done() → True jika response sudah diterima.
        # future.result() → mengambil response.
        self.future = self.client.call_async(request)

        # (14) Timer periodik untuk mengecek response.
        # Setiap 0.1 detik, panggil self.check_response().
        self.timer = self.create_timer(0.1, self.check_response)

    def check_response(self):
        # (15) CALLBACK TIMER — mengecek apakah response sudah datang.
        """
        Mengecek apakah response dari service sudah diterima.
        Dipanggil setiap 0.1 detik oleh timer.
        """
        # (16) Cek apakah future sudah selesai (response diterima).
        if self.future.done():
            try:
                # (17) Ambil response dari service server.
                # future.result() mengembalikan objek Response.
                # response.sum berisi hasil penjumlahan.
                response = self.future.result()
                self.get_logger().info(
                    f'Response: {response.sum}'
                )
            except Exception as e:
                # (18) Tangani error jika panggilan gagal.
                self.get_logger().error(
                    f'Panggilan service gagal: {e}'
                )
            finally:
                # (19) Setelah selesai, hentikan node dan program.
                rclpy.shutdown()
                sys.exit(0)


def main():
    # (20) rclpy.init() — inisialisasi ROS2 (WAJIB).
    rclpy.init()
    # (21) Membuat instance node ServiceClientNode.
    node = ServiceClientNode()
    
    try:
        # (22) rclpy.spin(node) — loop utama, jalankan timer & callback.
        rclpy.spin(node)
    except KeyboardInterrupt:
        # (23) Tangani Ctrl+C.
        print("\nService client dihentikan.")
    finally:
        # (24) Bersihkan node dan shutdown ROS2.
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    # (25) Entry point.
    main()
