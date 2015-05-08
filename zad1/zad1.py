import matplotlib.pyplot as plt
import math
import random

counter = 0


def f(x1, y1, x2, y2):
    """
    :param x1: 1 point x
    :param y1: 1 point y
    :param x2: 2 point x
    :param y2: 2 point y
    :return: distance
    """
    return math.sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2)


def t(n):
    global T0
    return T0 / n


def random_tour(arr, n):
    """
    Return random path
    :param arr: array
    :param n:
    :return:
    """
    return [[0 for x in range(2)] for x in range(n)]


def calculate_distance(arr, n):
    """
    Return max distance
    :param arr:
    :param n:
    :return:
    """
    dist = 0.0
    for i in range(n - 1):
        dist += f(arr[i][0], arr[i][1], arr[i + 1][0], arr[i + 1][1])
    return dist + f(arr[n - 1][0], arr[n - 1][1], arr[0][0], arr[0][1])


def generate_normal_four_group(arr, n):
    sigma = 300  # odchylenie
    mu = 500  # srednia

    for i in range(n):
        arr[i][0] = random.gauss(mu, sigma)
        arr[i][1] = random.gauss(mu, sigma)
    return arr


def generate_nine_groups(arr, n):
    for i in range(n):
        arr[i][0] = random.randint((i % 9) * 50, ((i % 9) * 50) + 25)
        arr[i][1] = random.randint((i % 9) * 50, ((i % 9) * 50) + 25)
    return arr


def swap1(arr, n):
    new = list(arr)
    a = random.randint(0, n - 1)
    if a + 1 > n - 1:
        new[a], new[0] = new[0], new[a]
    else:
        new[a], new[a + 1] = new[a + 1], new[a]
    return new


def swap2(arr, n):
    global counter
    new = list(arr)
    if counter + 1 > n - 1:
        new[counter], new[0] = new[0], new[counter]
    else:
        new[counter], new[counter + 1] = new[counter + 1], new[counter]

    counter += 1
    if counter > n - 1:
        counter = 0
    return new


def annealing(arr, n, T, k):
    distance = calculate_distance(arr, n)
    current_path = arr
    for i in range(1, k):
        neighbour = swap1(current_path, n)
        distance_new = calculate_distance(neighbour, n)
        if distance_new < distance:
            current_path = neighbour
            distance = distance_new
        else:
            if math.exp((distance - distance_new) / T) > 0.8:
                current_path = neighbour
                distance = distance_new
        T = t(i)
        temperature.append(T)
        energy_foo.append(distance)
    return current_path


# Main program:
n = int(raw_input("Number of cities (n): "))
T0 = T = 1000
k = int(raw_input("Maximum number of steps: "))
maxVal = 100

arr = []
for x in range(n):
    arr.append([0 for i in range(2)])
for i in range(n):
    arr[i][0] = random.randint(0, maxVal)
    arr[i][1] = random.randint(0, maxVal)

# additional generation
# arr = generate_nine_groups(arr, n)
arr = generate_normal_four_group(arr, n)

print arr

energy_foo = []
temperature = [T]
solution = annealing(arr, n, T, k)

plt.figure(1)
plt.title("Solution")
plt.plot([row[0] for row in solution] + [solution[0][0]], [row[1] for row in solution] + [solution[0][1]], marker="x")
plt.draw()
plt.figure(2)
plt.title("Distance in steps")
plt.plot(range(k - 1), energy_foo)
plt.draw()
plt.figure(3)
plt.title("Temperature in steps")
plt.plot(range(k), temperature)
plt.show()
