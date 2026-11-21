/*
 * lexico_traductor.l
 * Analizador lexico que alimenta a Bison en el traductor.
 * Igual que el del semantico, pero los numeros y los operadores
 * relacionales tambien entregan su texto, porque el traductor
 * necesita escribirlos en el codigo de salida.
 */

%{
#include <stdlib.h>
#include <string.h>
#include "traductor.tab.h"

void errorLexico(int linea, const char *texto);
%}

%option noyywrap
%option nounput
%option noinput
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
                                                yylval.num.texto = strdup(yytext);
                                                return NUM_DECIMAL; }
{DIGITO}+                                     { yylval.num.valor = atof(yytext);
                                                yylval.num.linea = yylineno;
                                                yylval.num.texto = strdup(yytext);
                                                return NUM_ENTERO; }

"=="|"!="                                     { yylval.rel.esIgualdad = 1;
                                                yylval.rel.linea = yylineno;
                                                strcpy(yylval.rel.op, yytext);
                                                return OPREL; }
"<="|">="|"<"|">"                             { yylval.rel.esIgualdad = 0;
                                                yylval.rel.linea = yylineno;
                                                strcpy(yylval.rel.op, yytext);
                                                return OPREL; }
"="                                           { return ASIG; }

[+\-*/(){};,]                                 { return yytext[0]; }

"//".*                                        { /* comentario de linea: se ignora */ }
"/*"([^*]|"*"+[^*/])*"*"+"/"                  { /* comentario de bloque: se ignora */ }

[ \t\r\n]+                                    { /* espacios: se ignoran */ }

.                                             { errorLexico(yylineno, yytext); }

%%
