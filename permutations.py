import itertools
import random
import math


def compose(p,q):
    return [p[q[i]-1] for i in range(len(p))]

def inverse(p):
    resp = [0 for _ in range(len(p))]
    for i in range(len(p)):
        resp[p[i]-1] = i + 1
    return resp

def random_permutation(elements):
    pi = []
    n = len(elements)
    for i in range(n):
        el = random.choice(list(elements))
        pi.append(el)
        elements.remove(el)
    return pi

def permutations_set(n, pos, k):
    """
    This functions returns the list of k!
    permutations that help obtaining the list
    of permutations that result from mixing the elements
    of the pos-th set of k consecutive numbers in any 
    permutation pi of Sn
    """
    perms = {}
    taus = list(itertools.permutations(range(1, k+1)))[1:]

    move_set_beginning = [i for i in range(pos, pos+k)] + [i for i in range(1,pos)] + [i for i in range(pos+k, n+1)]
    move_set_end = inverse(move_set_beginning)

    for tau in taus:
        perms[tuple(compose(move_set_beginning, compose(list(tau) + [i for i in range(k+1,n+1)], move_set_end)))] = 0

    return perms


def generate_movements(n,k):
    """
    This function generates the movements of the every set of k consecutive numbers
    """
    resp = {}
    for i in range(1, n-k+2):
        resp[i] = permutations_set(n, i, k)
    return resp


#prueba

# sigmas = permutations_set(5, 2, 3)

# pi = [2,1,4,5,3]

# neighborhood = generate_movements(5,3)

# for i in range(1, 4):
#     print(f"-------------------- {i} -------------------")
#     N = neighborhood[i]
#     for sigma in N:
#         print(compose(pi, sigma))
#    print("--------------------")




