import numpy as np
import matplotlib.pyplot as plt

def dx(f, h=1e-6):
    return lambda x: (f(x + h) - f(x - h)) / (2 * h)


def pade(m, n, f):
    count = 0
    N = m + n
    a = np.zeros(N + 1)

    df = f
    for i in range(N + 1):
        count += 1
        a[i] = df(0) / np.math.factorial(i)
        df = dx(df)
        df = f


    q = np.zeros(m + 1)
    p = np.zeros(n + 1)

    q[0] = 1
    p[0] = a[0]

    B = np.zeros((N + 1, N + 2))
    for i in range(1, N + 1):
        for j in range(1, i):
            count += 1
            if j <= n:
                B[i, j] = 0
        
        if i <= n:
            B[i, i] = 1

        for j in range(i + 1, N + 1):
            count += 1
            B[i, j] = 0

        for j in range(1, i):
            count += 1
            if j <= m:
                B[i, n + j] = -a[i - j]

        for j in range(n + i + 1, N + 1):
            count += 1
            B[i, j] = 0

        B[i, N + 1] = a[i]

    # solve the linear system using partial pivoting
    for i in range(n + 1, N):
        # find pivot element
        # Let k be the smallest integer with i ≤ k ≤ N and |bk,i| = maxi≤j≤N |bj,i|
        k = np.argmax(np.abs(B[i:, i])) + i
        if B[k, i] == 0:
            print("The system is singular.")
            return None
        
        # interchange rows i and k
        if k != i:
            B[[i, k]] = B[[k, i]]

        # for each row j below i, subtract a multiple of row i so that the new entry in column i is zero
        for j in range(i + 1, N + 1):
            xm = B[j, i] / B[i, i]
            for k in range(i, N + 2):
                count += 1
                B[j, k] -= xm * B[i, k]
            
            B[j, i] = 0

    if B[N, N] == 0:
        print("The system is singular.")
        return None
    
    if m > 0:
        q[m] = B[N, N + 1] / B[N, N]

    for i in range(N - 1, n, -1):
        count += 1
        q[i - n] = (B[i, N + 1] - np.dot(B[i, i + 1:N + 1], q[i - n + 1:])) / B[i, i]

    for i in range(n, -1, -1):
        count += 1
        p[i] = B[i, N + 1] - sum([B[i, j] * q[j-n] for j in range(n + 1, N + 1)])
    print('pade steps: ', count)
    return p, q


def f(x):
    return np.exp(x)


def r(x, p, q):
    return np.polyval(p, x) / np.polyval(q, x)


def main():
    m = 40
    n = 100
    p, q = pade(m, n, f)

    p = p[1:]
    q = q[1:]

    p = np.flip(p)
    q = np.flip(q)

    x = np.linspace(0, 10, 100)
    y = f(x)
    y1 = r(x, p, q)

    error = np.abs(y - (-y1))

    plt.plot(x, y, label='original')
    plt.plot(x, -y1, label='pade approximation')
    plt.plot(x, error, label='error')
    plt.legend()
    plt.show()




if __name__ == '__main__':
    main()
