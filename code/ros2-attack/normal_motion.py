#!/usr/bin/env python3
import sys
import time

from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np

"""
This script makes the end-effector perform pick, pour, and place tasks continuously between two points.
To get started, open a terminal and type:

    ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=px150 use_sim:=true

Then change to this directory and type:

    python3 bartender.py
"""

def main():
    # Initialize the InterbotixManipulatorXS object
    bot = InterbotixManipulatorXS(
        robot_model='px150',
        group_name='arm',
        gripper_name='gripper',
    )

    if bot.arm.group_info.num_joints < 5:
        print("This demo requires the robot to have at least 5 joints!")
        sys.exit()

    # Initial position
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_single_joint_position(joint_name='waist', position=np.pi / 2.0)
    bot.gripper.release()
    
    # Continuous loop between two points
    try:
        while True:
            # Move to the first point
            bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
            bot.gripper.grasp()
            time.sleep(1)  # Hold for demonstration purposes

            # Move to the second point
            bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
            bot.gripper.release()
            time.sleep(1)  # Hold for demonstration purposes

            # Rotate the waist to add variety to the movement
            bot.arm.set_single_joint_position(joint_name='waist', position=-np.pi / 2.0)
            time.sleep(1)

            bot.arm.set_single_joint_position(joint_name='waist', position=np.pi / 2.0)
            time.sleep(1)

    except KeyboardInterrupt:
        # This allows the user to stop the loop by pressing Ctrl+C
        print("Stopping the continuous motion.")
        bot.arm.go_to_home_pose()

if __name__ == '__main__':
    main()
