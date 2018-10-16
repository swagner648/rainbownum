from .RainbowSim import RainbowSim


class RbSumsEq(RainbowSim):
    def __init__(self, k, n, mod):
        self.mod = mod
        self.sums = [0 for _ in range(n)]
        super(RbSumsEq, self).__init__(k, n , self.sums)
        self.generate_sums()

    def generate_sums(self):
        if self.mod:
            values = list(range(self.k - 1))
        else:
            values = list(range(1, self.k))
        self.recur_gen_sums(self.sums, values, 0)

    def recur_gen_sums(self, sums, values, loop):
        k = self.k - 1
        if loop == k:
            return
        if self.mod:
            stop_case = self.n - k + loop
        else:
            stop_case = self.n - k + loop + 1
        while values[loop] <= stop_case:
            self.recur_gen_sums(sums, values, loop + 1)
            if loop == k - 1:
                sum = 0
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    sum = sum + values[i]
                    out[i] = values[i]
                unique = True
                for i in range(len(values)):
                    if out[i] == sum % self.n or out[i] == sum:
                        unique = False
                if self.mod:
                    out[k] = sum % self.n
                else:
                    if sum <= self.n:
                        out[k] = sum
                        for i in range(self.k):
                            out[i] = out[i] - 1
                    else:
                        unique = False
                if unique:
                    for i in range(self.k):
                        sums[out[i]].add_set(out)
            values[loop] = values[loop] + 1
            for lp in range(loop + 1, k):
                values[lp] = values[lp-1] + 1