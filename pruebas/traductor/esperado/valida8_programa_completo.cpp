// Traducido de MiniLang a C++
#include <iostream>

int main() {
    int a = 48;
    int b = 18;
    while (a != b) {
        if (a > b) {
            a = a - b;
        } else {
            b = b - a;
        }
    }
    std::cout << a << std::endl;
    int numero = 4821;
    int suma = 0;
    while (numero > 0) {
        int digito = numero - numero / 10 * 10;
        suma = suma + digito;
        numero = numero / 10;
    }
    std::cout << suma << std::endl;
    int n = 6;
    int pasos = 0;
    while (n != 1) {
        int mitad = n / 2;
        if (n - mitad * 2 == 0) {
            n = mitad;
        } else {
            n = 3 * n + 1;
        }
        pasos = pasos + 1;
    }
    std::cout << pasos << std::endl;
    return 0;
}
