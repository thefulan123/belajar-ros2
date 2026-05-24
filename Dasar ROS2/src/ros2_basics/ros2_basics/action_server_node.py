import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci
import asyncio


class ActionServerNode(Node):
    def __init__(self):
        super().__init__('action_server_node')
        self.action_server = ActionServer(
            self, Fibonacci, 'fibonacci', self.execute_callback
        )
        self.get_logger().info('Action server /fibonacci siap!')

    async def execute_callback(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(f'Goal: Fibonacci ke-{order}')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return Fibonacci.Result()

            fib_n = feedback_msg.sequence[i] + feedback_msg.sequence[i - 1]
            feedback_msg.sequence.append(fib_n)
            goal_handle.publish_feedback(feedback_msg)
            await asyncio.sleep(0.5)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Selesai: {result.sequence}')
        return result


def main():
    rclpy.init()
    node = ActionServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
