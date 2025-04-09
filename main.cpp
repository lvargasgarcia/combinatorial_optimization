#include "smwtp.hpp"
#include "efficient_operators.hpp"


int main() {

    // std::string instance = "../instances_opt/instances/1000/n1000_24_b.txt";
    // std::string instance = "../instances/smwtp/n10_rdd0.4_tf1.0_seed2.txt";
    // auto prob = SMWTP(instance);
    // prob.getFunction();
    // int globalMin = prob.globalMin;

    // auto f = instance.getFunction();

    // for (const auto& [key, value] : f) {
    //     std::cout << key << ": " << value << "\n";
    // }

    // auto pi = std::vector<int>{2,1,4,5,3};
    // auto pi2 = std::vector<int>{1,3,4,2,5};

    // std:: cout << instance.delta(pi, pi2, 2, 3) << "\n";

    // auto info = generate_movements(6, 3);

    // for (const auto& [key, value] : info) {
    //     std::cout << "Position: " << key << "\n";
    //     for (const auto& [perm, _] : value) {
    //         std::cout << perm << "\n";
    //     }
    // }

    // local_search(3, instance, std::vector<int>{2,1,4,5,3});

    auto info = DRILS(instance, 3, 1000000, true);

    std::cout << "Reached value: " << info.second << "\n";
    // std::cout << "Global minimum: " << globalMin << "\n";

    // auto s = std::unordered_set<int>();
    // for (int i = 1; i <= instance.getN(); ++i) {
    //     s.insert(i);
    // }

    // int k = 0;
    // int l = 0;

    // for(int i = 0; i < 10000; ++i){
    //     auto pi = random_permutation(s);
    //     cout << "Initial permutation: " << to_string(pi) << "\n";
    //     auto pi2 = perturbation_function(pi);
    //     cout << "Perturbed permutation: " << to_string(pi2) << "\n";
    //     cout << "Movement: " << to_string(compose(inverse(pi), pi2)) << "\n";
    //     auto child = partition_crossover(pi, pi2, instance);
    //     cout << "Child permutation: " << to_string(child) << "\n";

    //     if (instance.evaluate(child) < instance.evaluate(pi) && instance.evaluate(child) < instance.evaluate(pi2)) {
    //         k++;
    //     }
        
    //     if (child != pi && child != pi2) {
    //         l++;
    //     }

    //     cout << "--------------------------\n";
    // }

    // std::cout << ((float)k)/((float)10000) << "\n";
    // std::cout << ((float)l)/((float)10000) << "\n";
    

}