from rainbownums import *

# a_1(x_1) + a_2(x_2) + ... + a_i(x_i) = b
a = [1, 1, -1]  # coefficients a_i
b = 0  # value for b (default 0 for sums and 1 for products))
mod = False  # whether calculating for [n] or Zn (default False)
for n in range(3, 6):
    # set up solver
    eq = RbSumsEq(n, a, b, mod)

    # eq.check_sums()

    # time limit for solving (default is 43200 sec (12 hours))
    eq.set_time_limit(1)

    # stops checking larger n when time limit is exceeded
    if eq.run() is None:
        break

    # print colorings with most colors
    eq.print_extreme_colorings()

    # print the sets generated based on a[] and b (sums in this case)
    eq.print_sets()

# Another format for computation
n = 1
a = [1, 1, -2]
b = 0
mod = True
while True:
    eq = RbSumsEq(n, a, b, mod)
    eq.set_time_limit(1)
    eq.run()
    if eq.time_limit_reached():
        break
    eq.print_extreme_colorings(1)
    eq.print_sets()
    n += 1

# Taking advantage of default settings for b and mod
a = [1, 1, 1, -1]
eq = RbSumsEq(11, a)
eq.run()
eq.print_extreme_colorings(3)
eq.print_sets([0, 1, 2])
