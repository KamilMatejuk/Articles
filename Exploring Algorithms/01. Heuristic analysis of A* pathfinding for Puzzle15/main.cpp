#include "settings.h"
#include "utils.h"
#include "puzzle.h"
#include "heuristic.h"
#include "solver.h"
#include <iostream>
#include <string>
#include <ctime>
using namespace std;

int main() {
    clear_log();
    srand(time(NULL));
    map<string, DataMap> results;

    for (int i = 0; i < NUMBER_OF_ITERATIONS; i++) {
        log(iteration_name("Running test " + to_string(i + 1)), true);
        log(section_name("Generating random Puzzle 15"), true);
        // random starting permutation
        Puzzle p = Puzzle(true);
        p.show();
        // solve with heuristics
        for (int j = 0; j < 3; j++) {
            log(section_name("Testing heuristic " + to_string(j + 1)), true);
            Solver s = Solver(p);
            s.solve(j + 1);
            string map_key = "heuristic " + to_string(j + 1) + " " + to_string(i);
            DataMap data = s.get_data();
            for (auto const& d : data) {
                log(d.first + ": " + d.second, true);
            }
            results.insert({map_key, data});
        }
    }
    log(iteration_name("Comparing results"), true);
    Solver::compare_results(results, 3);
    return 0;
}
