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

class SMWTP {
    
    public:
        
        std::vector<int> times;
        std::vector<int> weights;
        std::vector<int> due;
        double globalMin;
        double globalMax;

        SMWTP(const std::string& file) {
            
            globalMin = 0.0;
            globalMax = 0.0;
    
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

        double evaluate(const std::vector<int>& permutation) {
            int t = 0;
            double fit = 0.0;
    
            for (size_t i = 0; i < permutation.size(); ++i) {
                int job = permutation[i] - 1;
                t += times[job];
                if (t > due[job]) {
                    fit += weights[job] * (t - due[job]);
                }
            }
    
            return fit;
        }
    
        // Delta function
        double delta(const std::vector<int>& pi, const std::vector<int>& h, int position, int k) {
            std::vector<int> different_components;
            for (int i = position - 1; i < position + k - 1; ++i) {
                different_components.push_back(i);
            }
    
            double result = 0.0;
            int common_tardiness = 0;
    
            for (int i = 0; i < position - 1; ++i) {
                common_tardiness += times[pi[i] - 1];
            }
    
            int t_pi = common_tardiness;
            int t_hpi = common_tardiness;
    
            for (int i : different_components) {
                int job_pi = pi[i] - 1;
                int job_hpi = pi[h[i] - 1] - 1;
    
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
            }

            return dict;
        }
};


#endif