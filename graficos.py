import os
import re
import json
from collections import defaultdict

def select_parameters(n):
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for file in os.listdir("./results/"):
        
        regex = r"DRILS_([0-9]+(?:\.[0-9]*)?)_([0-9]+(?:\.[0-9]*)?)_([0-9]+(?:\.[0-9]*)?)_([0-9]+(?:\.[0-9]*)?)_([0-9]+(?:\.[0-9]*)?)\.json"
        group = re.match(regex, file)

        if not group:
            continue

        dict_data = json.load(open("./results/" + file))

        if n != int(group.group(5)):
            continue

        neighborhood_size = int(group.group(2))
        percentage_components_to_perturb = float(group.group(3))
        percentage_perturbation_range = float(group.group(4))

        performance = dict_data["performance"] if dict_data["performance"] != 0 else 1
        data[neighborhood_size][percentage_components_to_perturb][percentage_perturbation_range].append(performance)

    # Calculate means and save them
    means = defaultdict(lambda: defaultdict(dict))
    for neighborhood_size, perturb_data in data.items():
        for percentage_components_to_perturb, range_data in perturb_data.items():
            for percentage_perturbation_range, performances in range_data.items():
                mean_performance = sum(performances) / len(performances)
                means[neighborhood_size][percentage_components_to_perturb][percentage_perturbation_range] = mean_performance

    # Select the tuple of best parameters

    best_params = None
    best_performance = 0
    for neighborhood_size, perturb_data in means.items():
        for percentage_components_to_perturb, range_data in perturb_data.items():
            for percentage_perturbation_range, performance in range_data.items():
                if performance > best_performance:
                    best_performance = performance
                    best_params = (neighborhood_size, percentage_components_to_perturb, percentage_perturbation_range)
    
    print(f"Best parameters for n = {n}: {best_params} with performance {best_performance}")

    return best_params, data[best_params[0]][best_params[1]][best_params[2]]


# Example usage
if __name__ == "__main__":
    select_parameters(40)





