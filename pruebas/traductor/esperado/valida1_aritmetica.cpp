// Traducido de MiniLang a C++
#include <iostream>

int main() {
    int a = 12;
    int b = 5;
    double f = 2.5;
    std::cout << a + b << std::endl;
    std::cout << a - b << std::endl;
    std::cout << a * b << std::endl;
    std::cout << a / b << std::endl;
    std::cout << a + f << std::endl;
    std::cout << a * f << std::endl;
    std::cout << f / 2 << std::endl;
    std::cout << a - b * 2 << std::endl;
    std::cout << (a - b) * 2 << std::endl;
    std::cout << a + b * f << std::endl;
    return 0;
}
