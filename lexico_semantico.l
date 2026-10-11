/*
 * lexico_semantico.l
 * Analizador lexico que alimenta a Bison en el analizador semantico.
 * A diferencia de lexico_sintactico.l, aqui cada token lleva un valor
 * (nombre, numero, linea) que las acciones semanticas necesitan.
 */

%{
#include <stdlib.h>
#include <string.h>
#include "semantico.tab.h"

void errorLexico(int linea, const char *texto);
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

{LETRA}({LETRA}|{DIGITO})*                    { yylval.id.nombre = strdup(yytext);
                                                yylval.id.linea = yylineno;
                                                return ID; }

{DIGITO}+"."{DIGITO}+                         { yylval.num.valor = atof(yytext);
                                                yylval.num.linea = yylineno;
                                                return NUM_DECIMAL; }
{DIGITO}+                                     { yylval.num.valor = atof(yytext);
                                                yylval.num.linea = yylineno;
                                                return NUM_ENTERO; }

"=="|"!="                                     { yylval.rel.esIgualdad = 1;
                                                yylval.rel.linea = yylineno;
                                                return OPREL; }
"<="|">="|"<"|">"                             { yylval.rel.esIgualdad = 0;
                                                yylval.rel.linea = yylineno;
                                                return OPREL; }
"="                                           { return ASIG; }

[+\-*/(){};,]                                 { return yytext[0]; }

"//".*                                        { /* comentario de linea: se ignora */ }
"/*"([^*]|"*"+[^*/])*"*"+"/"                  { /* comentario de bloque: se ignora */ }

[ \t\r\n]+                                    { /* espacios: se ignoran */ }

.                                             { errorLexico(yylineno, yytext); }

%%
