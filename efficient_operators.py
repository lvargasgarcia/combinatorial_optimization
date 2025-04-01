from permutations import *
from smwtp import *
from functionsamples import *
import time
from collections import deque


def get_filtered_list(x, k, n):
    return [i for i in range(x - k + 1, x + k - 1) if 1 <= i <= n - k + 1]

class SetWithMin:
    def __init__(self):
        self.set = set()
        self.min = None
    
    def add(self, element):
        self.set.add(element)
        if self.min == None or element[1] < self.min[1]:
            self.min = element
    
    def discard(self, element):
        self.set.discard(element)
        if element == self.min:
            self.min = None
            for e in self.set:
                if self.min == None or e[1] < self.min[1]:
                    self.min = e
    
    def __len__(self):
        return len(self.set)
    
    def __list__(self):
        return list(self.set)
    
    def __iter__(self):
        return iter(self.set)

def compute_scores(pi, neighborhood, T, delta, k):
    
    improving_set = T()
    
    for key in neighborhood.keys():
        for sigma in neighborhood[key]:
            change = delta(pi, sigma, key, k)
            neighborhood[key][tuple(sigma)] = change
            if change < 0:
                improving_set.add((key,tuple(sigma)))

    return improving_set

def update_scores(pi, neighborhood, improving_set, list_keys, delta, k):

    to_remove = set()
    
    for key in list_keys:
        for sigma in neighborhood[key].keys():
            change = delta(pi, sigma, key, k)
            neighborhood[key][sigma] = change
            if change < 0:
                improving_set.add((key,sigma))
            else:
                to_remove.add((key,sigma))
    
    for key in to_remove:
        improving_set.discard(key)




def local_search(k,instance, T, p):
    
    """
    This function returns the permutation that minimizes the value of the objective function
    """
    pi = p[:]
    n = instance.getN()
    delta = instance.delta
    
    neighborhood = generate_movements(n,k)
    improving_set = compute_scores(pi, neighborhood, T, delta, k)

    while len(improving_set) > 0:
        selected_move = random.choice(list(improving_set))
        pi = compose(pi, selected_move[1])
        list_keys = get_filtered_list(selected_move[0], k, n)
        update_scores(pi, neighborhood, improving_set, list_keys, delta, k)
        # print(len(improving_set))
                
    return pi


def partition_crossover(sigma_1, sigma_2, delta):
    child = sigma_1[:]
    moves = []
    pi = compose(inverse(sigma_1), sigma_2)
    i = 0
    n = len(sigma_1)
    
    while i < n:
        h = list(range(1,n+1))
        l = i
        h[l] = pi[l]
        j = h[l] - 1
        
        while l < j:
            l += 1
            h[l] = pi[l]
            j = max(j, h[l] - 1)
        
        moves.append(h[:])
        delta_1 = delta(sigma_1, h, i + 1, j - i + 1)
        # delta_2 = f(compose(sigma_1,h)) - f(sigma_1)

        # if delta_1 != delta_2:
        #     raise("Delta 1 and Delta 2 are not equal")

        if delta_1 < 0:
            child = compose(child, h)

        i = l + 1
    
    return child

def perturbation_function(p, k, r):
    pi = p[:]
    for _ in range(k):
        i = random.randint(0, len(pi)-1)
        t = random.randint(-r, r)
        if t != 0 and i + t < len(pi) and i + t >= 0:
            pi[i], pi[i+t] = pi[i+t], pi[i]
    return pi


def DRILS(instance, local_search, px, perturbation_function, neighborhood_size, T, time_interval_drils, components_to_perturb, perturbation_range):

    delta = instance.delta

    def objective_function(pi):
        return instance.evaluate(pi)
    
    current = local_search(neighborhood_size, instance, T, random_permutation(instance.getN()))
    t_0 = time.time()

    best = current
    best_value = objective_function(current)

    while time.time() - t_0 < time_interval_drils:
        
        next = local_search(neighborhood_size, instance, T, perturbation_function(current, components_to_perturb, perturbation_range))
        child = px(current, next, delta)
        
        if child == current or child == next:
            current = next
        else:
            current = local_search(neighborhood_size, instance, T, child)

        current_value = objective_function(current)
        if current_value < best_value:
            best_value = current_value
            best = current
    
        print("Current value: ", current_value)
    
    return best, best_value

def HIRELS(instance, local_search, px, neighborhood_size, T, time_interval_hierls):

    stack = deque()
    t_0 = time.time()

    best, best_value = None, None

    while time.time() - t_0 < time_interval_hierls:

        current = local_search(neighborhood_size, instance, T, random_permutation(instance.getN()))
        current_level = 0

        if len(stack) == 0 or stack[-1][1] > 0:
            stack.append((current, current_level))
        else:
            
            pxSuccess = True
            
            while len(stack) > 0 and pxSuccess and stack[-1][1] == current_level:
                top = stack.pop()
                child = px(current, top[0], instance.delta)
                pxSuccess = child != current and child != top[0]
                if pxSuccess:
                    current = local_search(neighborhood_size, instance, T, child)
                    current_level += 1
            
            if pxSuccess:
                stack.append((current, current_level))
        
        current_value = instance.evaluate(current)
        if best is None or current_value < best_value:
            best = current
            best_value = current_value
    
    return best, best_value
            




# instance = SMWTP("instances_opt/instances/100/n100_1_b.txt")

# pi, pi_value = HIRELS(instance, local_search, partition_crossover, 3, set, 100000000)

# # instance = SMWTP("instances/smwtp/n10_rdd0.4_tf0.8_seed2.txt")

# # print(local_search(8,instance, set, 400))

# pi, pi_value = DRILS(instance, local_search, partition_crossover, perturbation_function, 3, set, 60, int(0.15*instance.getN()), int(0.25*instance.getN()))

# print("Final value: ", pi_value)
# print("Final permutation: ", pi)

# for _ in range(10000000):
#     sigma_1 = random_permutation(instance.getN())
#     sigma_2 = random_permutation(instance.getN())
#     child = partition_crossover(sigma_1, sigma_2, instance.delta)

#     if instance.evaluate(child) > instance.evaluate(sigma_1) or instance.evaluate(child) > instance.evaluate(sigma_2):
#         print("Error: child is not better than parents")
#         break
#     else:
#         print("Child is better than parents")


