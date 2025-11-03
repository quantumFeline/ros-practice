#!usr/bin/env/python3

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node

class DrawCircleNode(Node):

    def __init__(self):
        super().__init__('draw_circle')
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info("Draw circle node started")
        self.timer = self.create_timer(0.5, self.send_velocity)

    def send_velocity(self):
        message = Twist()
        message.linear.x = 2.0
        # message.linear.y = 0.0
        # message.linear.z = 0.0 doesn't exist in 2d
        # message.angular.x = 0.0 doesn't exist in 2d
        # message.angular.y = 0.0 doesn't exist in 2d
        message.angular.z = 1.0
        self.cmd_vel_pub.publish(message)

def main(args=None):
    rclpy.init(args=args)
    node = DrawCircleNode()
    rclpy.spin(node)
    rclpy.shutdown()