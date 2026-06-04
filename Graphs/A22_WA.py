import matplotlib.pyplot as plt

# Define waypoints for motion P1
motion_p1 = [
    {"label": "Initial Position", "x": 0.3, "y": 0, "z": 0.2, "marker": "^"},
    {"label": "Pick-Up Position (P1)", "x": 0.1, "y": 0, "z": -0.15, "marker": "^"},
    {"label": "Return to Initial (P1)", "x": -0.1, "y": 0, "z": 0.15, "marker": "^"},
]

# Define waypoints for motion P1
motion_p1_attack = [
    {"label": "", "x": 0.3, "y": 0, "z": 0.2, "marker": "+"},
    {"label": "", "x": 0.125, "y": 0, "z": -0.14, "marker": "+"},
    {"label": "", "x": -0.125, "y": 0, "z": 0.14, "marker": "+"},
]

# # Define waypoints for motion P2
# motion_p2 = [
#     {"label": "Initial Position", "x": 0.3, "y": 0, "z": 0.2, "marker": "o"},
#     {"label": "Pick-Up Position (P2)", "x": 0.2, "y": 0, "z": -0.2, "marker": "o"},
#     {"label": "Return to Initial (P2)", "x": -0.2, "y": 0, "z": 0.2, "marker": "o"},
# ]

# Extract coordinates for motion P1
p1_x_coords = [wp["x"] for wp in motion_p1]
p1_y_coords = [wp["y"] for wp in motion_p1]
p1_z_coords = [wp["z"] for wp in motion_p1]

# # Extract coordinates for motion P2
# p2_x_coords = [wp["x"] for wp in motion_p2]
# p2_y_coords = [wp["y"] for wp in motion_p2]
# p2_z_coords = [wp["z"] for wp in motion_p2]

# Extract coordinates for motion P2
p2_x_coords = [wp["x"] for wp in motion_p1_attack]
p2_y_coords = [wp["y"] for wp in motion_p1_attack]
p2_z_coords = [wp["z"] for wp in motion_p1_attack]

# Create a 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot motion P1
ax.plot(p1_x_coords, p1_y_coords, p1_z_coords, 'g-', label="Motion P1 Trajectory (without perturbation)")  # Line connecting P1 waypoints
for wp in motion_p1:
    ax.scatter(wp["x"], wp["y"], wp["z"], s=100, color="green", marker=wp["marker"])  # Highlight P1 waypoints
    ax.text(wp["x"] + 0.02, wp["y"] + 0.02, wp["z"], wp["label"], fontsize=10, color="green")

# Plot motion P2
ax.plot(p2_x_coords, p2_y_coords, p2_z_coords, 'r-', label="Motion P1 Trajectory (with perturbation)")  # Line connecting P2 waypoints
for wp in motion_p1_attack:
    ax.scatter(wp["x"], wp["y"], wp["z"], s=100, color="red", marker=wp["marker"])  # Highlight P2 waypoints
    ax.text(wp["x"] + 0.02, wp["y"] + 0.02, wp["z"], wp["label"], fontsize=10, color="red")

# Plot customization
ax.set_title("3D Waypoint Trajectories for Motion P1 with and without perturbation")
ax.set_xlabel("X Coordinate (m)")
ax.set_ylabel("Y Coordinate (m)")
ax.set_zlabel("Z Coordinate (m)")

# Add grid and legend
ax.legend()

# Save the plot in 500 DPI as PNG
plt.savefig("P1_trajectory.png", dpi=500, format='png')
########################################################



# Define waypoints for motion P2
motion_p2 = [
    {"label": "Initial Position", "x": 0.3, "y": 0, "z": 0.2, "marker": "o"},
    {"label": "Pick-Up Position (P2)", "x": 0.2, "y": 0, "z": -0.2, "marker": "o"},
    {"label": "Return to Initial (P2)", "x": -0.2, "y": 0, "z": 0.2, "marker": "o"},
]

# Define waypoints for motion P1
motion_p2_attack = [
    {"label": "", "x": 0.3, "y": 0, "z": 0.2, "marker": "+"},
    {"label": "", "x": 0.225, "y": 0, "z": -0.185, "marker": "+"},
    {"label": "", "x": -0.225, "y": 0, "z": 0.185, "marker": "+"},
]


# Extract coordinates for motion P1
p1_x_coords = [wp["x"] for wp in motion_p2]
p1_y_coords = [wp["y"] for wp in motion_p2]
p1_z_coords = [wp["z"] for wp in motion_p2]


# Extract coordinates for motion P2
p2_x_coords = [wp["x"] for wp in motion_p2_attack]
p2_y_coords = [wp["y"] for wp in motion_p2_attack]
p2_z_coords = [wp["z"] for wp in motion_p2_attack]

# Create a 3D plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot motion P1
ax.plot(p1_x_coords, p1_y_coords, p1_z_coords, 'g-', label="Motion P2 Trajectory (without perturbation)")  # Line connecting P1 waypoints
for wp in motion_p2:
    ax.scatter(wp["x"], wp["y"], wp["z"], s=100, color="green", marker=wp["marker"])  # Highlight P1 waypoints
    ax.text(wp["x"] + 0.02, wp["y"] + 0.02, wp["z"], wp["label"], fontsize=10, color="green")

# Plot motion P2
ax.plot(p2_x_coords, p2_y_coords, p2_z_coords, 'r-', label="Motion P2 Trajectory (with perturbation)")  # Line connecting P2 waypoints
for wp in motion_p2_attack:
    ax.scatter(wp["x"], wp["y"], wp["z"], s=100, color="red", marker=wp["marker"])  # Highlight P2 waypoints
    ax.text(wp["x"] + 0.02, wp["y"] + 0.02, wp["z"], wp["label"], fontsize=10, color="red")

# Plot customization
ax.set_title("3D Waypoint Trajectories for Motion P2 with and without perturbation")
ax.set_xlabel("X Coordinate (m)")
ax.set_ylabel("Y Coordinate (m)")
ax.set_zlabel("Z Coordinate (m)")

# Add grid and legend
ax.legend()

# Save the plot in 500 DPI as PNG
plt.savefig("P2_trajectory.png", dpi=500, format='png')
plt.show()
