#pragma once
#include <iostream>
#include <stdlib.h>
#include <string>
#include <vector>
#include <thread>
#include <cstdlib>
#include <ctime>
#include <map>

typedef map<string, string> DataMap;

template<typename T> static void show_data(string name, vector<T> v, bool time) {
    string values = bold(cyan(name)) + " [ ";
    for (int i = 0; i < v.size(); i++) {
        string padding_l = (i == 0) ? "" : "\n\t\t ";
        string vss = time ? time_to_str(v[i], false) : to_string(v[i]);
        values += time ? padding_l + vss : vss + " ";
    }
    values += " ]";
    log(values, true);
    log(bold("\taverage:       ") + (time ? time_to_str(avg(v)) : to_string(avg(v))), true);
    log(bold("\tmedian:        ") + (time ? time_to_str(median(v)) : to_string(median(v))), true);
    log(bold("\tstd deviation: ") + (time ? time_to_str(standard_deviation(v)) : to_string(standard_deviation(v))), true);
}
template static void show_data(string, vector<int>, bool);
template static void show_data(string, vector<double>, bool);

class Solver {
    public:
        vector<Puzzle> visited_states;
        vector<Puzzle> states_to_visit;
        Puzzle solution;
        double solving_time = 0;
        clock_t start_time;
        
        Solver(Puzzle& puzzle);
        float heuristic(int number_of_heuristic, Puzzle& puzzle);
        void solve(int number_of_heuristic);
        bool check_successor(Puzzle& succ, Direction move, int number_of_heuristic);
        string get_path();
        DataMap get_data();

        static void compare_results(map<string, DataMap> results, int number_of_heuristics) {
            for (int j = 0; j < number_of_heuristics; j++) {
                vector<int> numbers_of_visited_states;
                vector<int> path_lengths;
                vector<double> times;
                string heuristic_key = "heuristic " + to_string(j + 1);
                for (auto const& x : results) {
                    string heuristic_name = x.first;
                    // if this is data for this heuristic
                    if (heuristic_name.find(heuristic_key) != string::npos) {
                        DataMap data = x.second;
                        for (auto const& d : data) {
                            string key = d.first;
                            string value = d.second;
                            if (key == "number of visited states") {
                                numbers_of_visited_states.push_back(atoi(value.c_str()));
                            }
                            if (key == "path length") {
                                path_lengths.push_back(atoi(value.c_str()));
                            }
                            if (key == "time") {
                                times.push_back(stod(value, NULL));
                            }
                            // cout << key << ": " << value << endl;
                        }
                    }
                }

                log(bold(red(heuristic_key)), true);
                show_data("Visited states", numbers_of_visited_states, false);
                show_data("Path lengths  ", path_lengths, false);
                show_data("Duration      ", times, true);
            }
        }

};
