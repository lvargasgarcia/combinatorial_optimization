from argparse import ArgumentParser
import os
from efficient_operators import *
from smwtp import SMWTP
import json
from itertools import product
import re

neighborhood_sizes = [2,3,4,5,6]

percentage_components_to_perturb = [0.05, 0.1, 0.15, 0.2]

percentage_perturbation_ranges = [0.1, 0.2, 0.3, 0.4]



def analysis(instance, neighborhood_size, percentage_components_to_perturb, percentage_perturbation_range, time_to_run, real_optimal_value, output_file):
    """
    This function runs the DRILS algorithm with the given parameters and returns the best permutation and its value.
    """
    components_to_perturb = int(percentage_components_to_perturb * instance.getN())
    perturbation_range = int(percentage_perturbation_range * instance.getN())

    pi, pi_value = DRILS(instance, local_search, partition_crossover, perturbation_function, neighborhood_size, set, time_to_run, components_to_perturb, perturbation_range)

    data = {}

    data["n"] = instance.getN()
    data["neighborhood_size"] = neighborhood_size
    data["percentage_components_to_perturb"] = percentage_components_to_perturb
    data["percentage_perturbation_range"] = percentage_perturbation_range
    data["time_to_run"] = time_to_run
    data["real_optimal_value"] = real_optimal_value
    data["best_value"] = pi_value
    data["best_permutation"] = pi
    data["distance_to_optimal_value"] = pi_value - real_optimal_value
    data["performance"] = real_optimal_value / pi_value


    json.dump(data, open(output_file, "w"), indent=4)


from multiprocessing import Pool

def process_instance(args):
    """Function to process a single instance in parallel."""
    
    neighborhood_size, percentage_components_to_perturb, percentage_perturbation_range, file, args, optimal_values = args

    regex = r".*_([0-9]+)_b.txt"
    group = re.match(regex, file).group(1)
        
    if group is None:
        print("Error:", file)
        raise ValueError("Error: group is None")
        
    number = int(group)

    output_file = f"./results/DRILS_{number}_{neighborhood_size}_{percentage_components_to_perturb}_{percentage_perturbation_range}_{args.n}.json"

    # Check if the file exists
    if not os.path.exists(output_file):

        real_optimal_value = optimal_values[number - 1]
        instance = SMWTP("./instances_opt/instances/" + str(args.n) + "/" + file)

        if real_optimal_value == 0:
            
            old_f = instance.evaluate

            def new_f(p):
                return old_f(p) + 1

            instance.evaluate = new_f
            real_optimal_value = 1


        analysis(instance, neighborhood_size, percentage_components_to_perturb, percentage_perturbation_range, args.time_to_run, real_optimal_value, output_file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--n", type=int)
    parser.add_argument("--time_to_run", type=int)

    args = parser.parse_args()

    optima_file = "./instances_opt/instances/opt" + str(args.n) + ".txt"
    optimal_values = []

    # mkdir -p results
    os.makedirs("./results", exist_ok=True)

    with open(optima_file, "r") as f:
        for i, line in enumerate(f):
            optimal_values.append(int(line.strip()))

    # Prepare arguments for parallel processing
    tasks = []
    for file in os.listdir("./instances_opt/instances/" + str(args.n)):
        for (neighborhood_size, percentage_component_to_perturb, percentage_perturbation_range) in product(neighborhood_sizes, percentage_components_to_perturb, percentage_perturbation_ranges):
            tasks.append((neighborhood_size, percentage_component_to_perturb, percentage_perturbation_range, file, args, optimal_values))

    # Use multiprocessing to parallelize the tasks
    with Pool(processes=10) as pool:
        pool.map(process_instance, tasks)

          


