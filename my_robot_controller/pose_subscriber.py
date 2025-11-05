#!usr/bin/env/python3

import rclpy

from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        self.pose_subscriber = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10)

    def pose_callback(self, message: Pose):
        self.get_logger().info(f"x: {message.x}, y: {message.y}")

def main(args=None):
    rclpy.init(args=args)
    node = PoseSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()