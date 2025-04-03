#ifndef EFFICIENT_OPERATORS_HPP
#define EFFICIENT_OPERATORS_HPP

#include <vector>
#include "smwtp.hpp"
#include "permutation_utils.hpp"
#include <unordered_set>
#include <ctime>
#include <algorithm>
#include <set>

class Pair {
    public:
        
        std::string first;
        int second;
    
        // Constructor to initialize the pair
        Pair(const std::string& f, double s) : first(f), second(s) {}
    
        bool operator<=(const Pair& other) const {
            return second <= other.second;
        }

        bool operator<(const Pair& other) const {
            return second < other.second;
        }

};

std::unordered_set<std::string> compute_scores(vector<int>& pi, std::unordered_map<int, std::unordered_map<std::string, int>>& neighborhood, SMWTP& instance, int k) {

    std::unordered_set<std::string> improving_set;

    for (auto& [position, moves] : neighborhood) {
        for (auto& [key, _] : moves) {
            auto change = instance.delta(pi, to_vec(key), position, k);
            neighborhood[position][key] = change;
            if (change < 0) {
                improving_set.insert(std::to_string(position) + ":" + key);
            }
        }
    }

    return improving_set;
}

template <typename T>
T getRandomElement(const std::unordered_set<T>& mySet) {
    if (mySet.empty()) {
        throw std::runtime_error("The unordered_set is empty");
    }

    // Seed the random number generator
    std::srand(std::time(nullptr));

    // Generate a random index
    int randomIndex = std::rand() % mySet.size();

    // Advance the iterator to the random index
    auto it = mySet.begin();
    std::advance(it, randomIndex);

    return *it;
}

std::vector<int> get_filtered_list(int x, int k, int n) {
    std::vector<int> result;

    for (int i = x - k + 1; i <= x + k - 1; ++i) {
        if (i >= 1 && i <= n - k + 1) {
            result.push_back(i);
        }
    }

    return result;
}

std::unordered_set<std::string> update_scores(vector<int>& pi, std::unordered_map<int, std::unordered_map<std::string, int>>& neighborhood, 
    std::unordered_set<std::string>& improving_set, std::vector<int> list_keys, SMWTP& instance, int k) {

    auto to_remove = std::unordered_set<std::string>();

    for(auto key: list_keys){
        for(auto & [sigma, _] : neighborhood[key]){
            auto change = instance.delta(pi, to_vec(sigma), key, k);
            if (change < 0) {
                improving_set.insert(std::to_string(key) + ":" + sigma);
            } else {
                to_remove.insert(std::to_string(key) + ":" + sigma);
            }
        }
    }

    for (auto& key : to_remove) {
        improving_set.erase(key);
    }

    return improving_set;
}

vector<int> local_search(int k, SMWTP& instance, vector<int> p) {

    int n = instance.getN();
    auto pi = p;
    auto neighborhood = generate_movements(n, k);
    auto improving_set = compute_scores(pi, neighborhood, instance, k);

    while (improving_set.size() > 0) {

        std::cout << improving_set.size() << "\n";
        
        // select a random move from the improving set
        auto selected_move = getRandomElement(improving_set);
        int position = std::stoi(selected_move.substr(0, selected_move.find(':')));
        vector<int> move = to_vec(selected_move.substr(selected_move.find(':') + 1));

        pi = compose(pi, move);
        auto list_keys = get_filtered_list(position, k, n);
        update_scores(pi, neighborhood, improving_set, list_keys, instance, k);

    }

    return pi;

}

auto compute_scores_steep(vector<int>& pi, std::unordered_map<int, std::unordered_map<std::string, int>>& neighborhood, SMWTP& instance, int k) {

    std::set<Pair> improving_set;

    for (auto& [position, moves] : neighborhood) {
        for (auto& [key, _] : moves) {
            
            auto change = instance.delta(pi, to_vec(key), position, k);
            neighborhood[position][key] = change;
            if (change < 0) {
                improving_set.insert(Pair(std::to_string(position) + ":" + key, change));
            }
        }
    }

    return improving_set;
}

void update_scores_steep(vector<int>& pi, std::unordered_map<int, std::unordered_map<std::string, int>>& neighborhood, 
    std::set<Pair>& improving_set, std::vector<int> list_keys, SMWTP& instance, int k) {


    for(auto key: list_keys){
        for(auto & [sigma, val] : neighborhood[key]){
            improving_set.erase(Pair(std::to_string(key) + ":" + sigma, val));
            auto change = instance.delta(pi, to_vec(sigma), key, k);
            neighborhood[key][sigma] = change;
            if (change < 0) {
                improving_set.insert(Pair(std::to_string(key) + ":" + sigma, change));
            }
        }
    }


}

vector<int> local_search_steep(int k, SMWTP& instance, vector<int> p) {

    int n = instance.getN();
    auto pi = p;
    auto neighborhood = generate_movements(n, k);
    auto improving_set = compute_scores_steep(pi, neighborhood, instance, k);

    while (improving_set.size() > 0) {

        std::cout << improving_set.size() << "\n";
        
        auto selected_move = improving_set.begin()->first;
        int position = std::stoi(selected_move.substr(0, selected_move.find(':')));
        vector<int> move = to_vec(selected_move.substr(selected_move.find(':') + 1));

        pi = compose(pi, move);
        auto list_keys = get_filtered_list(position, k, n);
        update_scores_steep(pi, neighborhood, improving_set, list_keys, instance, k);

    }

    return pi;

}

std::vector<int> partition_crossover(const std::vector<int>& sigma_1, const std::vector<int>& sigma_2, 
                                     SMWTP& instance) {
    std::vector<int> child = sigma_1; 
    std::vector<int> pi = compose(inverse(sigma_1), sigma_2); 
    int i = 0;
    int n = sigma_1.size();

    while (i < n) {
        std::vector<int> h(n, 0);
        for (int k = 0; k < n; ++k) {
            h[k] = k + 1;
        }
        int l = i;
        h[l] = pi[l];
        int j = h[l] - 1;

        while (l < j) {
            l += 1;
            h[l] = pi[l];
            j = std::max(j, h[l] - 1);
        }

        double delta_1 = instance.delta(sigma_1, h, i + 1, j - i + 1);

        if (delta_1 < 0) {
            child = compose(child, h);
        }

        i = l + 1; 
    }

    return child;
}

std::vector<int> perturbation_function(const std::vector<int>& p) {
    
    int n = p.size();
    std::srand(std::time(nullptr)); // Seed the random number generator

    int r = std::rand() % n + 1; 
    int total_elems = r;

    std::unordered_set<int> first_set(p.begin(), p.begin() + total_elems);
    std::vector<int> current_permutation = random_permutation(first_set);

    while (total_elems < n) {
        r = std::rand() % (n - total_elems) + 1; 
        std::unordered_set<int> next_set(p.begin() + total_elems, p.begin() + total_elems + r);
        std::vector<int> next_permutation = random_permutation(next_set);

        current_permutation.insert(current_permutation.end(), next_permutation.begin(), next_permutation.end());
        total_elems += r;
    }

    return current_permutation;
}

std::pair<std::vector<int>, int> DRILS(std::string& file, int neighborhood_size, long time_interval_drils, bool steepest_descent){

    auto instance = SMWTP(file);

    long t_0 = std::time(nullptr);

    auto id_set = std::unordered_set<int>();
    for (int i = 1; i <= instance.getN(); ++i) {
        id_set.insert(i);
    }

    auto pi = random_permutation(id_set);

    auto current = steepest_descent ? local_search_steep(neighborhood_size, instance, pi) : local_search(neighborhood_size, instance, pi);

    auto best = current;
    auto best_value = instance.evaluate(best);

    while (std::time(nullptr) - t_0 < time_interval_drils) {

        auto next = steepest_descent ? local_search_steep(neighborhood_size, instance, perturbation_function(current)) : local_search(neighborhood_size, instance, perturbation_function(current));
        auto child = partition_crossover(current, next, instance);

        if (child == current || child == next){
            current = next;
        }else{
            current = steepest_descent ? local_search_steep(neighborhood_size, instance, child) : local_search(neighborhood_size, instance, child);
        }

        auto current_value = instance.evaluate(current);
        if (current_value < best_value) {
            best = current;
            best_value = current_value;
        }

        std::cout << "Current value: " << current_value << "\n";
        std::cout << "Best value: " << best_value << "\n";
        std::cout << "-------------------------\n";

    }

    return std::make_pair(best, best_value);
}

#endif