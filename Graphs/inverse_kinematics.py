import numpy as np
from scipy.linalg import expm

# Define the screw axis (Slist) and home configuration (M)
M = np.array([
    [1.0, 0, 0, 0.358575],
    [0.0, 1, 0, 0],
    [0, 0, 1, 0.25457],
    [0, 0, 0, 1]
])

Slist = np.array([
    [0, 0, 1, 0, 0, 0],
    [0, 1, 0, -0.10457, 0, 0],
    [0, 1, 0, -0.25457, 0, 0.05],
    [0, 1, 0, -0.25457, 0, 0.2],
    [1, 0, 0, 0, 0.25457, 0]
]).T

# Define joint angles (thetas)
thetas = [1.0, 0.0, 0.0, 0.0, 0.0]  # Waist joint is 1.0 radians, others are 0

# Function to compute the matrix exponential of a screw axis
def matrix_exp6(screw, theta):
    se3mat = np.array([
        [0, -screw[2], screw[1], screw[3]],
        [screw[2], 0, -screw[0], screw[4]],
        [-screw[1], screw[0], 0, screw[5]],
        [0, 0, 0, 0]
    ])
    return expm(se3mat * theta)

# Compute the transformation matrix T
T = np.eye(4)
for i in range(len(thetas)):
    T = np.dot(T, matrix_exp6(Slist[:, i], thetas[i]))
T = np.dot(T, M)

# Extract the end-effector position (XYZ)
end_effector_position = T[:3, 3]
print(f"End-effector position: X={end_effector_position[0]:.4f}, "
      f"Y={end_effector_position[1]:.4f}, Z={end_effector_position[2]:.4f}")
