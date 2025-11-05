#!usr/bin/env/python3
import time

import rclpy

from rclpy.node import Node
import pyrealsense2 as rs
import numpy as np
import cv2
from builtin_interfaces.msg import Time
from sensor_msgs.msg import Image
from std_msgs.msg import Header

class CameraData:
    def __init__(self, color_frame, depth_frame):
        self.color_frame = color_frame
        self.depth_frame = depth_frame

def setup_pipeline():
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)

    return pipeline, config

def get_colormap(depth_frame):
    return cv2.applyColorMap(
        cv2.convertScaleAbs(depth_frame, alpha=0.03),
        cv2.COLORMAP_JET
    )

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.get_logger().info('Initializing camera subscriber...')
        self.pipeline, self.pipeline_config = setup_pipeline()

        self.camera_stream_pub = self.create_publisher(Image, '/camera/raw_stream', 10)
        self.timer = self.create_timer(3, self.send_camera_frame)
        self.frame_counter = 0

    def __del__(self):
        self.pipeline.stop()

    def send_camera_frame(self):
        camera_data = self.grab_frame()
        self.get_logger().info('Sending frame...')
        self.camera_stream_pub.publish(camera_data)

    def grab_frame(self) -> Image:
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        self.frame_counter += 1

        assert depth_frame and color_frame, "No camera data received"

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        width, height = depth_image.shape[1], depth_image.shape[0]

        return Image(header=Header(
                            stamp=self.get_clock().now().to_msg(),
                            frame_id=str(self.frame_counter)),
                     data=depth_image.tobytes(),
                     height=height,
                     width=width,
                     encoding="16UC1",
                     is_bigendian=False,
                     step=width * 2)
        # return CameraData(color_image, get_colormap(depth_image))

def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()
