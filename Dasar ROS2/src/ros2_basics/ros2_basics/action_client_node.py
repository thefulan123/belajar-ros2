import rclpy  # (1) Library utama ROS2 Python.
from rclpy.node import Node  # (2) Kelas dasar Node.
from rclpy.action import ActionClient  # (3) Class untuk membuat Action Client.
from example_interfaces.action import Fibonacci  # (4) Tipe action Fibonacci.
import sys  # (5) Library Python standar.


class ActionClientNode(Node):
    # (6) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        # (7) Panggil constructor parent dengan nama node UNIK.
        super().__init__('action_client_node')
        # (8) MEMBUAT ACTION CLIENT — ActionClient(self, Tipe, 'nama_action').
        self.client = ActionClient(self, Fibonacci, 'fibonacci')

        # (9) Log menunggu server.
        self.get_logger().info('Menunggu action server...')
        self.client.wait_for_server()  # (10) Tunggu server tersedia.
        self.get_logger().info('Action server ditemukan!')

        # (11) Buat goal — Fibonacci.Goal() dengan field order.
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10  # (12) Minta deret Fibonacci ke-10.
        self.get_logger().info(f'Mengirim goal: Fibonacci ke-{goal_msg.order}')

        # (13) Kirim goal secara async dengan callback feedback.
        self.send_goal_future = self.client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        # (14) Timer untuk cek apakah goal diterima.
        self.timer = self.create_timer(0.1, self.check_goal_accepted)

    def check_goal_accepted(self):
        # (15) CALLBACK TIMER — cek apakah server sudah merespon goal.
        if self.send_goal_future.done():
            goal_handle = self.send_goal_future.result()
            if goal_handle.accepted:  # (16) Goal diterima?
                self.get_logger().info('Goal diterima!')
                # (17) Minta result secara async.
                self.result_future = goal_handle.get_result_async()
                self.result_future.add_done_callback(self.result_callback)
            else:
                self.get_logger().error('Goal ditolak!')
                rclpy.shutdown()
                sys.exit(1)
            self.timer.cancel()  # (18) Hentikan timer — tidak perlu cek lagi.

    def feedback_callback(self, feedback_msg):
        # (19) CALLBACK FEEDBACK — dipanggil SETIAP ada feedback dari server.
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.sequence}')

    def result_callback(self, future):
        # (20) CALLBACK RESULT — dipanggil saat action selesai.
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()  # (21) Hentikan ROS2.
        sys.exit(0)  # (22) Keluar program.


def main():
    rclpy.init()
    node = ActionClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
