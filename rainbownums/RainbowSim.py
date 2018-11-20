from .LinkedLists import SetLinkedList
from .LinkedLists import ColoringLinkedList
import time


class RainbowSim:
    def __init__(self, n, a, b):
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
            return
        print("\naS(" + str(self.k) + ", " + str(self.n) + ") = ", str(self.colorings.maxColors+1))
        print("Total colorings:", self.colorings.len)
        print("Time:", time.time() - self.start)

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

    def print_extreme_colorings(self):
        if self.start != -1:
            print('Extreme Colorings:\n', self.colorings)

    def print_sets(self):
        print('Sums Generated:', end='')
        for n in range(self.n):
            if self.mod:
                temp = self.sets[n].head.next
                print('\n', n, ':', temp, end='')
                while temp is not None:
                    print(',', temp, end='')
                    temp = temp.next
            else:
                temp = [i+1 for i in self.sets[n].head.next]
                print('\n', n+1, ':', temp, end='')
                while temp is not None:
                    print(',', temp, end='')
                    temp = [i + 1 for i in temp.next]
        print()

    def set_time_limit(self, t):
        self.timeLimit = t

