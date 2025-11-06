#!usr/bin/env/python3

import rclpy

from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
from functools import partial

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.get_logger().info('Initializing turtle controller...')

        self.pose_subscriber = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.prev_x = 0
        # self.timer = self.create_timer(0.5, self.send_velocity)

    def pose_callback(self, pose: Pose):
        self.get_logger().info(f"x: {pose.x}, y: {pose.y}")
        cmd_vel_msg = Twist()

        if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
            cmd_vel_msg.linear.x = 1.0
            cmd_vel_msg.angular.z = 2.0
        # cmd_vel_msg.linear.x = pose.x
        # cmd_vel_msg.angular.z = pose.angular_velocity
        else:
            cmd_vel_msg.linear.x = 2.0
            cmd_vel_msg.angular.z = 0.2
        self.send_velocity(cmd_vel_msg)

        if pose.x > 5.5 >= self.prev_x:
            self.get_logger().info("Set to red")
            self.call_set_pen_service(255, 0, 0, 3, 0)
        if pose.x < 5.5 <= self.prev_x:
            self.get_logger().info("Set to green")
            self.call_set_pen_service(0, 255, 0, 3, 0)

        self.prev_x = pose.x

    def send_velocity(self, cmd_vel_msg: Twist):
        self.cmd_vel_pub.publish(cmd_vel_msg)

    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, "/turtle1/set_pen")
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Service not available, waiting again...")

        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        try:
            response = future.result()
        except Exception as ex:
            self.get_logger().warn("Service call failed %r" % (ex,))

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()