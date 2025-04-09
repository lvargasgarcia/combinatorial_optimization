#ifndef SMWTP_HPP
#define SMWTP_HPP

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <fstream>
#include <sstream>
#include <iostream>
#include <stdexcept>
#include <map>
#include <bits/stl_numeric.h>
#include <bits/algorithmfwd.h>
#include "permutation_utils.hpp"
#include "Neighborhood.hpp"

class SMWTP {
    
    public:
        
        std::vector<int> times;
        std::vector<int> weights;
        std::vector<int> due;
        permutation_t optima;
        double globalMin;
        double globalMax;

        SMWTP(const std::string& file) {
            
            globalMin = -1;
            globalMax = -1;
    
            std::ifstream infile(file);
            if (!infile.is_open()) {
                throw std::runtime_error("Error: Unable to open file " + file);
            }
    
            std::string line;
            int n = 0;
    
            // Read the first line for the number of elements
            if (std::getline(infile, line)) {
                std::istringstream iss(line);
                iss >> n;
            } else {
                throw std::runtime_error("Error: File is empty or invalid format");
            }
    
            // Read the remaining lines for times, weights, and due dates
            while (std::getline(infile, line)) {
                std::istringstream iss(line);
                double time, weight, dueDate;
                if (iss >> time >> weight >> dueDate) {
                    times.push_back(time);
                    weights.push_back(weight);
                    due.push_back(dueDate);
                } else {
                    throw std::runtime_error("Error: Invalid line format in file");
                }
            }
    
            if (n != static_cast<int>(times.size())) {
                std::cerr << "Warning: Elements count does not match" << std::endl;
            }
        }

        double evaluate(const permutation_t& permutation) {
            
            int t = 0;
            double fit = 0.0;
    
            for (size_t i = 0; i < this->times.size(); ++i) {
                int job = permutation[i];
                t += times[job];
                if (t > due[job]) {
                    fit += weights[job] * (t - due[job]);
                }
            }
    
            return fit;
        }
    
        // Delta function
        double delta(const permutation_t& pi, const permutation_t& selected_move, const permutation_t& h, int position, int k, long common_tardiness) {
                
            double result = 0.0;
    
            int t_pi = common_tardiness;
            int t_hpi = common_tardiness;
    
            for (int i = position; i < position + k; i++) {
                
                int job_pi = pi[selected_move[i]];
                int job_hpi = pi[selected_move[h[i]]];
    
                t_pi += times[job_pi];
                t_hpi += times[job_hpi];
    
                if (t_pi > due[job_pi]) {
                    result -= weights[job_pi] * (t_pi - due[job_pi]);
                }
    
                if (t_hpi > due[job_hpi]) {
                    result += weights[job_hpi] * (t_hpi - due[job_hpi]);
                }
            }
    
            return result;
        }
    
        // Get the number of jobs
        int getN() const {
            return times.size();
        }
    
        // Get the function values for all permutations
        std::map<std::string, double> getFunction() {
            
            int n = times.size();
            std::map<std::string, double> dict;

            vector<vector<int>> perms = permutations(n);
    
            for (const auto& perm : perms) {
                std::string key = to_string(perm);
                double value = evaluate(perm);
                dict[key] = value;

                if (globalMin == -1 || value < globalMin) {
                    globalMin = value;
                    optima = perm;
                }

                if (globalMax == -1 || value > globalMax) {
                    globalMax = value;
                }
            }

            return dict;
        }
};


#endif