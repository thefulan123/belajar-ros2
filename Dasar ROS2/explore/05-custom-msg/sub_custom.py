#!/usr/bin/env python3
# ============================================================
# sub_custom.py — Subscriber dengan Custom Message
#
# Menerima data SensorData dari topic /sensor_data.
# Parse JSON string kembali ke objek SensorData.
# ============================================================

import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_custom_msg import SensorData


class CustomSubNode(Node):
    def __init__(self):
        super().__init__('custom_sub_node')
        self.subscription = self.create_subscription(
            String,
            'sensor_data',
            self.listener_callback,
            10
        )
        self.get_logger().info('Subscriber custom message siap!')

    def listener_callback(self, msg):
        # Parse JSON string ke Python dict
        data = json.loads(msg.data)

        # Convert dict ke SensorData
        sensor = SensorData.from_dict(data)

        self.get_logger().info(f'Menerima: {sensor}')

        # Contoh: deteksi suhu tinggi
        if sensor.temperature > 30.0:
            self.get_logger().warn(
                f'Suhu tinggi! {sensor.temperature}°C'
            )


def main():
    rclpy.init()
    node = CustomSubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nSubscriber dihentikan.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
