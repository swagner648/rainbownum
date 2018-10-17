from .RainbowSim import RainbowSim


class RbProductsEq(RainbowSim):
    def __init__(self, k, n, a, b, mod):
        super(RbSumsEq, self).__init__(k, n, a, b)
        self.products = self.sets

        if self.b is 0:
            raise ValueError("Scalar b must be a nonzero integer.")

        if type(mod) is not bool:
            raise TypeError("Boolean mod must be either", True, "for Zn or", False, "for [n].")
        self.mod = mod

        self.generate_products()

    def generate_products(self):
        if self.mod:
            values = list(range(self.k - 1))
        else:
            values = list(range(1, self.k))
        self.recur_gen_products(self.products, values, 0)

    def recur_gen_products(self, products, a, b, values, loop):
        k = self.k - 1
        if loop == k:
            return
        if self.mod:
            stop_case = self.n - k + loop
        else:
            stop_case = self.n - k + loop + 1
        while values[loop] <= stop_case:
            self.recur_gen_products(products, values, loop + 1)
            if loop == k - 1:
                product = 1
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    product = product * values[i]
                    out[i] = values[i]
                unique = True
                product = int(b/(a[k]*products))
                for i in range(len(values)):
                    if out[i] == product % self.n or out[i] == product:
                        unique = False
                if self.mod:
                    out[k] = product % self.n
                else:
                    if product <= self.n:
                        out[k] = product
                        for i in range(self.k):
                            out[i] = out[i] - 1
                    else:
                        unique = False
                if unique:
                    for i in range(self.k):
                        products[out[i]].add_set(out)
            values[loop] = values[loop] + 1
            for lp in range(loop + 1, k):
                values[lp] = values[lp-1] + 1
