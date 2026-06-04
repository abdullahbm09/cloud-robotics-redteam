#!/usr/bin/env python3
import sys
from rclpy.node import Node
from std_msgs.msg import String
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import rclpy
import numpy as np


class DefectCorrectionNode(Node):
    def __init__(self, bot):
        # Initialize the ROS2 Node
        super().__init__('defect_correction_node')
        self.bot = bot  # Use the robot instance passed during initialization

        # Subscribe to the 'defect_type' topic
        self.subscription = self.create_subscription(
            String,
            'defect_type',
            self.defect_callback,
            10
        )
        self.get_logger().info("Defect Correction Node has been started.")

    def defect_callback(self, msg):
        defect_type = msg.data
        self.get_logger().info(f"Received defect type: {defect_type}")

        if defect_type == 'D1':
            self.perform_motion_p1()
        elif defect_type == 'D2':
            self.perform_motion_p2()
        elif defect_type == 'None':
            self.get_logger().info("No defect detected. Robot remains idle.")

    def perform_motion_p1(self):
        self.get_logger().info("Performing motion P1 for defect type D1.")
        # Initial position
        self.bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        self.bot.arm.set_single_joint_position(joint_name='waist', position=0.0)

        # P1 Motion: Pick up from the same starting point, slight variation
        self.bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.15)  # Move to P1
        self.bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.15)  # Return to start
        self.get_logger().info("Motion P1 completed.")

    def perform_motion_p2(self):
        self.get_logger().info("Performing motion P2 for defect type D2.")
        # Initial position
        self.bot.arm.set_ee_pose_components(x=0.3, z=0.2)
        self.bot.arm.set_single_joint_position(joint_name='waist', position=0.0)

        # P2 Motion: Pick up from the same starting point, slight variation
        self.bot.arm.set_ee_cartesian_trajectory(x=0.2, z=-0.2)  # Move to P2
        self.bot.arm.set_ee_cartesian_trajectory(x=-0.2, z=0.2)  # Return to start
        self.get_logger().info("Motion P2 completed.")


def main():
    # Initialize the InterbotixManipulatorXS object, which also initializes rclpy
    bot = InterbotixManipulatorXS(
        robot_model='px150',
        group_name='arm',
        gripper_name='gripper',
    )

    # Pass the bot to the DefectCorrectionNode
    rclpy.init()  # Ensure rclpy is initialized once
    defect_correction_node = DefectCorrectionNode(bot)

    try:
        rclpy.spin(defect_correction_node)
    except KeyboardInterrupt:
        pass
    finally:
        defect_correction_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
