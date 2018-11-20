from .RainbowSim import RainbowSim
import warnings


class RbProductsEq(RainbowSim):
    def __init__(self, n, a, b=1, mod=False):
        warnings.warn('Potential bug in code, currently under further inspection.')

        super(RbProductsEq, self).__init__(n, a, b, mod)
        self.products = self.sets

        if self.b is 0:
            raise ValueError("Scalar b must be a nonzero integer.")

        self.generate_products()

    def generate_products(self):
        if self.mod:
            values = list(range(self.k - 1))
        else:
            values = list(range(1, self.k))
        self.recur_gen_products(self.products, self.a, self.b, values, 0)

    def recur_gen_products(self, products, a, b, values, loop):
        k = self.k - 1
        if loop == k:
            return
        if self.mod:
            stop_case = self.n - k + loop
        else:
            stop_case = self.n - k + loop + 1
        while values[loop] <= stop_case:
            self.recur_gen_products(products, a, b, values, loop + 1)
            if loop == k - 1:
                product = 1
                out = [0 for _ in range(self.k)]
                for i in range(len(values)):
                    product = product * a[i] * values[i]
                    out[i] = values[i]
                valid = True
                # TODO Determine if modulo bug exists here aswell
                product = product/(b * a[k])
                if product != int(product):
                    valid = False
                product = int(product)
                for i in range(len(values)):
                    if out[i] == product % self.n or out[i] == product:
                        valid = False
                if self.mod:
                    out[k] = product % self.n
                else:
                    if product <= self.n:
                        out[k] = product
                        for i in range(self.k):
                            out[i] = out[i] - 1
                    else:
                        valid = False
                if valid:
                    for i in range(self.k):
                        products[out[i]].add_set(out)
            values[loop] = values[loop] + 1
            for lp in range(loop + 1, k):
                values[lp] = values[lp-1] + 1
