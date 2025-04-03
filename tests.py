from argparse import ArgumentParser
import os
from efficient_operators import *
from smwtp import SMWTP
import json
from itertools import product
import re
from drils import DRILS

def analysis(prob, instance, neighborhood_size, time_to_run, real_optimal_value, output_file):
    """
    This function runs the DRILS algorithm with the given parameters and returns the best permutation and its value.
    """

    pi, pi_value = DRILS(instance, neighborhood_size, time_to_run)

    data = {}

    data["n"] = prob.getN()
    data["neighborhood_size"] = neighborhood_size
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
    
    neighborhood_size, time_to_run, file, args, optimal_values = args

    regex = r".*_([0-9]+)_b.txt"
    group = re.match(regex, file).group(1)
        
    if group is None:
        print("Error:", file)
        raise ValueError("Error: group is None")
        
    number = int(group)

    output_file = f"./results/" + str(args.n) + f"/DRILS_{number}_{neighborhood_size}_{time_to_run}_{args.n}.json"

    # Check if the file exists
    if not os.path.exists(output_file):

        real_optimal_value = optimal_values[number - 1]
        instance = "./instances_opt/instances/" + str(args.n) + "/" + file
        prob = SMWTP(instance)

        if real_optimal_value == 0:

            old_f = prob.evaluate

            def new_f(p):
                return old_f(p) + 1

            prob.evaluate = new_f
            real_optimal_value = 1


        analysis(prob, instance, neighborhood_size, time_to_run, real_optimal_value, output_file)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--n", type=int)
    parser.add_argument("--processes", type=int, default=12)

    args = parser.parse_args()

    neighborhood_sizes = [2,3,4,5,6]
    times_to_run = [5, 10, 15, 20, 40, 60] if args.n == 40 else [60, 120, 180, 240]

    # args.n = 40

    optima_file = "./instances_opt/instances/opt" + str(args.n) + ".txt"
    optimal_values = []

    # mkdir -p results
    os.makedirs("./results/" + str(args.n) + "/", exist_ok=True)

    with open(optima_file, "r") as f:
        for i, line in enumerate(f):
            optimal_values.append(int(line.strip()))

    # Prepare arguments for parallel processing
    tasks = []
    for file in os.listdir("./instances_opt/instances/" + str(args.n)):
        for (neighborhood_size, time_to_run) in product(neighborhood_sizes, times_to_run):
            tasks.append((neighborhood_size, time_to_run, file, args, optimal_values))

    # Use multiprocessing to parallelize the tasks
    with Pool(processes=args.processes) as pool:
        pool.map(process_instance, tasks)

          


