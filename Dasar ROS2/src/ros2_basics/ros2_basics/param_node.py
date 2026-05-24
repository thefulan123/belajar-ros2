import rclpy
from rclpy.node import Node


class ParamNode(Node):
    """
    Node dengan parameter yang bisa diatur dari luar.
    Parameter bisa diubah via launch file, CLI, atau file YAML.
    """

    def __init__(self):
        super().__init__('param_node')

        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('message', 'Halo dari param_node!')
        self.declare_parameter('verbose', True)
        self.declare_parameter('max_count', 10)

        rate = self.get_parameter('publish_rate').value
        self._message = self.get_parameter('message').value
        self._verbose = self.get_parameter('verbose').value
        self._max_count = self.get_parameter('max_count').value
        self._count = 0

        self.timer = self.create_timer(rate, self.timer_callback)

        if self._verbose:
            self.get_logger().info(f'Rate: {rate}s, Max: {self._max_count}')

    def timer_callback(self):
        self._count += 1
        if self._verbose:
            self.get_logger().info(
                f'[{self._count}/{self._max_count}] {self._message}'
            )
        if self._count >= self._max_count:
            self.get_logger().info('Selesai.')
            self.timer.cancel()
            rclpy.shutdown()


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
