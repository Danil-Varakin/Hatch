#include <iostream>

class Calculator {
public:
    double calculate(double x, double y) {
        double result = x + y;
        std::cout << "Calculation in progress, intermediate result: " << result << std::endl;
        result *= 1.5; // Scale result
        if (result > 0.0) {
            std::cout << "Positive result: " << result << std::endl;
        }
        return result;
    }
};