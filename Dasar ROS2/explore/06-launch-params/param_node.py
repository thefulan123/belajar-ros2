#!/usr/bin/env python3
# ============================================================
# param_node.py — Node dengan Parameter
#
# Node ini membaca parameter yang bisa diubah
# tanpa perlu edit kode.
#
# Parameter bisa di-set via:
# - Launch file (.launch.py)
# - Command line: ros2 param set
# - YAML config file
#
# Cara jalankan:
#   python3 param_node.py
#   (menggunakan default parameter)
#
#   Atau pakai launch file:
#   ros2 launch launch/param_demo.launch.py
# ============================================================

import rclpy
from rclpy.node import Node


class ParamNode(Node):
    """
    Sebuah node yang menggunakan parameter.
    
    Parameter adalah pengaturan yang bisa diubah
    tanpa mengubah kode.
    """

    def __init__(self):
        super().__init__('param_node')

        # Deklarasikan parameter dengan nilai default
        # Parameter bisa diubah dari luar (launch file / CLI)
        self.declare_parameter('node_name', 'param_node')
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('message', 'Halo dari param_node!')
        self.declare_parameter('verbose', True)
        self.declare_parameter('max_count', 10)

        # Baca nilai parameter
        node_name = self.get_parameter('node_name').value
        publish_rate = self.get_parameter('publish_rate').value
        message = self.get_parameter('message').value
        verbose = self.get_parameter('verbose').value
        max_count = self.get_parameter('max_count').value

        # Ganti nama node sesuai parameter
        self._node_name = node_name
        self._message = message
        self._verbose = verbose
        self._max_count = max_count
        self._count = 0

        # Timer dengan rate dari parameter
        self.timer = self.create_timer(publish_rate, self.timer_callback)

        if self._verbose:
            self.get_logger().info(f'Node dimulai: {node_name}')
            self.get_logger().info(f'Publish rate: {publish_rate} detik')
            self.get_logger().info(f'Pesan: {message}')
            self.get_logger().info(f'Maks count: {max_count}')

    def timer_callback(self):
        self._count += 1

        if self._verbose:
            self.get_logger().info(
                f'[{self._count}/{self._max_count}] {self._message}'
            )

        # Berhenti setelah mencapai max_count
        if self._count >= self._max_count:
            self.get_logger().info('Mencapai max count. Berhenti.')
            self.timer.cancel()
            rclpy.shutdown()


def main():
    rclpy.init()
    node = ParamNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nNode dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
