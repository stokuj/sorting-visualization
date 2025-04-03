// sort.cpp (C++ standalone)
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>

// QuickSort
int partition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// BubbleSort
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] > arr[j+1]) {
                std::swap(arr[j], arr[j+1]);
            }
        }
    }
}

int main() {
    const int N = 10000;  // Rozmiar tablicy
    std::vector<int> data(N);
    
    // Generowanie losowych danych
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(1, 10000);
    for (auto& num : data) num = dist(rng);
    
    auto copy = data;
    
    // Pomiar QuickSort
    auto start = std::chrono::high_resolution_clock::now();
    quickSort(copy, 0, copy.size()-1);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> quick_time = end - start;
    
    // Pomiar BubbleSort
    copy = data;
    start = std::chrono::high_resolution_clock::now();
    bubbleSort(copy);
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> bubble_time = end - start;
    
    std::cout << "C++ results:\n";
    std::cout << "QuickSort: " << quick_time.count() << " s\n";
    std::cout << "BubbleSort: " << bubble_time.count() << " s\n";
    
    return 0;
}