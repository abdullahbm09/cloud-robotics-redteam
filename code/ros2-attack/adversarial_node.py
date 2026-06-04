#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from interbotix_xs_msgs.msg import JointSingleCommand
import time

class AdversarialNode(Node):
    def __init__(self):
        super().__init__('adversarial_node')
        # Publisher to the joint_single command topic
        self.publisher_ = self.create_publisher(JointSingleCommand, '/px150/commands/joint_single', 10)
        
        # Adversarial command parameters
        self.joint_name = 'waist'  # Specify the joint to target
        self.target_position = 1.0  # Set to a specific angle (radians)
        self.timer_period = 0.05  # Send command every second to maintain position
        
        # Timer to publish at regular intervals
        self.timer = self.create_timer(self.timer_period, self.hold_position)

    def hold_position(self):
        # Create a JointSingleCommand message
        msg = JointSingleCommand()
        msg.name = self.joint_name
        msg.cmd = self.target_position  # Hold the joint at the target position
        
        # Publish the command
        self.publisher_.publish(msg)
        self.get_logger().info(f'Holding joint {self.joint_name} at position {self.target_position}')

def main(args=None):
    rclpy.init(args=args)
    adversarial_node = AdversarialNode()
    rclpy.spin(adversarial_node)

    # Shutdown once done
    adversarial_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
