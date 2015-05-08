# SUDOKU
import math
import random
import os
import os.path

block_num = 3
############
def temp(n):
    global T0
    T = T0 / (n ** 2)
    return T  #na poczatek


##########
def calculate(arr, n):
    energy = 0
    for i in range(n):
        for j in range(n):
            energy += count_rows_cols(i, j, arr, n) + count_block(i, j, arr, n)
    return energy


##############
def count_rows_cols(i, j, arr, n):
    val = arr[i][j]
    count = 0
    for x in range(n):
        if arr[x][j] == val and x != i:
            count += 1

    for y in range(n):
        if arr[i][y] == val and y != j:
            count += 1
    return count


##################
def count_block(i, j, arr, n):
    global block_num
    val = arr[i][j]
    count = 0
    blockNumX = (i / block_num)  # 0..2
    blockNumY = (j / block_num)  #
    for x in range(blockNumX * 3, blockNumX * 3 + 3):
        for y in range(blockNumY * 3, blockNumY * 3 + 3):
            if arr[x][y] == val and (x != i or y != j):
                count += 1

    return count


##############
def simple_swap(arr, n):
    global orig
    new = list(arr)  #kopia?
    #23:39, moze to jeszcze dzis skonczymy :)
    xb = random.randint(0, block_num - 1)  #losujemy blok
    yb = random.randint(0, block_num - 1)

    #Moze byc przypadek ze wszystkie pola w bloku mamy zahardkodowane,
    #dlatego sprawdzamy czy jest sens w ogole bawic sie tu w zamiany
    while notHardcoded(xb, yb) <= 1:
        xb = random.randint(0, block_num - 1)  #losujemy blok
        yb = random.randint(0, block_num - 1)

    ax = random.randint(xb * 3, xb * 3 + 2)
    ay = random.randint(yb * 3, yb * 3 + 2)

    while orig[ax][ay] == True:  #trafilismy na zahardkodowany
        ax = random.randint(xb * 3, xb * 3 + 2)
        ay = random.randint(yb * 3, yb * 3 + 2)

    bx = random.randint(xb * 3, xb * 3 + 2)
    by = random.randint(yb * 3, yb * 3 + 2)

    while orig[bx][by] == True or (ax == bx and ay == by):
        bx = random.randint(xb * 3, xb * 3 + 2)
        by = random.randint(yb * 3, yb * 3 + 2)

    new[ax][ay], new[bx][by] = new[bx][by], new[ax][ay]
    return new


##################
def notHardcoded(xb, yb):
    global orig
    count = 0
    for x in range(xb * 3, xb * 3 + 3):
        for y in range(yb * 3, yb * 3 + 3):
            if orig[x][y] == False:
                count += 1
    return count


##################
def write_solution(solution):
    pass


###################
def sim_annealing(arr, n, T, k):
    energy_val = [0.0] * (k + 1)
    current_solution = list(fill_arr(arr, n))
    current_val = calculate(current_solution, n)
    for i in range(1, k):
        neighbour = simple_swap(current_solution, n)
        second_val = calculate(neighbour, n)
        if second_val < current_val:
            current_solution = neighbour
            current_val = second_val
        else:
            if math.exp((current_val - second_val) / T) > 0.8:
                current_solution = neighbour
                current_val = second_val
        T = temp(i)
        energy_val[i] = current_val

    print "Value: " + str(current_val)
    plt.plot(range(k + 1), energy_val)
    plt.draw()
    plt.show()
    return current_solution


#################################
def writeArr(f, arr):
    global orig
    for i in range(9):
        for j in range(9):
            c = f.read(1)
            f.read(1)
            if c == 'x':
                arr[i][j] = 0
                orig[i][j] = False
            else:
                arr[i][j] = int(c)
                orig[i][j] = True


#################################

def writeSolution(f, solution):
    for i in range(3):
        for j in range(3):
            f.write(str(solution[i][j]) + " ")
        f.write('\n')


##############################
def fill_arr(arr, n):
    #Kilka sposobow:
    #1. Wypelnic wartosciamy unikalnymi w kazdym bloku i w kazdej iteracji sobie permutujemy liczby w bloku
    #2. Nawrzucac absurdalnie losowe wartosci i w kazdej iteracji wybierac np. 9 takich (z kazdego bloku) dla ktorego losuje znowu
    #Wybieram sobie rozw. nr 1 - bardziej madre i prawdopodobne
    global orig
    i = 1
    for xb in range(block_num):
        for yb in range(block_num):
            for x in range(xb * 3, xb * 3 + 3):
                for y in range(yb * 3, yb * 3 + 3):
                    if arr[x][y] == 0:
                        #9 wartosci unikalnych w polu
                        while isInBlock(i, arr, xb, yb):
                            i += 1
                        arr[x][y] = i
            i = 1
    return arr


##############################
def isInBlock(i, arr, xb, yb):
    for x in range(xb * 3, xb * 3 + 3):
        for y in range(yb * 3, yb * 3 + 3):
            if arr[x][y] == i:
                return True

    return False

#############################
#n = int(raw_input("Input n: "))
T = float(raw_input("Input T: "))
k = int(raw_input("Input no. of steps: "))

T0 = T  #poczatkowa temperatura
i = 1
print "Reading from file..."
T = T0
for name in os.listdir('./test'):
    if os.path.isfile('./test/' + name):  #TODO: Sprawic by to ladniej wygladalo
        arr = [[0 for x in range(9)] for x in range(9)]
        orig = [[0 for x in range(9)] for x in
                range(9)]  #orig daje nam informacje ktore pola mozemy sobie permutowac swobodnie
        f = open('./test/' + name, 'r')
        writeArr(f, arr)
        print "Before"
        for p in range(9):
            print arr[p]

        print "Working..."
        solution = sim_annealing(arr, 9, T, k)
        print "Writing..."
        f2 = open(str(i) + "_solution.txt", 'w')
        writeSolution(f2, solution)
        f.close()
        f2.close()
        i += 1
        print "Results:"
        for q in range(9):
            print solution[q]
