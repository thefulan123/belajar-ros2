import json
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ros2_basics.custom_msg_types import SensorData


class CustomPubNode(Node):
    def __init__(self):
        super().__init__('custom_pub_node')
        self.publisher = self.create_publisher(String, 'sensor_data', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Custom pub node siap!')

    def timer_callback(self):
        sensor = SensorData(
            temperature=round(random.uniform(20.0, 35.0), 1),
            humidity=round(random.uniform(40.0, 80.0), 1),
            pressure=round(random.uniform(1000.0, 1020.0), 1)
        )
        msg = String()
        msg.data = json.dumps(sensor.to_dict())
        self.publisher.publish(msg)
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
