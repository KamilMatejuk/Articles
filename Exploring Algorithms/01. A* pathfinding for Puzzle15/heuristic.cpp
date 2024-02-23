#include "settings.h"
#include "puzzle.h"
#include "heuristic.h"
#include <iostream>
#include <cmath>
#include <math.h>


float heuristic3(Puzzle& puzzle) {
    // Manhattan Distance from cell to correct position
    // with weights depending on cell nr
    // (1 is most important, 15 is least important)
    // summed with exponential distance from empty space to first not ordered cell
    float distances = 0;
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(PUZZLE_SIZE, 2);
            }
            int expected_x = (p - 1) % PUZZLE_SIZE;
            int expected_y = floor((p - 1) / PUZZLE_SIZE);
            int d = abs(j - expected_x) + abs(i - expected_y);
            float importance = 1.0 - (float)(p / pow(PUZZLE_SIZE, 2));
            distances += d * importance;
        }
    }
    // distance from empty to first not ordered
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(PUZZLE_SIZE, 2);
            }
            int expected_x = (p - 1) % PUZZLE_SIZE;
            int expected_y = floor((p - 1) / PUZZLE_SIZE);
            if((i != expected_y) || (j != expected_x)) {
                int d = abs(j - puzzle.empty_x) + abs(i - puzzle.empty_y);
                float importance = 1.0 - (float)(p / pow(PUZZLE_SIZE, 2));
                distances += d * importance * importance;
                goto endloop;
            }
        }
    }
    endloop:
    return PUZZLE_SIZE * distances;
}

float heuristic2(Puzzle& puzzle) {
    // Manhattan Distance from cell to correct position
    // with weights depending on cell nr
    // (1 is most important, 15 is least important)
    float distances = 0;
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(PUZZLE_SIZE, 2);
            }
            int expected_x = (p - 1) % PUZZLE_SIZE;
            int expected_y = floor((p - 1) / PUZZLE_SIZE);
            int d = abs(j - expected_x) + abs(i - expected_y);
            float importance = 1.0 - (float)(p / pow(PUZZLE_SIZE, 2));
            distances += d * importance;
        }
    }
    return PUZZLE_SIZE * distances;
}

float heuristic1(Puzzle& puzzle) {
    // Manhattan Distance from cell to correct position 
    int distances = 0;
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            int p = puzzle.positions[i][j];
            if(p == 0) {
                p = pow(PUZZLE_SIZE, 2);
            }
            int expected_x = (p - 1) % PUZZLE_SIZE;
            int expected_y = floor((p - 1) / PUZZLE_SIZE);
            distances += abs(j - expected_x) + abs(i - expected_y);
        }
    }
    return PUZZLE_SIZE * distances;
}