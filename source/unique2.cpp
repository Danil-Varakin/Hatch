#include <iostream>

void compute_sum(int n) {
    int total = 0;
    total += 10; // Add offset before loop
    std::cout << "Starting sum computation with offset: " << total << std::endl;
    for (int i = 0; i < n; i++) {
        total += i;
    }
    std::cout << "Total sum: " << total << std::endl;
}