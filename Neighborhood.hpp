#ifndef NEIGHBORHOOD_HPP
#define NEIGHBORHOOD_HPP

#include <memory>
#include <vector>
#include <algorithm> // Required for std::next_permutation
#include <string>

using permutation_t = std::vector<int>;
using perms_set_t = std::vector<permutation_t>;

long factorial (int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

permutation_t compose(const permutation_t& a, const permutation_t& b, int n) {
    permutation_t result(n);
    for (int i = 0; i < n; ++i) {
        result[i] = a[b[i]];
    }
    return result;
}

permutation_t inverse(const permutation_t& a, int n) {
    permutation_t result(n);
    for (int i = 0; i < n; ++i) {
        result[a[i]] = i;
    }
    return result;
}

std::vector<std::vector<int>> permutations(int n, int initial_position, int k) {
    
    std::vector<std::vector<int>> result;
    std::vector<int> perm(n);
    
    for (int i = 0; i < n; ++i) {
        perm[i] = i;
    }

    std::next_permutation(perm.begin() + initial_position, perm.begin() + initial_position + k);

    do {
        std::vector<int> new_perm(n);
        std::copy(perm.begin(), perm.end(), new_perm.begin());
        result.push_back(new_perm);
    } while(std::next_permutation(perm.begin() + initial_position, perm.begin() + initial_position + k));


    return result;
}

void generate_permutations_set(int n, int position, int k, perms_set_t& perms_set, long perms_count) {
        
    auto perms = permutations(n,position,k);
    
    for(size_t j = 0; j < perms_count; j++){
        
        perms_set[position * perms_count + j] = permutation_t(n);
        std::copy(perms[j].begin(), perms[j].end(), perms_set[position * perms_count + j].begin());
    }
    

}

class Neighborhood {

    public:
        
        perms_set_t perms_set;
        int n;
        int k;
        long size;
        int categories;
        long perms_count;

        std::vector<std::pair<int,int>> improving_moves_set;
        std::vector<int> improving_moves_indexes;
        std::vector<long> scores;
        std::vector<long> common_tardiness_set;

        Neighborhood(int n, int k) {
            
            this->n = n;
            this->k = k;
            this->categories = n - k + 1;
            this->perms_count = (factorial(k) - 1);
            this->size = this->perms_count * this->categories;
            this->perms_set = perms_set_t(this->size);
            this->common_tardiness_set = std::vector<long>(this->size);
            this->improving_moves_indexes = std::vector<int>(this->size);
            this->scores = std::vector<long>(this->size);

            for (size_t i = 0; i < this->size; i++) {
                this->improving_moves_indexes[i] = -1;
                this->scores[i] = 0;
            }

            for (size_t i = 0; i < this->categories; i++) {
                generate_permutations_set(n,i,k,this->perms_set, this->perms_count);
            }
        
        }

        std::string to_string() {
            std::string result = "Neighborhood: \n";
            for (size_t i = 0; i < this->categories; i++) {
                result += "Category " + std::to_string(i) + ":\n";
                for(size_t j = 0; j < this->perms_count; j++){
                    result += "Permutation " + std::to_string(j) + ": ";
                    for (size_t l = 0; l < this->n; l++) {
                        result += std::to_string(this->perms_set[i * this->perms_count + j][l]) + " ";
                    }
                    result += "\n";
                }
            }
            return result;
        }

        void insert_move(const int position, const int index) {
            
            if(this->improving_moves_indexes[index] == -1) {
                
                this->improving_moves_set.push_back(std::make_pair(position, index));
                this->improving_moves_indexes[index] = this->improving_moves_set.size() - 1;
            
            }

        }


        void remove_move(const int index) {

            int idx = this->improving_moves_indexes[index];

            if(idx != -1) {

                auto moved_h = this->improving_moves_set.back();
                this->improving_moves_indexes[moved_h.second] = idx;

                std::swap(this->improving_moves_set[idx], this->improving_moves_set.back());
                this->improving_moves_set.pop_back();
                this->improving_moves_indexes[index] = -1;
                                
            
            }

        }

        std::pair<int,int> select_improving_move() {
            
            return *this->improving_moves_set.begin();

        }

};

#endif
