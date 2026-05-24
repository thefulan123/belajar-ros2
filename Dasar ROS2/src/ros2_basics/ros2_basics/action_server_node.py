import rclpy  # (1) Library utama ROS2 Python.
from rclpy.node import Node  # (2) Kelas dasar Node.
from rclpy.action import ActionServer  # (3) Class untuk membuat Action Server.
from example_interfaces.action import Fibonacci  # (4) Tipe action Fibonacci.
import asyncio  # (5) Library async Python — untuk await/async.


class ActionServerNode(Node):
    # (6) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        # (7) Panggil constructor parent dengan nama node UNIK.
        super().__init__('action_server_node')
        # (8) MEMBUAT ACTION SERVER — ActionServer(self, Tipe, 'nama', callback).
        self.action_server = ActionServer(
            self, Fibonacci, 'fibonacci', self.execute_callback
        )
        # (9) Log server siap.
        self.get_logger().info('Action server /fibonacci siap!')

    async def execute_callback(self, goal_handle):
        # (10) CALLBACK EKSEKUSI — fungsi ASYNC (pakai async/await).
        # goal_handle: objek kontrol goal (accepted, feedback, canceled, succeed).
        order = goal_handle.request.order  # (11) Ambil goal dari client.
        self.get_logger().info(f'Goal: Fibonacci ke-{order}')

        # (12) Buat feedback — dikirim berkala ke client.
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]  # (13) Dua angka Fibonacci pertama.

        # (14) Loop hitung deret Fibonacci.
        for i in range(1, order):
            if goal_handle.is_cancel_requested:  # (15) Cek cancel dari client.
                goal_handle.canceled()  # (16) Tandai sebagai dibatalkan.
                return Fibonacci.Result()  # (17) Kembalikan result kosong.

            fib_n = feedback_msg.sequence[i] + feedback_msg.sequence[i - 1]
            feedback_msg.sequence.append(fib_n)
            goal_handle.publish_feedback(feedback_msg)  # (18) Kirim feedback.
            await asyncio.sleep(0.5)  # (19) Simulasi proses (non-blocking).

        # (20) Goal selesai — tandai succeed.
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence  # (21) Isi result.
        self.get_logger().info(f'Selesai: {result.sequence}')
        return result  # (22) Kembalikan result ke client.


def main():
    rclpy.init()
    node = ActionServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
