#include "settings.h"
#include "utils.h"
#include <string>
#include <vector>
#include <iostream>
#include <fstream>

string bold(string text) {
    return "\033[1m" + text + "\033[0m";
}

string red(string text) {
    return "\033[31m" + text + "\033[0m";
}

string green(string text) {
    return "\033[32m" + text + "\033[0m";
}

string cyan(string text) {
    return "\033[36m" + text + "\033[0m";
}

string pad(string text, int width, char padding) {
    string res = "";
    if (text.size() > width) {
        res = text;
    } else {
        int pad_width = (width - text.size()) / 2;
        for (int i = 0; i < pad_width - 1; i++) {
            res += padding;
        }
        res += " " + text + " ";
        int size = res.size();
        for (int i = width; i > size; i--) {
            res += padding;
        }
    }
    return res;
}

string section_name(string text) {
    return bold(green(pad(text, 80, '=')));
}

string iteration_name(string text) {
    return bold(cyan(pad(text, 80, '=')));
}

string time_to_str(double time, bool short_version /* true */) {
    double t = time;
    int h = time / 3600;
    time -= 3600 * h;
    int m = time / 60;
    time -= 60 * m;
    int s = time;
    time -= s;
    int ms = time * 1000;
    string res = "";
    char buffer[24];
    if (!short_version || h > 0) {
        sprintf(buffer, "%1s", to_string(h).c_str());
        res += string(buffer) + " h ";
    }
    if (!short_version || m > 0) {
        sprintf(buffer, "%2s", to_string(m).c_str());
        res += string(buffer) + " m ";
    }
    if (!short_version || s > 0) {
        sprintf(buffer, "%2s", to_string(s).c_str());
        res += string(buffer) + " s ";
    }
    sprintf(buffer, "%3s", to_string(ms).c_str());
    res += string(buffer) + " ms (" + to_string(t) + "s)";
    return res;
}

void clear_log() {
    ofstream outfile;
    outfile.open(LOG_FILE);
    outfile << "";
}

void log(string text, bool show) {
    if (show) {
        cout << text << endl;
    }
    // remove special chars
    vector<string> remove_list;
    remove_list.push_back("\033[0m");
    remove_list.push_back("\033[1m");
    remove_list.push_back("\033[31m");
    remove_list.push_back("\033[32m");
    remove_list.push_back("\033[36m");
    for (string rs : remove_list) {
        size_t pos = string::npos;
        while ((pos = text.find(rs)) != string::npos) {
            text.erase(pos, rs.length());
        }
    }
    ofstream outfile;
    outfile.open(LOG_FILE, ios_base::app); // append
    outfile << text + "\n";
}

void clear_path() {
    ofstream outfile;
    outfile.open(SAVE_PATH_FILE);
    outfile << "";
}

void save_path(string text) {
    ofstream outfile;
    outfile.open(SAVE_PATH_FILE, ios_base::app); // append
    outfile << text + "\n";
}