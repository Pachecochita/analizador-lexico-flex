/*
 * analizador.l
 * Analizador Lexico para "MiniLang"
 * Lenguaje de prueba: declaraciones tipo C simplificadas
 */

%{
#include <stdio.h>
#include <stdlib.h>
%}

DIGITO   [0-9]
LETRA    [a-zA-Z_]

%%

"int"|"float"|"if"|"else"|"while"|"print"    { printf("PALABRA_RESERVADA\t%s\n", yytext); }

{LETRA}({LETRA}|{DIGITO})*                    { printf("IDENTIFICADOR\t%s\n", yytext); }

{DIGITO}+"."{DIGITO}+                         { printf("NUMERO_DECIMAL\t%s\n", yytext); }
{DIGITO}+                                     { printf("NUMERO_ENTERO\t%s\n", yytext); }

"=="                                          { printf("OP_RELACIONAL\t%s\n", yytext); }
"!="                                          { printf("OP_RELACIONAL\t%s\n", yytext); }
"<="                                          { printf("OP_RELACIONAL\t%s\n", yytext); }
">="                                          { printf("OP_RELACIONAL\t%s\n", yytext); }
"<"                                           { printf("OP_RELACIONAL\t%s\n", yytext); }
">"                                           { printf("OP_RELACIONAL\t%s\n", yytext); }

"="                                           { printf("OP_ASIGNACION\t%s\n", yytext); }
"+"                                           { printf("OP_SUMA\t%s\n", yytext); }
"-"                                           { printf("OP_RESTA\t%s\n", yytext); }
"*"                                           { printf("OP_MULTIPLICACION\t%s\n", yytext); }
"/"                                           { printf("OP_DIVISION\t%s\n", yytext); }

"("                                           { printf("PARENTESIS_IZQ\t%s\n", yytext); }
")"                                           { printf("PARENTESIS_DER\t%s\n", yytext); }
"{"                                           { printf("LLAVE_IZQ\t%s\n", yytext); }
"}"                                           { printf("LLAVE_DER\t%s\n", yytext); }
";"                                           { printf("PUNTO_COMA\t%s\n", yytext); }
","                                           { printf("COMA\t%s\n", yytext); }

"//".*                                        { /* comentario de linea: se ignora */ }
"/*"([^*]|"*"+[^*/])*"*"+"/"                  { /* comentario de bloque: se ignora */ }

[ \t\r\n]+                                    { /* espacios en blanco: se ignoran */ }

.                                              { printf("ERROR_LEXICO\t%s\n", yytext); }

%%

int yywrap(void) { return 1; }

int main(int argc, char **argv) {
    if (argc > 1) {
        FILE *archivo = fopen(argv[1], "r");
        if (!archivo) {
            fprintf(stderr, "No se pudo abrir el archivo: %s\n", argv[1]);
            return 1;
        }
        yyin = archivo;
    }
    yylex();
    if (argc > 1) {
        fclose(yyin);
    }
    return 0;
}
