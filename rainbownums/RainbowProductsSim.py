from .RainbowSim import RainbowSim


class RbProductsEq(RainbowSim):
    def __init__(self, k, n, mod):
        self.mod = mod
        self.products = [0 for _ in range(n)]
        super(RbProductsEq, self).__init__(k, n, self.products)
        self.generate_products()

    def generate_products(self):
        if self.mod:
            values = list(range(self.k))
        else:
            values = list(range(1, self.k + 1))
        self.recur_gen_products(self.products, values, 0)

    def recur_gen_products(self, products, values, loop):
        k = self.k - 1
        if loop == k:
            return
        while values[loop] <= self.n - k + loop + 1:
            self.recur_gen_products(products, values, loop + 1)
            if loop == k - 1:
                product = 1
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    product = product * values[i]
                    out[i] = values[i]
                unique = True
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
