import numpy as np
import matplotlib.pyplot as plt

def volume(f, a, b, n_x, n_y):
    dx = (b - a) / n_x
    dy = 2 * np.pi / n_y
    total_volume = 0.0

    for i in range(n_x):
        cur_x = a + i * dx

        for j in range(n_y):
            cur_y = -np.pi + j * dy
            z = f(cur_x, cur_y)

            base_level = f(cur_x, -np.pi)  # Height at the base level

            volume_contribution = z # - base_level
            volume_contribution *= dx * dy

            total_volume += volume_contribution

    return total_volume

def find_fraction_points_volume(f, a, b, n_x, n_y, calculated_volume, fraction):
    dx = (b - a) / n_x
    dy = 2 * np.pi / n_y
    total_volume = 0.0
    points = []
    for i in range(n_x):
        cur_x = a + i * dx

        for j in range(n_y):
            
            cur_y = -np.pi + j * dy
            points.append((cur_x,cur_y))
            z = f(cur_x, cur_y)

            base_level = f(cur_x, -np.pi)  # Height at the base level

            volume_contribution = z # - base_level
            volume_contribution *= dx * dy

            total_volume += volume_contribution

            if total_volume >= calculated_volume * fraction:
                return points

    return None


# Example function f(x, y)
def f(x, y):
    return abs(np.sin(x) + np.cos(y))

a = 0.0
b = 2 * np.pi
n_x = 100  # Number of subdivisions along the x-axis
n_y = 100  # Number of subdivisions along the y-axis

# Compute the volume
computed_volume = volume(f, a, b, n_x, n_y)
print("Computed Volume:", computed_volume)

# Plot the function
x = np.linspace(a, b, 100)
y = np.linspace(-np.pi, np.pi, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fraction = 1/2

points = find_fraction_points_volume(f, a, b, n_x, n_y, computed_volume, fraction)

pX = [x[0] for x in points]
pY = [x[1] for x in points]
pZ = [f(pX[i], pY[i]) + .1 for i in range(len(points))]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis',alpha=0.5)
ax.scatter(pX, pY, pZ, c='b', marker='o')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Function Plot')
plt.show()





