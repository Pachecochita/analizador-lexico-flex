// Traducido de MiniLang a JavaScript
"use strict";

let a = 3;
let b = 5;
let c = 5;
console.log(Number(a < b));
console.log(Number(a > b));
console.log(Number(b <= c));
console.log(Number(a >= b));
console.log(Number(b === c));
console.log(Number(a !== b));
console.log(Number(Number(a < b) === Number(b < c)));
console.log(Number(a < b) + Number(b === c));
console.log(Number(a < b) * 10);
let r = Number(a < b);
console.log(r);
console.log(Number(a + 1 < b));
console.log(Number(a < b + 1));
let x = 2.5;
console.log(Number(x < 3));
console.log(Number(x >= 2.5));
