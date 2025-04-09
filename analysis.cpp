#include "Neighborhood.hpp"
#include "smwtp.hpp"
#include "local_search.hpp"
#include <iostream>
#include "DRILS.hpp"
#include <nlohmann/json.hpp>
#include <vector>
#include <utility>

using json = nlohmann::json;

void save_vector_to_json(const std::vector<std::pair<long, long>>& data, int real_optima, int neighborhood_size) {
    json j;

    for (const auto& elem : data) {
        j[std::to_string(elem.first)] = elem.second;
    }

    j["real_optima"] = real_optima;
    j["neighborhood_size"] = neighborhood_size;

    auto dump = j.dump(4);
    std::cout << dump; // `4` es indentación bonita
}


int get_number_from_line(const std::string& file_path, int line_number) {
    
    std::ifstream file(file_path);

    if (!file.is_open()) {
        std::cerr << "No se pudo abrir el archivo: " << file_path << std::endl;
        return -1;  // Retorna -1 si hay un error al abrir el archivo
    }

    std::string line;
    int current_line = 1;
    int target_number = -1;  

    while (std::getline(file, line)) {
        if (current_line == line_number) {
            std::stringstream ss(line);
            ss >> target_number;  // Extrae el número de la línea
            break;
        }
        ++current_line;
    }

    file.close();

    return target_number;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Uso: " << argv[0] << " <archivo_instancia>\n";
        return 1;
    }

    int n = std::stoi(argv[1]);
    int number = std::stoi(argv[2]);

    int neighborhood_size = std::stoi(argv[3]);
    int run_time = std::stoi(argv[4]);

    std::string instance = "./instances_opt/instances/" + std::to_string(n) + "/n" + std::to_string(n) + "_" + std::to_string(number) + "_b.txt";
    std::string optima_file = "./instances_opt/instances/opt" + std::to_string(n) + ".txt";

    long real_optima = get_number_from_line(optima_file, number);

    auto prob = SMWTP(instance);

    n = prob.getN();

    auto result = DRILS(prob, neighborhood_size, run_time);

    save_vector_to_json(result, real_optima, neighborhood_size);

    return 0;
}
