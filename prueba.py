from smwtp import *
from functionsamples import *

from permutations import *


instance = SMWTP("instances/smwtp/n8_rdd0.4_tf0.8_seed0.txt")

pi = [2,1,4,5,3,8,7,6]

tau_1 = [2,4,5,1,3,8,7,6]
tau_2 = [2,1,4,5,8,7,3,6]

movements = generate_movements(8,3)

h1 = movements[2][0]
h2 = movements[3][1]

delta_1 = instance.evaluate(compose(pi,h2)) - instance.evaluate(pi)
delta_2 = instance.evaluate(compose(compose(pi,h1), h2)) - instance.evaluate(compose(pi,h1))

print(delta_1)
print(delta_2)

print("------------------")

print(instance.delta(pi,h2,3,3))
