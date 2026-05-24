import rclpy  # (1) Library utama ROS2 Python.
from rclpy.node import Node  # (2) Kelas dasar Node.
from example_interfaces.srv import AddTwoInts  # (3) Tipe service AddTwoInts.
import sys  # (4) Library Python standar untuk sys.exit().


class ServiceClientNode(Node):
    # (5) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        # (6) Panggil constructor parent dengan nama node UNIK.
        super().__init__('service_client_node')
        # (7) MEMBUAT SERVICE CLIENT — self.create_client(Tipe, 'nama_service').
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        # (8) Tunggu server tersedia — WAJIB sebelum memanggil.
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Menunggu service /add_two_ints...')

        # (9) Buat request, isi field a=5, b=3.
        request = AddTwoInts.Request()
        request.a = 5
        request.b = 3
        self.get_logger().info(f'Mengirim: {request.a} + {request.b}')

        # (10) Panggil service secara async — self.client.call_async(request).
        self.future = self.client.call_async(request)
        # (11) Timer periodik untuk cek response.
        self.timer = self.create_timer(0.1, self.check_response)

    def check_response(self):
        # (12) CALLBACK TIMER — cek apakah response sudah diterima.
        if self.future.done():
            try:
                response = self.future.result()  # (13) Ambil response.
                self.get_logger().info(f'Response: {response.sum}')
            except Exception as e:
                self.get_logger().error(f'Gagal: {e}')
            finally:
                rclpy.shutdown()  # (14) Hentikan ROS2.
                sys.exit(0)  # (15) Keluar dari program.


def main():
    rclpy.init()
    node = ServiceClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
