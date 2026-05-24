import rclpy  # (1) Library utama ROS2 Python.
from rclpy.node import Node  # (2) Kelas dasar Node.


class ParamNode(Node):
    # (3) Semua node ROS2 HARUS mewarisi class Node.
    """
    Node dengan parameter yang bisa diatur dari luar.
    Parameter bisa diubah via launch file, CLI, atau file YAML.
    """

    def __init__(self):
        # (4) Panggil constructor parent dengan nama node UNIK.
        super().__init__('param_node')

        # (5) DEKLARASI PARAMETER — self.declare_parameter('nama', nilai_default).
        self.declare_parameter('publish_rate', 1.0)   # (6) Interval timer (float, detik).
        self.declare_parameter('message', 'Halo dari param_node!')  # (7) Pesan (string).
        self.declare_parameter('verbose', True)        # (8) Mode verbose (bool).
        self.declare_parameter('max_count', 10)        # (9) Maks pesan (int).

        # (10) BACA PARAMETER — self.get_parameter('nama').value.
        rate = self.get_parameter('publish_rate').value
        self._message = self.get_parameter('message').value
        self._verbose = self.get_parameter('verbose').value
        self._max_count = self.get_parameter('max_count').value
        self._count = 0  # (11) Counter internal.

        # (12) Timer dengan interval dari parameter.
        self.timer = self.create_timer(rate, self.timer_callback)

        if self._verbose:
            self.get_logger().info(f'Rate: {rate}s, Max: {self._max_count}')

    def timer_callback(self):
        # (13) CALLBACK TIMER — dipanggil sesuai publish_rate.
        self._count += 1
        if self._verbose:
            self.get_logger().info(
                f'[{self._count}/{self._max_count}] {self._message}'
            )
        # (14) Berhenti setelah mencapai max_count.
        if self._count >= self._max_count:
            self.get_logger().info('Selesai.')
            self.timer.cancel()  # (15) Hentikan timer.
            rclpy.shutdown()     # (16) Hentikan ROS2.


def main():
    rclpy.init()
    node = ParamNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
