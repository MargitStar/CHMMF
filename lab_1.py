import sys

def exact_function(x):
    return 2 * (x - 1) ** 2

def apprs_diff(y1, y2, N, result):
    for i in range(N):
        result = max(result, abs(y1[i] - y2[i * 2]))
    return result

def appr_exact_diff(y, N, x, result):
    for i in range(N):
        result = max(result, abs(y[i] - exact_function(x[i])))
    return result

def make_difference_scheme(A, B, h):
    N = int((B - A) / h)

    x = [A]
    a = [0]
    b = [-1 / h - 2 + h / 2]
    c = [1 / h]
    f = [- 3 + (4/5)*(h/2)]
    for i in range(1, N):
        x.append(x[i - 1] + h)
        a.append(1/(h ** 2) - (x[i]+1)/ (2*h))
        b.append(-2/(h**2) - 2)
        c.append(1/(h**2) + (x[i]+1)/(2*h))
        f.append(4*(2*x[i] - 1))
    
    x.append(B)
    a.append(0)
    b.append(1)
    f.append(1/2)
    return a, b, c, f, x, N

def find_solution(a, b, c, f, n):
    c[0] /= b[0]
    f[0] /= b[0]

    for i in range(1, n):
        c[i] /= b[i] - a[i] * c[i - 1]
        f[i] = (f[i] - a[i] * f[i - 1]) / (b[i] - a[i] * c[i - 1])
    
    f[n] = (f[n] - a[n] * f[n - 1]) / (b[n] - a[n] * c[n - 1])

    for i in reversed(range(0,n)):
        f[i] -= c[i] * f[i + 1]

def display_solution(x, y, N, h):
    print(f'Solution with h = {h}')
    for i in range(N + 1):
        print(f'({x[i]:.4f}, {y[i]:.4f})')
    
# With h = 0.1
a, b, c, f, x, N = make_difference_scheme(0.5, 1.5, 0.1)
for i in range(1, N):
    if abs(b[i]) < abs(a[i]) + abs(c[i]):
        sys.exit("No diagonal dominance")

find_solution(a, b, c, f, N)
display_solution(x, f, N, 0.1)

# With h = 0.05
a1, b1, c1, f1, x1, N1 = make_difference_scheme(0.5, 1.5, 0.05)
for i in range(1, N1):
    if abs(b1[i]) < abs(a1[i]) + abs(c1[i]):
        sys.exit("No diagonal dominance")
find_solution(a1, b1, c1, f1, N1)
display_solution(x1, f1, N1, 0.05)

print(f'||U(X) - Y_h/2(x)||: {appr_exact_diff(f1, N1, x1, 0)}')
print(f'||Y_h(x) - Y_h/2(x)||: {apprs_diff(f, f1, N, 0)}')