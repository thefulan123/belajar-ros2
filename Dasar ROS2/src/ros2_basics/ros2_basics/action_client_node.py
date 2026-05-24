import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci
import sys


class ActionClientNode(Node):
    def __init__(self):
        super().__init__('action_client_node')
        self.client = ActionClient(self, Fibonacci, 'fibonacci')

        self.get_logger().info('Menunggu action server...')
        self.client.wait_for_server()
        self.get_logger().info('Action server ditemukan!')

        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10
        self.get_logger().info(f'Mengirim goal: Fibonacci ke-{goal_msg.order}')

        self.send_goal_future = self.client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback
        )
        self.timer = self.create_timer(0.1, self.check_goal_accepted)

    def check_goal_accepted(self):
        if self.send_goal_future.done():
            goal_handle = self.send_goal_future.result()
            if goal_handle.accepted:
                self.get_logger().info('Goal diterima!')
                self.result_future = goal_handle.get_result_async()
                self.result_future.add_done_callback(self.result_callback)
            else:
                self.get_logger().error('Goal ditolak!')
                rclpy.shutdown()
                sys.exit(1)
            self.timer.cancel()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback: {feedback.sequence}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()
        sys.exit(0)


def main():
    rclpy.init()
    node = ActionClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
