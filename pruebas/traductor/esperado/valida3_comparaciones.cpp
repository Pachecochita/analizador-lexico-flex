// Traducido de MiniLang a C++
#include <iostream>

int main() {
    int a = 3;
    int b = 5;
    int c = 5;
    std::cout << (a < b) << std::endl;
    std::cout << (a > b) << std::endl;
    std::cout << (b <= c) << std::endl;
    std::cout << (a >= b) << std::endl;
    std::cout << (b == c) << std::endl;
    std::cout << (a != b) << std::endl;
    std::cout << ((a < b) == (b < c)) << std::endl;
    std::cout << (a < b) + (b == c) << std::endl;
    std::cout << (a < b) * 10 << std::endl;
    int r = a < b;
    std::cout << r << std::endl;
    std::cout << (a + 1 < b) << std::endl;
    std::cout << (a < b + 1) << std::endl;
    double x = 2.5;
    std::cout << (x < 3) << std::endl;
    std::cout << (x >= 2.5) << std::endl;
    return 0;
}
