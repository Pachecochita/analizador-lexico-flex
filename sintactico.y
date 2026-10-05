/*
 * sintactico.y
 * Analizador Sintactico para "MiniLang" (gramatica libre de contexto)
 * Usa el mismo lenguaje documentado para el analizador lexico.
 */

%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);
extern int yylineno;
extern char *yytext;

int huboError = 0;
%}

%token INT FLOAT IF ELSE WHILE PRINT
%token ID NUM_ENTERO NUM_DECIMAL
%token OPREL ASIG

%left '+' '-'
%left '*' '/'
%nonassoc OPREL

%%

programa:
      lista_sentencias
    ;

lista_sentencias:
      /* vacio */
    | lista_sentencias sentencia
    ;

sentencia:
      declaracion ';'
    | asignacion ';'
    | if_sentencia
    | while_sentencia
    | print_sentencia ';'
    ;

tipo:
      INT
    | FLOAT
    ;

declaracion:
      tipo ID
    | tipo ID ASIG expresion
    ;

asignacion:
      ID ASIG expresion
    ;

if_sentencia:
      IF '(' expresion ')' '{' lista_sentencias '}'
    | IF '(' expresion ')' '{' lista_sentencias '}' ELSE '{' lista_sentencias '}'
    ;

while_sentencia:
      WHILE '(' expresion ')' '{' lista_sentencias '}'
    ;

print_sentencia:
      PRINT '(' expresion ')'
    ;

expresion:
      expresion '+' expresion
    | expresion '-' expresion
    | expresion '*' expresion
    | expresion '/' expresion
    | expresion OPREL expresion
    | '(' expresion ')'
    | ID
    | NUM_ENTERO
    | NUM_DECIMAL
    ;

%%

void yyerror(const char *s) {
    huboError = 1;
    fprintf(stderr, "ERROR_SINTACTICO\tlinea %d: %s cerca de '%s'\n", yylineno, s, yytext);
}

int main(int argc, char **argv) {
    extern FILE *yyin;
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            fprintf(stderr, "No se pudo abrir el archivo: %s\n", argv[1]);
            return 1;
        }
    }
    int resultado = yyparse();
    if (resultado == 0 && huboError == 0) {
        printf("ANALISIS_SINTACTICO\tcorrecto\n");
        return 0;
    }
    printf("ANALISIS_SINTACTICO\tincorrecto\n");
    return 1;
}
