// Traducido de MiniLang a JavaScript
"use strict";

let n = 5;
let fact = 1;
let i = 1;
while (i <= n) {
    fact = fact * i;
    i = i + 1;
}
console.log(fact);
let cuenta = 3;
while (cuenta > 0) {
    console.log(cuenta);
    cuenta = cuenta - 1;
}
let k = 1;
while (k <= 6) {
    let mitad = Math.trunc(k / 2);
    let resto = k - mitad * 2;
    if (resto === 0) {
        console.log(k);
    } else {
        if (k === 5) {
            console.log(100);
        }
    }
    k = k + 1;
}
