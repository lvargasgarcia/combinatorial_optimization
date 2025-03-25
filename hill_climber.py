from permutations import *
from smwtp import *
from functionsamples import *
import time

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

def compute_scores(pi, neighborhood, objective_function, T):
    pi_neighborhood = {}
    improving_set = T()
    pi_value = objective_function(pi)
    
    for key in neighborhood.keys():
        
        pi_neighborhood[key] = {}
        
        for sigma in neighborhood[key]:

            delta = objective_function(compose(pi, sigma)) - pi_value
            pi_neighborhood[key][tuple(sigma)] = delta
            if delta < 0:
                improving_set.add((key,tuple(sigma)))

    return pi_neighborhood, improving_set

def update_scores(pi, pi_neighborhood, objective_function, improving_set, list_keys):
    pi_value = objective_function(pi)
    to_remove = set()
    
    for key in list_keys:
        for sigma in pi_neighborhood[key].keys():
            delta = objective_function(compose(pi, sigma)) - pi_value
            pi_neighborhood[key][sigma] = delta
            if delta < 0:
                improving_set.add((key,sigma))
            else:
                to_remove.add((key,sigma))
    
    for key in to_remove:
        improving_set.discard(key)




def hill_descent(k,instance, T):
    
    """
    This function returns the permutation that minimizes the value of the objective function
    """
    
    n = instance.getN()

    def objective_function(pi):
        return instance.evaluate(pi)
    
    neighborhood = generate_movements(n,k)
    permutations = list(itertools.permutations(range(1,n+1)))

    t_0 = time.time()

    l = 1

    best = None
    best_value = None

    while l < 20:

        t_0 = time.time()

        random_solution = random.choice(permutations)
        pi = list(random_solution)
        pi_neighborhood, improving_set = compute_scores(pi, neighborhood, objective_function, T)

        while len(improving_set) > 0:
            selected_move = random.choice(list(improving_set))
            pi = compose(pi, selected_move[1])
            list_keys = get_filtered_list(selected_move[0], k, n)
            update_scores(pi, pi_neighborhood, objective_function, improving_set, list_keys)
        
        if best == None or objective_function(pi) < best_value:
            best = pi
            best_value = objective_function(pi)
        
        print("---- Iteration: ", l, "Time: ", time.time() - t_0, "Best value: ", best_value)

        l += 1
        
    return best, best_value



instance = SMWTP("instances/smwtp/n10_rdd0.4_tf0.8_seed0.txt")

print(hill_descent(4,instance, set))