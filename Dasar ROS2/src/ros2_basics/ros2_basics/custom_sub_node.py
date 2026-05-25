#!/usr/bin/env python3
import json  # (1) Library JSON — parsing string ke Python dict.
import rclpy  # (2) Library utama ROS2 Python.
from rclpy.node import Node  # (3) Kelas dasar Node.
from std_msgs.msg import String  # (4) Tipe pesan String.
from ros2_basics.custom_msg_types import SensorData  # (5) Custom message SensorData.


class CustomSubNode(Node):
    # (6) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        super().__init__('custom_sub_node')
        # (7) MEMBUAT SUBSCRIPTION — self.create_subscription(Tipe, 'topic', callback, qos).
        self.subscription = self.create_subscription(
            String, 'sensor_data', self.listener_callback, 10
        )
        self.get_logger().info('Custom sub node siap!')

    def listener_callback(self, msg):
        # (8) CALLBACK SUBSCRIPTION — dipanggil SETIAP ada data di /sensor_data.
        data = json.loads(msg.data)  # (9) Parse JSON → dict.
        sensor = SensorData.from_dict(data)  # (10) Dict → objek SensorData.
        self.get_logger().info(f'Menerima: {sensor}')
        # (11) Contoh deteksi suhu tinggi.
        if sensor.temperature > 30.0:
            self.get_logger().warn(f'Suhu tinggi! {sensor.temperature}°C')


def main():
    rclpy.init()
    node = CustomSubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
