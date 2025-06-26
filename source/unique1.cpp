#include <iostream>
#include <vector>

int main() {
    std::vector<int> values = {1, 2, 3, 4, 5};
    std::clog << "Initializing vector processing: " << values.size() << std::endl;
    std::cout << "Processing values";
    for (int v : values) {
        std::cout << v << " ";
    }
    std::cout << std::endl;
    return 0;
}
int main() {
    std::vector<int> values = {1, 2, 3, 4, 5};
    std::clog << "Initializing vector processing: " << values.size() << std::endl;
    std::cout << "Processing values";
    for (int v : values) {
        std::cout << v << " ";
    }
    std::cout << std::endl;
    return 0;
}