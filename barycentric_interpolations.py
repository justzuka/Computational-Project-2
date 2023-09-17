import numpy as np
# Plot the result
import matplotlib.pyplot as plt
def barycentric_rational_interpolation(xs, ys, xx):
    count = 0
    n = len(xs)
    m = len(xx)
    w = np.ones(n)

    for j in range(n):
        for k in range(n):
            count += 1
            if j != k:
                w[j] *= 1 / (xs[j] - xs[k])

    yy = np.zeros(m)
    for i in range(m):
        numer = 0.0
        denom = 0.0

        for j in range(n):
            count += 1
            wj = w[j] / (xx[i] - xs[j])
            numer += wj * ys[j]
            denom += wj

        yy[i] = numer / denom

    print("barycentric steps= ", count)
    return yy
# Define the function to be interpolated
def f(x):
    return np.exp(x)


def main():
    n = 50
    # Define the interpolation points
    xs = np.linspace(0, 2*np.pi, n)
    ys = f(xs)
    
    # Define the points to be interpolated
    x = np.linspace(0, 2*np.pi, 100)

    # Compute the interpolation
    y = barycentric_rational_interpolation(xs, ys, x)

    # error = [abs(f(x[i]) - y[i]) for i in range(len(x))]
    error = np.abs(y - f(x))

    plt.plot(x, f(x), label='f(x)')
    plt.plot(xs, ys, 'o', label='interpolation points')
    plt.plot(x, error,label='error')
    plt.plot(x, y, label='interpolation')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()