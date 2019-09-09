from .LinkedLists import SetLinkedList
from .LinkedLists import ColoringLinkedList
import time, sys, warnings, multiprocessing as mp, queue, itertools, numpy as np


class _RainbowSim:
    def __init__(self, n, a, initialize, params):
        if type(n) is not int or n < 1:
            raise TypeError("Scalar n must be an integer greater than or equal to 1")
        self.n = n

        try:
            for i in a:
                if type(i) is not int:
                    raise TypeError()
        except TypeError:
            raise TypeError("Vector a[] must be a list containing only integers")
        self.a = a
        self.k = len(a)

        self.initialize = initialize
        self.params = params

        self.sets = self._generate_sets()

        self.timeLimit = 43200  # 12 hours
        self.start = time.time()

    def _generate_sets(self):
        """
        Generate set matrix for coloring checking.

        :return: Set matrix 2-D ndarray
        """
        sets = np.array([])
        for combination in itertools.combinations(list(range(self.n)), self.k):
            for permutation in itertools.permutations(combination, self.k):
                set = [self._invert(p) for p in permutation]
                if self._is_valid_set(set):
                    set_row = [0 if i in permutation else 1for i in self.n]
                    sets = np.append(sets, [set_row], axis=0)
                    break
        return sets

    def _gen_colorings(self, coloring, used, loop, queue):
        return

    def _add_set(self, set):
        """
        Add set to SetLinkedList.

        :param set: Set to be added
        :return: None
        """
        for i in set:
            self.sets[i].add_set(set)
        self.sets[self.n].add_set(set)

    def _extreme_colorings(self, quantity=-1):
        """
        Print to console the extreme colorings.

        :param quantity: Quantity of colorings to be printed (default = -1 to print all)
        :return: None
        """
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

    def _sets(self, nums=-1, invert=False):
        """
        Print to console the sets generated.

        :param nums: List of numbers whose sets will be printed (default = -1 to print all)
        :return: None
        """
        print('Sets Generated:')
        print('Index\tInverted', end='')
        if nums < 0:
            nums = list(range(self.n))
        for n in nums:
            temp = self.sets[n].head.next
            print('\n', str(n).ljust(8), self._invert(n), '\t: ', end='')
            if temp is not None:
                if invert:
                    print(list(self._invert(i) for i in temp.data), end='')
                else:
                    print(temp, end='')
                temp = temp.next
                while temp is not None:
                    if invert:
                        print(',', list(self._invert(i) for i in temp.data), end='')
                    else:
                        print(',', temp.data, end='')
                    temp = temp.next
            else:
                print(None, end='')
        print('\n')

    def _invert(self, i):
        """
        Default invert method.

        :param i: Index to be inverted
        :return: Index unchanged
        """
        return i

    def _is_valid_set(self, set):
        """
        Default valid set checker method.

        :param set: Set to be checked for validity
        :return: Boolean describing set validity
        """
        return False

    def run(self):
        """
        Find extreme colorings.

        :return:    1 if time limit WAS NOT reached
                    0 if time limit WAS reached
        """
        self.start = time.time()
        coloring = [-1 for _ in range(self.n)]
        coloring[0] = 0
        used = [0 for _ in range(self.n)]
        used[0] = 1

        self._gen_colorings(coloring, used, 1, self.queue)

        temp_colorings = []
        running = self.processes
        while running:
            try:
                while 1:
                    temp_colorings.append(self.queue.get(False))
            except queue.Empty:
                pass
            time.sleep(0.5)  # Give tasks a chance to put more data in
            if not self.queue.empty():
                continue
            running = [p for p in running if p.is_alive()]

        temp_colorings.sort()
        for data in temp_colorings:
            self.colorings.add_coloring(data[0], data[1])

        if time.time() - self.start > self.timeLimit:
            print("\nRb(" + self.equation() + ", n = " + str(self.n) + ") computation exceed time limit.")
            return None
        print("\nRb(" + self.equation() + ", n = " + str(self.n) + ") = ", str(self.colorings.maxColors + 1))
        print("Total colorings:", self.colorings.len)
        print("Time:", time.time() - self.start)
        return 1

    def _check_coloring_matrix(self, coloring_matrix):
        """
        Check coloring matrix for rainbow sets.

        :param coloring_matrix:  Coloring matrix to be checked
        :return: Boolean validity value
        """
        result = self.sets.dot(coloring_matrix)
        if np.amin([np.amax(row) for row in result]):
            return False
        return True

    def check_coloring(self, coloring):
        """
        Check coloring for rainbow sets.

        :param coloring: Coloring to be checked
        :return: Boolean validity value
        """
        coloring_matrix = []
        if self._check_coloring_matrix(coloring_matrix):
            print("VALID: Coloring", coloring, "for n =", self.n, "works! Yippee!")
            return True
        print("INVALID: Coloring", coloring, "for n =", self.n, "contains rainbow sets :(")
        return False

    def set_time_limit(self, t):
        """
        Set time limit for maximum computation time.

        :param t: Time limit in seconds
        :return: None
        """
        self.timeLimit = t

    def time_limit_reached(self):
        """
        Check whether time limit has been reached.

        :return: Boolean describing whether time limit has been reached.
        """
        # TODO bug in time_limit_reached likely due to multiprocessing
        return self.start < 0

    def print_extreme_colorings(self, quantity=-1):
        """
        Default method to print extreme colorings.

        :return: None
        """
        self._extreme_colorings(quantity)

    def print_sets(self, nums=-1):
        """
        Default method to print sets.

        :return: None
        """
        self._sets(nums, True)
