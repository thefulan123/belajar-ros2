import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceServerNode(Node):
    def __init__(self):
        super().__init__('service_server_node')
        self.srv = self.create_service(
            AddTwoInts, 'add_two_ints', self.add_callback
        )
        self.get_logger().info('Service server /add_two_ints siap!')

    def add_callback(self, request, response):
        self.get_logger().info(f'Menerima: {request.a} + {request.b}')
        response.sum = request.a + request.b
        self.get_logger().info(f'Mengirim: {response.sum}')
        return response


def main():
    rclpy.init()
    node = ServiceServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
