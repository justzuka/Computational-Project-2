import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n = 1000

def volume(f, a, b):
    dx = (b - a) / n 
    cur = a 
    volume = 0
    while cur <= b:
        volume += np.pi * f(cur)**2 * dx 
        cur += dx 
    
    return volume

def find_fraction_volume(f, a, b, calculated_volume, fraction):
    dx = (b - a) / n 
    cur = a 
    volume = 0
    while cur <= b:
        volume += np.pi * f(cur)**2 * dx 
        
        if volume >= calculated_volume * fraction:
            return cur

        cur += dx 
    return None

def f(x):
    return x**2  # Example function f(x)

a = 0.0  # Lower limit of integration
b = 3 * np.pi  # Upper limit of integration

Volume = volume(f, a, b)
print("Volume: ", Volume)

fraction = 1/2
frac_x = find_fraction_volume(f, a, b, Volume, fraction)



# Generate x values for the curve
x = np.linspace(a, b, 100)

# Compute y and z values for the curve
y = np.zeros_like(x)
z = f(x)

# Create mesh grid for generating the solid of revolution
theta = np.linspace(0, 2*np.pi, 100)
X, Theta = np.meshgrid(x, theta)

# Compute coordinates for each point on the surface
Y = np.sin(Theta) * y + np.cos(Theta) * z
Z = np.cos(Theta) * y - np.sin(Theta) * z

high = np.max(Z)

# Plot the solid of revolution
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(frac_x, 0, np.linspace(-high, high, 100), color='red', marker='o', s=50)

ax.plot_surface(X, Y, Z, cmap='viridis',alpha=0.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Solid of Revolution')
plt.show()
