import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ros2_basics.custom_msg_types import SensorData


class CustomSubNode(Node):
    def __init__(self):
        super().__init__('custom_sub_node')
        self.subscription = self.create_subscription(
            String, 'sensor_data', self.listener_callback, 10
        )
        self.get_logger().info('Custom sub node siap!')

    def listener_callback(self, msg):
        data = json.loads(msg.data)
        sensor = SensorData.from_dict(data)
        self.get_logger().info(f'Menerima: {sensor}')
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
