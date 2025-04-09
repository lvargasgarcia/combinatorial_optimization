#ifndef LOCAL_SEARCH_HPP
#define LOCAL_SEARCH_HPP

#include "Neighborhood.hpp"
#include "smwtp.hpp"
#include <memory>
#include <algorithm>
#include <random>
#include <ctime>

std::vector<int> get_filtered_list(const int x, const int k, const int n) {

    int start = x - k + 1;
    int end = x + k - 1;

    int first = std::max(0, start);
    int last = std::min(n - k, end);

    int result_size = std::max(0, last - first + 1);

    auto result = std::vector<int>(result_size);

    for (int i = 0, val = first; val <= last; ++i, ++val) {
        result[i] = val;
    }

    return result;
}

std::string to_string(const permutation_t& perm, int n) {
    std::string result = "[";
    for (int i = 0; i < n; ++i) {
        result += std::to_string(perm[i]);
        if (i < n - 1) {
            result += ", ";
        }
    }
    result += "]";
    return result;
}

void compute_scores(const permutation_t& pi, Neighborhood& neighborhood, SMWTP& instance, int k) {
    
    auto identity = permutation_t(pi.size());
    for (size_t i = 0; i < pi.size(); i++) {
        identity[i] = i;
    }
    
    for (size_t i = 0; i < neighborhood.categories; i++) {
        for(size_t j = 0; j < neighborhood.perms_count; j++){
            
            auto current = i*neighborhood.perms_count + j;
            
            //Compute initial common tardiness
            
            long common_tardiness = 0;
            int l = 0;
            auto move = neighborhood.perms_set[current];
            
            while(l < i){
                common_tardiness += instance.times[pi[l]];
                l++;
            }

            auto change = instance.delta(identity, pi, move, i, k, common_tardiness);

            // auto change2 = -instance.evaluate(pi) + instance.evaluate(compose(pi, move, instance.getN()));

            // if(change != change2){
            //     std::cout << "Error: " << change << " != " << change2 << "\n";
            //     change2 = -instance.evaluate(pi) + instance.evaluate(compose(pi, move, instance.getN()));
            //     change = instance.delta(identity, pi, move, i, k, common_tardiness);
            // }

            neighborhood.scores[current] = change;
            neighborhood.common_tardiness_set[current] = common_tardiness;

            if (change < 0) {
                
                neighborhood.insert_move(i, current);
                
            }

        }
    }

}

void update_scores(permutation_t& pi, Neighborhood& neighborhood, std::vector<int> list_keys, SMWTP& instance, int k, int selected_move_position,
                    int selected_move_index) {                              
    
        auto selected_move = neighborhood.perms_set[selected_move_index];
        
        for(int i: list_keys){
            for(int j = 0; j < neighborhood.perms_count; j++){
                
                auto current = i*neighborhood.perms_count + j;
                auto move = neighborhood.perms_set[current];

                //update common tardiness
                auto common_tardiness = neighborhood.common_tardiness_set[current];
                for(int l = selected_move_position; l < i; l++){
                    common_tardiness = common_tardiness - instance.times[pi[l]] + instance.times[pi[selected_move[move[l]]]];
                }
                neighborhood.common_tardiness_set[current] = common_tardiness;

                auto change = instance.delta(pi, selected_move, move, i, k, common_tardiness);

                // auto change2 = -instance.evaluate(compose(pi, selected_move, instance.getN())) + instance.evaluate(compose(compose(pi, selected_move, instance.getN()), move, instance.getN()));

                // if(change != change2){
                //     std::cout << "Error: " << change << " != " << change2 << "\n";
                //     auto change2 = -instance.evaluate(compose(pi, selected_move, instance.getN())) + instance.evaluate(compose(compose(pi, selected_move, instance.getN()), move, instance.getN()));
                //     change = instance.delta(pi, selected_move, move, i, k, common_tardiness);
                // }

                neighborhood.scores[current] = change;

                if (change < 0) {
                    
                    neighborhood.insert_move(i,current);
                
                } else {
                    
                    neighborhood.remove_move(current);
                
                }
            }
        }

        auto aux = std::make_unique<int[]>(k);

        for(int i = selected_move_position; i < selected_move_position + k; i++){
            aux[i - selected_move_position] = pi[selected_move[i]];
        }

        for(int i = selected_move_position; i < selected_move_position + k; i++){
            pi[i] = aux[i - selected_move_position];
        }

}

std::pair<permutation_t,long> local_search(int k, SMWTP& instance, const permutation_t& pi){

    int n = instance.getN();

    permutation_t p = permutation_t(n);
    std::copy(pi.begin(), pi.end(), p.begin());

    long current_fit = instance.evaluate(p);

    // std::cout << "Initial permutation: " << to_string(p, n) << "\n";

    // std::cout << "Initial fitness: " << current_fit << "\n";

    auto neighborhood = Neighborhood(n,k);

    // std::cout << neighborhood.to_string() << "\n";

    compute_scores(p, neighborhood, instance, k);

    while (neighborhood.improving_moves_set.size() > 0) {

        // std::cout << neighborhood.improving_moves_set.size() << "\n";
        
        auto selected_move = neighborhood.select_improving_move();
        current_fit += neighborhood.scores[selected_move.second];

        // std::cout << "New fitness: " << current_fit << "\n";

        auto list_keys = get_filtered_list(selected_move.first, k, n);
        update_scores(p, neighborhood, list_keys, instance, k, selected_move.first, selected_move.second);

        // std::cout << "New permutation: " << to_string(p, n) << "\n";   

    }

    return std::make_pair(p, current_fit);

}

#endif 

