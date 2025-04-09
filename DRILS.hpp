#ifndef DRILS_HPP
#define DRILS_HPP

#include "Neighborhood.hpp"
#include "smwtp.hpp"
#include <memory>
#include <algorithm>
#include <random>
#include <ctime>
#include "local_search.hpp"



permutation_t partition_crossover(const permutation_t& sigma_1, const permutation_t& sigma_2, SMWTP& instance) {

    int n = sigma_1.size();
    std::vector<int> child = sigma_1;
    std::vector<int> pi = compose(inverse(sigma_1, n), sigma_2, n);

    int i = 0;
    long common_tardiness = 0;

    permutation_t identity = permutation_t(n);

    for (int j = 0; j < n; ++j) {
        identity[j] = j;
    }

    while (i < n) {

        permutation_t h(n, 0);

        for (int k = 0; k < n; ++k) {
            h[k] = k;
        }

        int l = i;
        int initial_pos = l;

        long aux_common_tardiness = instance.times[sigma_1[l]];

        h[l] = pi[l];
        int j = h[l];

        while (l < j) {
            l += 1;
            aux_common_tardiness += instance.times[sigma_1[l]];
            h[l] = pi[l];
            j = std::max(j, h[l]);
        }

        int final_pos = l;
        int incr = final_pos - initial_pos;

        double delta_1 = instance.delta(identity, sigma_1, h, initial_pos, incr + 1, common_tardiness);
        common_tardiness += aux_common_tardiness;

        double delta_2 = instance.evaluate(compose(sigma_1, h, n)) - instance.evaluate(sigma_1);

        if(delta_1 != delta_2){
            std::cout << "Error: " << delta_1 << " != " << delta_2 << "\n";
            delta_2 = instance.evaluate(compose(sigma_1, h, n)) - instance.evaluate(sigma_1);
            delta_1 = instance.delta(identity, sigma_1, h, initial_pos, incr, common_tardiness);
        }

        if (delta_1 < 0) {

            permutation_t aux(incr + 1);

            for(int k = initial_pos; k <= final_pos; k++){
                aux[k - initial_pos] = sigma_1[h[k]];
            }

            for(int k = initial_pos; k <= final_pos; k++){
                child[k] = aux[k - initial_pos];
            }

        }

        i = l + 1;
    }

    return child;
}

permutation_t random_permutation(const permutation_t& elems, std::mt19937& gen) {
    permutation_t vec(elems.begin(), elems.end());
    std::shuffle(vec.begin(), vec.end(), gen);
    return vec;
}

permutation_t perturbation_function(const permutation_t& p, std::mt19937& gen) {

    int n = p.size();
    std::uniform_int_distribution<> dist;

    int r = std::uniform_int_distribution<>(1, n)(gen);
    int total_elems = r;

    permutation_t first_chunk(p.begin(), p.begin() + total_elems);
    permutation_t current_permutation = random_permutation(first_chunk, gen);

    while (total_elems < n) {
        int remaining = n - total_elems;
        r = std::uniform_int_distribution<>(1, remaining)(gen);

        permutation_t next_chunk(p.begin() + total_elems, p.begin() + total_elems + r);
        permutation_t next_permutation = random_permutation(next_chunk, gen);

        current_permutation.insert(current_permutation.end(), next_permutation.begin(), next_permutation.end());
        total_elems += r;
    }

    return current_permutation;
}

std::vector<std::pair<long, long>> DRILS(SMWTP& instance, int neighborhood_size, long time_interval_drils){

    long t_0 = std::time(nullptr);

    auto resp = std::vector<std::pair<time_t, long>>();

    int n = instance.getN();

    auto id_perm = permutation_t(n);

    for (int i = 0; i < n; ++i) {
        id_perm[i] = i;
    }

    auto device = std::mt19937();

    auto pi = random_permutation(id_perm, device);

    auto current = local_search(neighborhood_size, instance, pi);

    auto best = current.first;
    auto best_value = current.second;
    resp.push_back(std::make_pair(std::time(nullptr) - t_0, current.second));

    while (std::time(nullptr) - t_0 < time_interval_drils) {

        auto next = local_search(neighborhood_size, instance, perturbation_function(current.first, device));
        auto child = partition_crossover(current.first, next.first, instance);

        if (child == current.first || child == next.first){
            current = next;
        }else{
            current = local_search(neighborhood_size, instance, child);
        }

        auto current_value = current.second;
        if (current_value < best_value) {
            best = current.first;
            best_value = current_value;
            resp.push_back(std::make_pair(std::time(nullptr) - t_0, best_value));
        }

        // std::cout << "Current value: " << current_value << "\n";
        // std::cout << "Best value: " << best_value << "\n";
        // std::cout << "-------------------------\n";

    }

    return resp;
}

#endif