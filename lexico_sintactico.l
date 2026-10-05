/*
 * lexico_sintactico.l
 * Analizador lexico "silencioso": en vez de imprimir cada token (como
 * analizador.l) se lo entrega a Bison para que arme la gramatica.
 */

%{
#include "sintactico.tab.h"
%}

%option noyywrap
%option yylineno

DIGITO [0-9]
LETRA  [a-zA-Z_]

%%

"int"                                         { return INT; }
"float"                                       { return FLOAT; }
"if"                                          { return IF; }
"else"                                        { return ELSE; }
"while"                                       { return WHILE; }
"print"                                       { return PRINT; }

{LETRA}({LETRA}|{DIGITO})*                    { return ID; }

{DIGITO}+"."{DIGITO}+                         { return NUM_DECIMAL; }
{DIGITO}+                                     { return NUM_ENTERO; }

"=="|"!="|"<="|">="|"<"|">"                   { return OPREL; }
"="                                           { return ASIG; }

[+\-*/(){};,]                                 { return yytext[0]; }

"//".*                                        { /* comentario: se ignora */ }
"/*"([^*]|"*"+[^*/])*"*"+"/"                  { /* comentario: se ignora */ }

[ \t\r\n]+                                    { /* espacios: se ignoran */ }

.                                              { fprintf(stderr, "ERROR_LEXICO\tlinea %d: caracter no reconocido '%s'\n", yylineno, yytext); }

%%
