#include "settings.h"
#include "puzzle.h"
#include "utils.h"
#include <iostream>
#include <iomanip>
#include <string>
#include <cmath>
using namespace std;


string get_direction_name(Direction d) {
    string name = "";
    switch (d) {
        case Direction::DOWN:  name = "DOWN";  break;
        case Direction::RIGHT: name = "RIGHT"; break;
        case Direction::UP:    name = "UP";    break;
        case Direction::LEFT:  name = "LEFT";  break;
    }
    return name;
}

Puzzle::Puzzle(bool _shuffle /* false */) {
    // create starting positions
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            positions[i][j] = PUZZLE_SIZE * i + j + 1;
        }
    }
    empty_x = PUZZLE_SIZE - 1;
    empty_y = PUZZLE_SIZE - 1;
    positions[empty_y][empty_x] = 0;
    id = "";
    // shuffle
    if (_shuffle) {
        shuffle(pow(PUZZLE_SIZE, 4));
    }
    solution_path_size = 0;
};

Puzzle Puzzle::copy(int new_id) {
    Puzzle p = Puzzle(false);
    // set id
    p.id = id + to_string(new_id);
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            p.positions[i][j] = positions[i][j];
        }
    }
    p.empty_x = empty_x;
    p.empty_y = empty_y;
    p.solution_path_size = solution_path_size;
    return p;
}

string Puzzle::short_state_repr() {
    string repr = "";
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            repr += to_string(positions[i][j]) + "|";
        }
    }
    return repr.substr(0, repr.size() - 1);
}

bool Puzzle::swap(Direction direction) {
    float angle_radians = (PI * direction / 180);
    int x = round(empty_x + sin(angle_radians));
    int y = round(empty_y - cos(angle_radians));
    // check if in range
    if (x < 0 || x >= PUZZLE_SIZE || y < 0 || y >= PUZZLE_SIZE) {
        return false;
    }
    // check if adjacent
    if (!(x == empty_x && abs(y - empty_y) == 1) && \
        !(y == empty_y && abs(x - empty_x) == 1)) {
        return false;
    }
    // swap
    positions[empty_y][empty_x] = positions[y][x];
    positions[y][x] = 0;
    empty_x = x;
    empty_y = y;
    solution_path_size++;
    // save swap
    save_path(id + " " + get_direction_name(direction));
    return true;
}

void Puzzle::shuffle(int n) {
    int i = 0;
    Direction last_direction = Direction::LEFT;
    while (i < n) {
        vector<Direction> possible_dirs = get_possible_moves();
        Direction d = possible_dirs[rand() % possible_dirs.size()];
        // opposite to last direction
        if (abs(d - last_direction) == 180) {
            continue;
        }
        // swap
        if (swap(d)) {
            last_direction = d;
            i++;
        }
    }
    // return empty place to lower right corner
    for (int i = empty_x; i < PUZZLE_SIZE - 1; i++) {
        swap(Direction::RIGHT);
    }
    for (int i = empty_y; i < PUZZLE_SIZE - 1; i++) {
        swap(Direction::DOWN);
    }
}

vector<Direction> Puzzle::get_possible_moves() {
    Direction dirs[4] = { UP, RIGHT, DOWN, LEFT };
    vector<Direction> possible_dirs;
    for (int i = 0; i < 4; i++) {
        Direction d = dirs[i];
        float angle_radians = (PI * d / 180);
        int x = round(empty_x + sin(angle_radians));
        int y = round(empty_y - cos(angle_radians));
        // check if in range
        if (x >= 0 && x < PUZZLE_SIZE && y >= 0 && y < PUZZLE_SIZE) {
            possible_dirs.push_back(d);
        }
    }
    return possible_dirs;
}

bool Puzzle::is_finished() {
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            int p = positions[i][j];
            if (p == 0) {
                p = PUZZLE_SIZE * PUZZLE_SIZE;
            }
            int expected_x = (p - 1) % PUZZLE_SIZE;
            int expected_y = int((p - 1) / PUZZLE_SIZE);
            if (expected_y != i || expected_x != j) {
                return false;
            }
        }
    }
    return true;
}

void Puzzle::show() {
    string edge = "+";
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        edge += "----+";
    }
    log(edge, true);
    for (int i = 0; i < PUZZLE_SIZE; i++) {
        string inside = "|";
        for (int j = 0; j < PUZZLE_SIZE; j++) {
            int p = positions[i][j];
            if (p == 0) {
                inside += "    |";
            } else if (p > 9) {
                inside += " " + to_string(positions[i][j]) + " |";
            } else {
                inside += "  " + to_string(positions[i][j]) + " |";
            }
        }
        log(inside, true);
        log(edge, true);
    }
}
