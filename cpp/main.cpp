// sort.cpp (C++ standalone)
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <random>


// QuickSort

enum class PivotMethod {
    LAST,          // ostatni element (domyślny)
    RANDOM,        // losowy element
    MEDIAN_OF_THREE // mediana z trzech
};

int partition(std::vector<int>& arr, int first, int last, PivotMethod method) {
    // Wybór pivota na podstawie metody
    switch (method) {
        case PivotMethod::RANDOM: {
            // Losowy indeks między first a last
            int randomIndex = first + rand() % (last - first + 1);
            std::swap(arr[randomIndex], arr[last]); // pivot na końcu
            break;
        }
        case PivotMethod::MEDIAN_OF_THREE: {
            // Indeks środkowy
            int mid = first + (last - first) / 2;
            
            // Sortowanie trzech elementów: first, mid, last
            if (arr[first] > arr[mid]) std::swap(arr[first], arr[mid]);
            if (arr[mid] > arr[last]) std::swap(arr[mid], arr[last]);
            if (arr[first] > arr[mid]) std::swap(arr[first], arr[mid]);
            
            // Mediana jest w mid, zamiana z last
            std::swap(arr[mid], arr[last]);
            break;
        }
        case PivotMethod::LAST: // Domyślne zachowanie
        default:
            break; // pivot to ostatni element
    }

    // Standardowy schemat Lomuto (pivot = arr[last])
    int pivot = arr[last];
    int i = first - 1;
    for (int j = first; j < last; j++) {
        if (arr[j] <= pivot) {
            i++;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[last]);
    return i + 1;
}

void quickSort(std::vector<int>& arr, int first, int last, PivotMethod method = PivotMethod::LAST) {
    if (first < last) { //Warunek końca rekurencji
        int pi = partition(arr, first, last, method); // Indeks pivota

        // Rekurencyjne wywołanie QuickSort dla podtablicy przed i po pivocie
        quickSort(arr, first, pi - 1, method);
        quickSort(arr, pi + 1, last, method);
    }
}

// Przeciążenie dla wygody (bez podawania first i last)
void quickSort(std::vector<int>& arr, PivotMethod method = PivotMethod::LAST) {
    if (!arr.empty()) {
        quickSort(arr, 0, arr.size() - 1, method);
    }
}


// BubbleSort
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    bool swapped;
    for (int i = 0; i < n - 1; i++) {
        swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break; // Tablica już posortowana
    }
}

int main() {
    const int N = 100000;  // Rozmiar tablicy
    std::vector<int> data(N);

    // Generowanie losowych danych
    std::mt19937 rng(std::random_device{}());
    std::uniform_int_distribution<int> dist(1, 10000);
    for (auto& num : data) num = dist(rng);
    auto copy = data;
    
    // Pomiar QuickSort z domyślnym pivota (ostatni element)
    auto start = std::chrono::high_resolution_clock::now();
    quickSort(copy, 0, copy.size()-1);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> quick_time_last = end - start;

    // Pomiar QuickSort
    copy = data;
    start = std::chrono::high_resolution_clock::now();
    quickSort(copy, 0, copy.size()-1, PivotMethod::MEDIAN_OF_THREE);
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> quick_time_med_of_three = end - start;

    // Pomiar BubbleSort
    copy = data;
    start = std::chrono::high_resolution_clock::now();
    bubbleSort(copy);
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> bubble_time = end - start;
    
    std::cout << "C++ results:\n";
    std::cout << "QuickSort z LAST: " << quick_time_last.count() << " s\n";
    std::cout << "QuickSort z MEDIAN_OF_THREE: " << quick_time_med_of_three.count() << " s\n";
    std::cout << "BubbleSort: " << bubble_time.count() << " s\n";
    
    return 0;
}