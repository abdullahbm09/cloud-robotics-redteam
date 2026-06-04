#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random
import time

class DefectDetectionNode(Node):
    def __init__(self):
        super().__init__('defect_detection_node')
        self.publisher_ = self.create_publisher(String, 'defect_type', 10)
        self.timer = self.create_timer(2.0, self.publish_defect_type)
        self.get_logger().info("Defect Detection Node has been started.")

    def publish_defect_type(self):
        # Randomly choose between D1, D2, and None (no defect)
        defect_type = random.choice(['D1', 'D2', 'None'])
        msg = String()
        msg.data = defect_type
        self.publisher_.publish(msg)
        if defect_type == 'None':
            self.get_logger().info("Published: No defect detected.")
        else:
            self.get_logger().info(f"Published defect type: {defect_type}")

def main(args=None):
    rclpy.init(args=args)
    defect_detection_node = DefectDetectionNode()
    try:
        rclpy.spin(defect_detection_node)
    except KeyboardInterrupt:
        pass
    finally:
        defect_detection_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
