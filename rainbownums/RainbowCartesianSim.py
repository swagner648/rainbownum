from .RainbowSim import RainbowSim


class RbCartesianEq(RainbowSim):
    def __init__(self, n, a, b=0, mod=False):
        super(RbCartesianEq, self).__init__(n, a, b, mod)
        self.products = self.sets
        self.generate_products()

    def generate_products(self):
        if self.mod:
            values = list(range(self.k - 1))
        else:
            values = list(range(1, self.k))
        self.recur_gen_products(self.products, self.a, self.b, values, 0)

    def recur_gen_products(self, sums, a, b, values, loop):
        print(self.products)
        return True
