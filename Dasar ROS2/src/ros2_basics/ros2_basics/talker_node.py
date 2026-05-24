import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TalkerNode(Node):
    """
    Publisher node — mengirim pesan ke topic /chatter setiap 1 detik.
    Sama seperti explore/02-pub-sub/talker.py, tapi dibungkus sebagai package.
    """

    def __init__(self):
        super().__init__('talker_node')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        self.get_logger().info('Talker node siap!')

    def timer_callback(self):
        msg = String()
        msg.data = f'Halo ROS2! Pesan ke-{self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Mengirim: "{msg.data}"')
        self.count += 1


def main():
    rclpy.init()
    node = TalkerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
