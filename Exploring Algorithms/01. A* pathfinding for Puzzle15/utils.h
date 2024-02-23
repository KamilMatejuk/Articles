#pragma once
#include <iostream>
#include <algorithm>
#include <numeric>
#include <string>
#include <vector>
#include <cmath>
using namespace std;

string bold(string text);
string red(string text);
string green(string text);
string cyan(string text);
int get_console_width();

string section_name(string text);
string iteration_name(string text);

string time_to_str(double time, bool short_version = true);

// static string RUN_NAME = "test";
static string LOG_FILE = "logs/" + RUN_NAME + ".log";
void clear_log();
void log(string text, bool show = false);
static string SAVE_PATH_FILE = "save_path/" + RUN_NAME + ".path";
void clear_path();
void save_path(string text);

template<typename T> double avg(vector<T> v) {
    return (double)(accumulate(v.begin(), v.end(), 0.0) / v.size());
}
template double avg(vector<int>);
template double avg(vector<double>);

template<typename T> double standard_deviation(vector<T> v) {
    double mean = avg(v);
    double sq_sum = inner_product(v.begin(), v.end(), v.begin(), 0.0);
    return sqrt(sq_sum / v.size() - mean * mean);
}
template double standard_deviation(vector<int>);
template double standard_deviation(vector<double>);

template<typename T> double median(vector<T> v) {
    size_t size = v.size();
    if (size == 0) {
        return 0;
    } else {
        sort(v.begin(), v.end());
        if (size % 2 == 0) {
            return (double)(v[size / 2 - 1] + v[size / 2]) / 2;
        } else {
            return (double)(v[size / 2]);
        }
    }
}
template double median(vector<int>);
template double median(vector<double>);