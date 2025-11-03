#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')
        self.counter = 0
        self.get_logger().info('Initializing MyRobotNode')
        self.get_logger().info("Running MyRobotNode")
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info(f"Hello {self.counter}")
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)

    my_robot_node = MyRobotNode()
    rclpy.spin(my_robot_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()