from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp
import numpy as np


class SudokuPuzzle(object):
    def __init__(self, data, original_entries=None):
        self.data = data
        if original_entries is None:
            self.original_entries = np.arange(81)[self.data > 0]  # list: not 0 positions
        else:
            self.original_entries = original_entries

    def random_not_counted(self):
        """
        Setting zero as random
        """
        for num in range(9):
            block_indices = self.get_block(num)
            block = self.data[block_indices]
            zero_indices = [ind for i, ind in enumerate(block_indices) if block[i] == 0]
            to_fill = [i for i in range(1, 10) if i not in block]
            shuffle(to_fill)
            for ind, value in zip(zero_indices, to_fill):
                self.data[ind] = value

    def get_block(self, k, ignore_originals=False):
        """
        Get 3x3 blocks
        """
        row_offset = (k // 3) * 3
        col_offset = (k % 3) * 3
        ptr = [col_offset + (j % 3) + 9 * (row_offset + (j // 3)) for j in range(9)]
        if ignore_originals:
            ptr = filter(lambda x: x not in self.original_entries, ptr)
        return ptr

    @staticmethod
    def get_column(i):
        return [i + 9 * j for j in range(9)]

    @staticmethod
    def get_row(i):
        return [j + 9 * i for j in range(9)]

    def __str__(self):
        def not_zero(s):
            if s != 0:
                return str(s)
            else:
                return "x"

        results = np.array([self.data[self.get_row(j)] for j in range(9)])
        out_s = ""
        for i, row in enumerate(results):
            if i % 3 == 0:
                out_s += "-" * 25 + '\n'
            out_s += "| " + " | ".join(
                [" ".join(not_zero(s) for s in list(row)[3 * (k - 1):3 * k]) for k in range(1, 4)]) + " |\n"
        out_s += "-" * 25 + '\n'
        return out_s

    def score_board(self):
        """
        -1 when unique
        """
        score = 0
        for row in range(9):
            score -= len(set(self.data[self.get_row(row)]))
        for col in range(9):
            score -= len(set(self.data[self.get_column(col)]))
        return score

    def swap_random(self):
        """
        Picking a square, then swap two small squares within.
        """
        new_data = deepcopy(self.data)
        block = randint(0, 8)
        num_in_block = len(self.get_block(block, ignore_originals=True))
        random_squares = sample(range(num_in_block), 2)
        square1, square2 = [self.get_block(block, ignore_originals=True)[ind] for ind in random_squares]
        new_data[square1], new_data[square2] = new_data[square2], new_data[square1]
        return new_data

    def solve(self, verbose=False):
        self.random_not_counted()
        current = self.score_board()
        best = current
        T = 0.5  # initial T

        for count in range(0, 400000):
            if verbose and (count % 1000 == 0):
                print "%s,\tT = %.7f,\tbest_till_now = %s,\tcurrent = %s" % \
                      (count, T, best, current)

            new_data = self.swap_random()
            new = SudokuPuzzle(new_data, self.original_entries).score_board()
            delta = float(current - new)

            if exp((delta / T)) - random() > 0:
                self.data = new_data
                current = new

            if current < best:
                best = new

            if new == -162:
                self.data = new_data
                break

            T *= .99999

        if best == -162:
            print "\nSolved."
        else:
            print "\nNot solved :(. (%s/-162 points). Try again." % (best)

SP = SudokuPuzzle((np.array([
    5, 3, 0, 0, 7, 0, 0, 0, 0,
    6, 0, 0, 1, 9, 5, 0, 0, 0,
    0, 9, 8, 0, 0, 0, 0, 6, 0,
    8, 0, 0, 0, 6, 0, 0, 0, 3,
    4, 0, 0, 8, 0, 3, 0, 0, 1,
    7, 0, 0, 0, 2, 0, 0, 0, 6,
    0, 6, 0, 0, 0, 0, 2, 8, 0,
    0, 0, 0, 4, 1, 9, 0, 0, 5,
    0, 0, 0, 0, 8, 0, 0, 7, 9])))
print SP
SP.solve(verbose=True)
print SP