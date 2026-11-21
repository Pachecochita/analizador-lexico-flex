// Traducido de MiniLang a C++
#include <iostream>

int main() {
    int n = 5;
    int fact = 1;
    int i = 1;
    while (i <= n) {
        fact = fact * i;
        i = i + 1;
    }
    std::cout << fact << std::endl;
    int cuenta = 3;
    while (cuenta > 0) {
        std::cout << cuenta << std::endl;
        cuenta = cuenta - 1;
    }
    int k = 1;
    while (k <= 6) {
        int mitad = k / 2;
        int resto = k - mitad * 2;
        if (resto == 0) {
            std::cout << k << std::endl;
        } else {
            if (k == 5) {
                std::cout << 100 << std::endl;
            }
        }
        k = k + 1;
    }
    return 0;
}
