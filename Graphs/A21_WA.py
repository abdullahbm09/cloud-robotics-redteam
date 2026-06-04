import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the waypoints for the main trajectory in 3D space
main_waypoints = [
    {"label": "Initial Position", "x": 0.3, "y": 0, "z": 0.2},
    {"label": "Grasping Position", "x": 0.1, "y": 0.1, "z": -0.16},
    {"label": "Releasing Position", "x": -0.1, "y": -0.1, "z": 0.16}
]

# Define the holding position as a separate trajectory
holding_position = {"label": "Holding Position (Attack)", "x": 0.1937, "y": 0.3017, "z": 0.2546}

# Extract coordinates for the main trajectory
main_x_coords = [wp["x"] for wp in main_waypoints]
main_y_coords = [wp["y"] for wp in main_waypoints]
main_z_coords = [wp["z"] for wp in main_waypoints]

# Extract coordinates for the holding position
holding_x = holding_position["x"]
holding_y = holding_position["y"]
holding_z = holding_position["z"]

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the main trajectory
ax.plot(main_x_coords, main_y_coords, main_z_coords, 'bo-', label="Normal Movement (Without attack)")  # Line connecting waypoints

# Annotate and highlight each waypoint in the main trajectory
for wp in main_waypoints:
    ax.scatter(wp["x"], wp["y"], wp["z"], s=100)  # Highlight the point
    ax.text(wp["x"] + 0.02, wp["y"] + 0.02, wp["z"], wp["label"], fontsize=10)

# Plot the holding position as a separate point
ax.scatter(holding_x, holding_y, holding_z, s=100, color="red", label="Holding Position (During Attack)")
ax.text(holding_x + 0.02, holding_y + 0.02, holding_z, holding_position["label"], fontsize=10, color="red")

# Plot customization
ax.set_title("3D Waypoint Trajectories of the Robotic Arm")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")

# Set grid and legend
ax.legend()

# Save the plot in 500 DPI as PNG
plt.savefig("A21_WA.png", dpi=500, format='png')
plt.show()
