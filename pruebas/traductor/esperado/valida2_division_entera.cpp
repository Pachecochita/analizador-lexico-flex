// Traducido de MiniLang a C++
#include <iostream>

int main() {
    int a = 7;
    int cero = 0;
    int neg = cero - 7;
    std::cout << a / 2 << std::endl;
    std::cout << neg / 2 << std::endl;
    std::cout << a / 2.0 << std::endl;
    std::cout << 100 / 7 / 2 << std::endl;
    std::cout << 1 / 2 * 10 << std::endl;
    std::cout << 10 / 4 * 4 << std::endl;
    double x = 10 / 4;
    std::cout << x << std::endl;
    double y = 10 / 4.0;
    std::cout << y << std::endl;
    return 0;
}
