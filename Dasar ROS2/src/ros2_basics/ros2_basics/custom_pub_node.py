#!/usr/bin/env python3
import json  # (1) Library JSON — serialisasi data ke string.
import random  # (2) Library random — untuk data sensor acak.
import rclpy  # (3) Library utama ROS2 Python.
from rclpy.node import Node  # (4) Kelas dasar Node.
from std_msgs.msg import String  # (5) Tipe pesan String (kirim JSON).
from ros2_basics.custom_msg_types import SensorData  # (6) Custom message SensorData.


class CustomPubNode(Node):
    # (7) Semua node ROS2 HARUS mewarisi class Node.
    def __init__(self):
        super().__init__('custom_pub_node')
        # (8) Publisher ke topic /sensor_data (tipe String — JSON).
        self.publisher = self.create_publisher(String, 'sensor_data', 10)
        # (9) Timer setiap 1 detik.
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Custom pub node siap!')

    def timer_callback(self):
        # (10) CALLBACK TIMER — buat data sensor acak.
        sensor = SensorData(
            temperature=round(random.uniform(20.0, 35.0), 1),
            humidity=round(random.uniform(40.0, 80.0), 1),
            pressure=round(random.uniform(1000.0, 1020.0), 1)
        )
        # (11) Serialisasi ke JSON, publish ke topic.
        msg = String()
        msg.data = json.dumps(sensor.to_dict())
        self.publisher.publish(msg)  # (12) PUBLISH — kirim data.
        self.get_logger().info(f'Mengirim: {sensor}')


def main():
    rclpy.init()
    node = CustomPubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
