from smwtp import *
from functionsamples import *
from efficient_operators import *

from permutations import *
from drils import DRILS

best_pc, best_valuec = DRILS("instances_opt/instances/1000/n1000_20_b.txt", 5, 1000000000000000)

print(best_pc, best_valuec)


# instance = SMWTP()

# for pi in itertools.permutations(range(1, 6)):
#     print(f"{pi}: {instance.evaluate(pi)}")



# pi_1 = [2, 1, 4, 5, 3]
# pi_2 = [1, 3, 4, 2, 5]

# print(instance.delta(pi_1, pi_2, 2, 3))

# pi = [2,1,4,5,3,8,7,6]

# tau_1 = [2,4,5,1,3,8,7,6]
# tau_2 = [2,1,4,5,8,7,3,6]

# movements = generate_movements(8,3)

# h1 = movements[2][0]
# h2 = movements[3][1]

# delta_1 = instance.evaluate(compose(pi,h2)) - instance.evaluate(pi)
# delta_2 = instance.evaluate(compose(compose(pi,h1), h2)) - instance.evaluate(compose(pi,h1))

# print(delta_1)
# print(delta_2)

# print("------------------")

# print(instance.delta(pi,h2,3,3))
