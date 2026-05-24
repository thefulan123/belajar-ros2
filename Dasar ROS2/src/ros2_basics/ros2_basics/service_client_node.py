import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys


class ServiceClientNode(Node):
    def __init__(self):
        super().__init__('service_client_node')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Menunggu service /add_two_ints...')

        request = AddTwoInts.Request()
        request.a = 5
        request.b = 3
        self.get_logger().info(f'Mengirim: {request.a} + {request.b}')

        self.future = self.client.call_async(request)
        self.timer = self.create_timer(0.1, self.check_response)

    def check_response(self):
        if self.future.done():
            try:
                response = self.future.result()
                self.get_logger().info(f'Response: {response.sum}')
            except Exception as e:
                self.get_logger().error(f'Gagal: {e}')
            finally:
                rclpy.shutdown()
                sys.exit(0)


def main():
    rclpy.init()
    node = ServiceClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
