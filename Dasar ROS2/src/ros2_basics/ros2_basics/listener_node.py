import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ListenerNode(Node):
    """
    Subscriber node — menerima pesan dari topic /chatter.
    Sama seperti explore/02-pub-sub/listener.py, tapi dibungkus sebagai package.
    """

    def __init__(self):
        super().__init__('listener_node')
        self.subscription = self.create_subscription(
            String, 'chatter', self.listener_callback, 10
        )
        self.get_logger().info('Listener node siap!')

    def listener_callback(self, msg):
        self.get_logger().info(f'Menerima: "{msg.data}"')


def main():
    rclpy.init()
    node = ListenerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
