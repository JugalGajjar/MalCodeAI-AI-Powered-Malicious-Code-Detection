#include <iostream>
#include <vector>
#include <string>

class Calculator {
private:
    std::vector<std::string> history;

public:
    double add(double a, double b) {
        double result = a + b;
        history.push_back(std::to_string(a) + " + " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    double subtract(double a, double b) {
        double result = a - b;
        history.push_back(std::to_string(a) + " - " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    double multiply(double a, double b) {
        double result = a * b;
        history.push_back(std::to_string(a) + " * " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    double divide(double a, double b) {
        if (b == 0) throw std::runtime_error("Division by zero.");
        double result = a / b;
        history.push_back(std::to_string(a) + " / " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    void printHistory() const {
        std::cout << "Calculation History:\n";
        for (const auto& entry : history)
            std::cout << entry << std::endl;
    }
};

int main() {
    Calculator calc;
    calc.add(5, 3);
    calc.subtract(10, 4);
    calc.multiply(2, 6);
    try {
        calc.divide(8, 0);
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }

    calc.divide(9, 3);
    calc.printHistory();

    return 0;
}