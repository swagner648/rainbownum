from .LinkedLists import SetLinkedList
from .LinkedLists import ColoringLinkedList
import time


class RainbowSim:
    def __init__(self, n, a, b, mod):
        if type(n) is not int:
            raise TypeError("Scalar n must be an integer greater than or equal to 1")
        if n < 1:
            raise ValueError("Scalar n must be greater than or equal to 1.")
        self.n = n

        for i in a:
            if type(i) is not int:
                raise TypeError("Vector a[] can only contain nonzero integers")
            if i is 0:
                raise ValueError("Vector a[] cannot contain 0-value elements.")
        self.a = a
        self.k = len(a)

        if type(b) is not int:
            raise TypeError("Scalar b must be an integer.")
        self.b = b

        if type(mod) is not bool:
            raise TypeError("Boolean mod must be either", True, "for Zn or", False, "for [n].")
        self.mod = mod

        self.sets = [0 for _ in range(n)]
        for i in range(n):
            self.sets[i] = SetLinkedList()

        self.colorings = ColoringLinkedList()

        self.timeLimit = 43200
        self.start = 0

    def run(self):
        self.start = time.time()
        coloring = ["*" for _ in range(self.n)]
        coloring[0] = 0
        used = [0 for _ in range(self.n)]
        used[0] = 1
        self.gen_colorings(coloring, used, 1)
        if self.start == -1:
            print("\naS(" + str(self.k) + ", " + str(self.n) + ") computation exceed time limit.")
            return None
        print("\naS(" + str(self.k) + ", " + str(self.n) + ") = ", str(self.colorings.maxColors+1))
        print("Total colorings:", self.colorings.len)
        print("Time:", time.time() - self.start)
        return 1

    def gen_colorings(self, coloring, used, loop):
        if time.time() - self.start > self.timeLimit:
            self.start = -1
            return
        if loop == self.n:
            return
        for i in range(0, self.n):
            if i != 0 and used[i-1] == 0:
                return
            used[i] += 1
            coloring[loop] = i
            if self.contains_rainbow_sum(coloring, loop):
                used[i] -= 1
                continue
            self.gen_colorings(coloring, used, loop+1)
            if loop == self.n-1:
                colors = 0;
                for j in used:
                    if j == 0:
                        break
                    colors += 1
                self.colorings.add_coloring(coloring, colors)
            used[i] -= 1

    def contains_rainbow_sum(self, coloring, new):
        temp = self.sets[new].head.next
        while temp is not None:
            skip = False
            used = [0 for _ in range(self.n)]
            unique = True
            for i in temp.data:
                if i > new:
                    skip = True
                    break
                used[coloring[i]] += 1
                if used[coloring[i]] > 1:
                    unique = False
            if skip:
                temp = temp.next
                continue
            if unique:
                return True
            temp = temp.next
        return False

    def check_coloring(self, coloring):
        for i in range(1, self.n):
            if self.contains_rainbow_sum(coloring, i) is True:
                print("INVALID: Coloring", coloring, "for n =", self.n, "contains rainbow sums :(")
                return
        print("VALID: Coloring", coloring, "for n = ", self.n, "works!")

    def print_extreme_colorings(self, quantity=-1):
        if self.start != -1:
            temp = self.colorings.head
            i = 0
            while temp is not None and (i < quantity or quantity < 0):
                if i == 0:
                    print(temp, end='')
                else:
                    print(',', temp, end='')
                temp = temp.next
                i += 1
        print()

    def print_sets(self, number=-1):
        print('Sets Generated:', end='')
        for n in range(self.n):
            if number >= 0 and self.mod:
                n = number
            if number >= 0 and not self.mod:
                n = number-1
            if self.mod:
                temp = self.sets[n].head.next
                print('\n', n, ':', temp, end='')
                if temp is not None:
                    temp = temp.next
                    while temp is not None:
                        print(',', temp, end='')
                        temp = temp.next
            else:
                temp = self.sets[n].head.next
                print('\n', n+1, ':', temp, end='')
                if temp is not None:
                    temp = temp.next
                    while temp is not None:
                        print(',', [i + 1 for i in temp.data], end='')
                        temp = temp.next
            if number >= 0:
                return
        print()

    def set_time_limit(self, t):
        self.timeLimit = t

    def time_limit_reached(self):
        return self.start < 0

    def is_distinct(self, out, valid):
        if not valid:
            return False
        for i in out[:-1]:
            if i == out[self.k-1]:
                return False
        return True

    def sum_leq_n(self, out, valid):
        if not valid:
            return False
        if not self.mod and out[self.k-1] > self.n:
            return False
        return True

    def decrement_if_not_mod(self, out, valid):
        if not valid or self.mod:
            return out
        for i in range(self.k):
            out[i] = out[i] - 1
        return out

    def add_set(self, out, valid):
        if not valid:
            return
        for i in out:
            self.sets[i].add_set(out)
