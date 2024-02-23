#include "settings.h"
#include "puzzle.h"
#include "heuristic.h"
#include "utils.h"
#include "solver.h"
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <limits>
#include <ctime>

Solver::Solver(Puzzle& puzzle) {
    visited_states = {};
    states_to_visit = { puzzle };
    start_time = clock();
    clear_path();
}

float Solver::heuristic(int number_of_heuristic, Puzzle& puzzle) {
    switch(number_of_heuristic) {
        case 1: return heuristic1(puzzle);
        case 2: return heuristic2(puzzle);
        case 3: return heuristic3(puzzle);
        default: return 0;
    }
}

void Solver::solve(int number_of_heuristic) {
    start_time = clock();
    while (states_to_visit.size() != 0 && 
        ((double) (clock() - start_time)) / CLOCKS_PER_SEC < 14400 /* 4h */) {
        // find nodes with least f
        int min_index = -1;
        int min_f = numeric_limits<int>::max();
        int min_g = numeric_limits<int>::max();
        int min_h = numeric_limits<int>::max();
        for (int i = 0; i < states_to_visit.size(); i++) {
            Puzzle state = states_to_visit[i];
            float g = (float)state.solution_path_size;
            float h = heuristic(number_of_heuristic, state);
            float f = g + h;
            if (f < min_f) {
                min_f = f;
                min_g = g;
                min_h = h;
                min_index = i;
            }
        }
        if (min_index == -1) {
            continue;
        }
        Puzzle min_state = states_to_visit[min_index];
        log("Found minimal state " + min_state.short_state_repr() + \
                " -> f = g + h = " + to_string(min_g) + " + " + \
                to_string(min_h) + " = " + to_string(min_f));
        // pop off list
        states_to_visit.erase(states_to_visit.begin() + min_index);
        // for each successor
        int i = 0;
        for (Direction move : min_state.get_possible_moves()) {
            Puzzle p = min_state.copy(i++);
            if (check_successor(p, move, number_of_heuristic)) {
                // finished
                return;
            }
        }
        visited_states.push_back(min_state);
    }
}

bool Solver::check_successor(Puzzle& succ, Direction move, int number_of_heuristic) {
    succ.swap(move);
    // check if finished
    if (succ.is_finished()) {
        solution = succ;
        solving_time = ((double) (clock() - start_time)) / CLOCKS_PER_SEC;
        log("Found final solution in " + time_to_str(solving_time) + " s (path length: " + \
            to_string(solution.solution_path_size) + ")", true);
        log(get_path());
        return true;
    }
    // f = g + h
    float succ_f = succ.solution_path_size + heuristic(number_of_heuristic, succ);
    // check if already in list to visit with lower value
    bool already_exists_with_lower_f = false;
    for (Puzzle state : states_to_visit) {
        if (state.short_state_repr() == succ.short_state_repr()) {
            float state_f = state.solution_path_size + heuristic(number_of_heuristic, state);
            if (state_f < succ_f) {
                already_exists_with_lower_f = true;
                break;
            }
        }
    }
    if (already_exists_with_lower_f) {
        return false;
    }
    // check if already visited with lower value
    already_exists_with_lower_f = false;
    for (Puzzle state : visited_states) {
        if (state.short_state_repr() == succ.short_state_repr()) {
            float state_f = state.solution_path_size + heuristic(number_of_heuristic, state);
            if (state_f < succ_f) {
                already_exists_with_lower_f = true;
                break;
            }
        }
    }
    if (already_exists_with_lower_f) {
        return false;
    }
    // otherwise add to list
    states_to_visit.push_back(succ);
    return false;
}

string Solver::get_path() {
    vector<string> path;
    string id = solution.id;
    while (id.size() > 0) {
        ifstream infile;
        infile.open(SAVE_PATH_FILE);
        for(string line; getline(infile, line); ){
            int space_index = line.find_first_of(" ");
            string line_id = line.substr(0, space_index);
            string line_dir = line.substr(space_index + 1);
            if (line_id == id) {
                path.insert(path.begin(), line_dir);
                id = id.substr(0, id.size() - 1);
                break;
            }
        }
    }
    string path_str;
    for (string dir : path) {
        path_str += dir + " ";
    }
    return path_str;
}

DataMap Solver::get_data() {
    if (solving_time == 0) {
        solving_time = ((double) (clock() - start_time)) / CLOCKS_PER_SEC;
    }
    return {
        {"number of visited states", to_string(visited_states.size() + 1)},
        {"path length", to_string(solution.solution_path_size)},
        {"path", get_path()},
        {"time", to_string(solving_time)}
    };
}
