// Traducido de MiniLang a JavaScript
"use strict";

let a = 48;
let b = 18;
while (a !== b) {
    if (a > b) {
        a = a - b;
    } else {
        b = b - a;
    }
}
console.log(a);
let numero = 4821;
let suma = 0;
while (numero > 0) {
    let digito = numero - Math.trunc(numero / 10) * 10;
    suma = suma + digito;
    numero = Math.trunc(numero / 10);
}
console.log(suma);
let n = 6;
let pasos = 0;
while (n !== 1) {
    let mitad = Math.trunc(n / 2);
    if (n - mitad * 2 === 0) {
        n = mitad;
    } else {
        n = 3 * n + 1;
    }
    pasos = pasos + 1;
}
console.log(pasos);
