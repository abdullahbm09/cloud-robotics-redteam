#!/usr/bin/env python3
import sys
import time
import random
from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS

def main():
    # Initialize the InterbotixManipulatorXS object
    bot = InterbotixManipulatorXS(
        robot_model='px150',
        group_name='arm',
        gripper_name='gripper',
    )

    try:
        while True:
            # Randomly select a defect type
            defect_type = random.choice(['D1', 'D2', 'None'])
            print(f"Detected defect type: {defect_type}")

            if defect_type == 'D1':
                perform_motion_p1(bot)
            elif defect_type == 'D2':
                perform_motion_p2(bot)
            elif defect_type == 'None':
                print("No defect detected. Robot remains idle.")

            # Wait for a short interval before detecting the next defect
            time.sleep(2)

    except KeyboardInterrupt:
        # This allows the user to stop the loop by pressing Ctrl+C
        print("Stopping the continuous motion.")
        bot.arm.go_to_home_pose()

def perform_motion_p1(bot):
    print("Performing motion P1 for defect type D1.")
    start_time = time.time()

    # Ensure a consistent starting position
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.go_to_home_pose()
    time.sleep(0.5)  # Allow the robot to stabilize

    # P1 Motion: Adjusted for reachable workspace
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.1)  # Move to P1
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.1)  # Return to start

    elapsed_time = time.time() - start_time
    print(f"Motion P1 completed in {elapsed_time:.2f} seconds.")
    print("Returning to starting position and stabilizing.")
    bot.arm.go_to_home_pose()
    time.sleep(1.0)  # Additional stabilization time

def perform_motion_p2(bot):
    print("Performing motion P2 for defect type D2.")
    start_time = time.time()

    # Ensure a consistent starting position
    bot.arm.set_ee_pose_components(x=0.3, z=0.2)
    bot.arm.go_to_home_pose()
    time.sleep(0.5)  # Allow the robot to stabilize

    # P2 Motion: Adjusted for reachable workspace
    bot.arm.set_ee_cartesian_trajectory(x=0.05, z=-0.05)  # Move to P2
    bot.arm.set_ee_cartesian_trajectory(x=-0.05, z=0.05)  # Return to start

    elapsed_time = time.time() - start_time
    print(f"Motion P2 completed in {elapsed_time:.2f} seconds.")
    print("Returning to starting position and stabilizing.")
    bot.arm.go_to_home_pose()
    time.sleep(1.0)  # Additional stabilization time

if __name__ == '__main__':
    main()
