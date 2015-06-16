import matplotlib.pyplot as plt
import math
import random


def f(x1, y1, x2, y2):
    return math.sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2)


def neighbours_4(x, y, arr, n):
    if arr[x][y] == 0:
        return 0

    number = 0
    # |
    #-x-
    # |
    if x - 1 > 0:
        number += 1

    if x + 1 < n:
        number += 1

    if y + 1 < n:
        number += 1

    if y - 1 > 0:
        number += 1

    return energy_fun(number)


def neighbours_8(x, y, arr, n):
    if arr[x][y] == 0:
        return 0

    neighbours = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if 0 < i < n and 0 < j < n:
                if i != x and j != y:
                    neighbours += 1

    return energy_fun(neighbours)


def temp(n):
    global T0
    return T0 / n


def energy_fun(n):
    if n == 0:
        return 0.0
    else:
        return 1.0 / n


def swap(arr, n):
    new = list(arr)
    max = n-1
    x1 = random.randint(0, max)
    y1 = random.randint(0, max)

    x2 = random.randint(0, max)
    y2 = random.randint(0, max)

    while new[x2][y2] == new[x1][y1] or (x2 == x1 and y2 == y1):
        x2 = random.randint(0, max)
        y2 = random.randint(0, max)

    new[x1][y1], new[x2][y2] = new[x2][y2], new[x1][y1]
    return new


def calculate_energy(arr, n):
    global type
    if type == 1:
        f = neighbours_4
    else:
        f = neighbours_8

    energy = 0.0
    for x in range(n - 1):
        for y in range(n - 1):
            energy += f(x, y, arr, n)
    return energy


def annealing(arr, n, T, k):
    value_now = calculate_energy(arr, n)
    solution_now = list(arr)
    for i in range(1, k):
        solution_next = swap(solution_now, n)
        value_next = calculate_energy(solution_next, n)
        if value_next < value_now:
            solution_now = list(solution_next)
            value_now = value_next
        else:
            if math.exp((value_now - value_next) / T) > 0.8:
                solution_now = list(solution_next)
                value_now = value_next
        T = temp(i)
    return solution_now


def redraw(solution):
    global blacks, n
    s = []
    for p in range(2):
        s.append([0 for p in range(blacks)])
    i = 0
    for x in range(n):
        for y in range(n):
            if solution[x][y] == 1:
                s[0][i] = x
                s[1][i] = y
                i += 1
    return s


# Main program:
n = int(raw_input("Dimensions (n x n) n:"))
k = int(raw_input("Number of steps:"))
d = float(raw_input("Density: "))
print "Types:\n1 - 4 neighbours\n2 - 8 neighbours"
type = int(raw_input("Type:"))
T0 = T = 1000

arr = []
for x in range(n):
    arr.append([0 for y in range(n)])

blacks = int(math.ceil(d * (n ** 2)))

for i in range(blacks):
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    if arr[x][y] == 0:
        arr[x][y] = 1
    else:
        while arr[x][y] == 1:
            x = random.randint(0,n-1)
            y = random.randint(0,n-1)
        arr[x][y] = 1

plt.figure(1)
plt.title("Old")
XY1 = redraw(arr)
plt.scatter(XY1[0], XY1[1])
plt.draw()

plt.figure(2)
plt.title("New")
solution = annealing(arr, n, T, k)
XY = redraw(solution)
plt.scatter(XY[0], XY[1])
plt.draw()
plt.show()