#!/usr/bin/env python3
import sys
import time

from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
import numpy as np

"""
This script makes the end-effector perform pick, pour, and place tasks.
Note that this script may not work for every arm as it was designed for the wx250.
Make sure to adjust commanded joint positions and poses as necessary.

To get started, open a terminal and type:

    ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=wx250

Then change to this directory and type:

    python3 bartender.py
"""

def main():
    bot = InterbotixManipulatorXS(
        robot_model='wx250s',
        group_name='arm',
        gripper_name='gripper',
    )

    robot_startup()

    if (bot.arm.group_info.num_joints < 5):
        bot.get_node().logfatal(
            'This demo requires the robot to have at least 5 joints!'
        )
        robot_shutdown()
        sys.exit()

    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.set_single_joint_position(joint_name='waist', position=np.pi/2.0)
    bot.gripper.release()
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
    bot.gripper.grasp()
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
    bot.arm.set_single_joint_position(joint_name='waist', position=-np.pi/2.0)
    bot.arm.set_ee_cartesian_trajectory(pitch=1.5)
    bot.arm.set_ee_cartesian_trajectory(pitch=-1.5)
    bot.arm.set_single_joint_position(joint_name='waist', position=np.pi/2.0)
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.16)
    bot.gripper.release()
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
    bot.arm.go_to_home_pose()
    bot.arm.go_to_sleep_pose()

    # Adding a short delay to ensure all actions complete before shutdown
    time.sleep(1)
    robot_shutdown()

if __name__ == '__main__':
    main()

