/*
 * semantico.y
 * Analizador semantico para "MiniLang" (Flex + Bison).
 *
 * Usa la misma gramatica del analizador sintactico y le agrega
 * acciones semanticas (traduccion dirigida por la sintaxis):
 *   - Tabla de simbolos con ambitos (cada bloque { } abre uno nuevo)
 *   - Verificacion de declaracion antes de uso
 *   - Verificacion de tipos (int / float) en expresiones y asignaciones
 *   - Advertencias: variable sin usar, sin valor inicial, sombreado, etc.
 */

%code requires {
    /* Atributos sintetizados de una expresion */
    typedef struct {
        int tipo;    /* T_INT, T_FLOAT o T_ERROR */
        int cero;    /* 1 si es la constante 0 (para detectar division entre cero) */
        int linea;   /* linea donde termina la expresion */
    } Expr;
}

%code {
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

#define T_ERROR 0
#define T_INT   1
#define T_FLOAT 2

#define MAX_SIM 512
#define MAX_MSG 1024
#define MAX_NIVEL 63

/* Clases de mensaje */
#define M_ADVERTENCIA 0
#define M_SEMANTICO   1
#define M_SINTACTICO  2
#define M_LEXICO      3

typedef struct {
    char nombre[64];
    int  tipo;
    int  nivel;          /* 0 = global, 1.. = bloques anidados */
    int  idAmbito;
    int  linea;
    int  inicializada;
    int  usada;
    int  cerrado;        /* 1 cuando su bloque ya termino */
    int  avisoSinValor;  /* para avisar una sola vez */
} Simbolo;

typedef struct {
    int  linea;
    int  clase;
    int  orden;
    char texto[256];
} Mensaje;

static Simbolo tabla[MAX_SIM];
static int nSim = 0;
static Mensaje msgs[MAX_MSG];
static int nMsg = 0;
static int nErrores = 0, nAdvertencias = 0;

static int pilaAmbitos[MAX_NIVEL + 1];
static int nivelActual = 0;
static int contadorAmbitos = 0;
static int huboErrorSintactico = 0;

int yylex(void);
void yyerror(const char *s);
void errorLexico(int linea, const char *texto);
extern int yylineno;
extern char *yytext;

static const char *nombreTipo(int t) {
    return t == T_INT ? "int" : (t == T_FLOAT ? "float" : "error");
}

static void reportar(int clase, int linea, const char *fmt, ...) {
    va_list ap;
    if (nMsg >= MAX_MSG) return;
    msgs[nMsg].linea = linea;
    msgs[nMsg].clase = clase;
    msgs[nMsg].orden = nMsg;
    va_start(ap, fmt);
    vsnprintf(msgs[nMsg].texto, sizeof(msgs[nMsg].texto), fmt, ap);
    va_end(ap);
    nMsg++;
    if (clase == M_ADVERTENCIA) nAdvertencias++; else nErrores++;
}

/* ---------- Tabla de simbolos ---------- */

static int buscar(const char *nombre) {
    int i;
    for (i = nSim - 1; i >= 0; i--)
        if (!tabla[i].cerrado && strcmp(tabla[i].nombre, nombre) == 0) return i;
    return -1;
}

static int buscarEnAmbitoActual(const char *nombre) {
    int i, id = pilaAmbitos[nivelActual];
    for (i = nSim - 1; i >= 0; i--)
        if (!tabla[i].cerrado && tabla[i].idAmbito == id &&
            strcmp(tabla[i].nombre, nombre) == 0) return i;
    return -1;
}

static void declarar(const char *nombre, int tipo, int linea, int inicializada) {
    int previo = buscarEnAmbitoActual(nombre);
    int exterior;
    if (previo >= 0) {
        reportar(M_SEMANTICO, linea,
                 "la variable '%s' ya fue declarada en este bloque (linea %d)",
                 nombre, tabla[previo].linea);
        return;
    }
    exterior = buscar(nombre);
    if (exterior >= 0)
        reportar(M_ADVERTENCIA, linea,
                 "la variable '%s' oculta a otra del bloque exterior (linea %d)",
                 nombre, tabla[exterior].linea);
    if (nSim >= MAX_SIM) {
        reportar(M_SEMANTICO, linea, "demasiadas variables declaradas");
        return;
    }
    strncpy(tabla[nSim].nombre, nombre, 63);
    tabla[nSim].nombre[63] = '\0';
    tabla[nSim].tipo = tipo;
    tabla[nSim].nivel = nivelActual;
    tabla[nSim].idAmbito = pilaAmbitos[nivelActual];
    tabla[nSim].linea = linea;
    tabla[nSim].inicializada = inicializada;
    tabla[nSim].usada = 0;
    tabla[nSim].cerrado = 0;
    tabla[nSim].avisoSinValor = 0;
    nSim++;
}

static void entrarAmbito(void) {
    if (nivelActual >= MAX_NIVEL) return;
    nivelActual++;
    pilaAmbitos[nivelActual] = ++contadorAmbitos;
}

/* Cierra los simbolos de un ambito y avisa de los que nunca se usaron */
static void cerrarSimbolos(int idAmbito) {
    int i;
    for (i = 0; i < nSim; i++) {
        if (!tabla[i].cerrado && tabla[i].idAmbito == idAmbito) {
            if (!tabla[i].usada)
                reportar(M_ADVERTENCIA, tabla[i].linea,
                         "variable '%s' declarada pero nunca usada", tabla[i].nombre);
            tabla[i].cerrado = 1;
        }
    }
}

static void salirAmbito(void) {
    if (nivelActual == 0) return;
    cerrarSimbolos(pilaAmbitos[nivelActual]);
    nivelActual--;
}

/* ---------- Reglas de tipos ---------- */

static Expr usarVariable(const char *nombre, int linea) {
    Expr e;
    int i = buscar(nombre);
    e.cero = 0;
    e.linea = linea;
    if (i < 0) {
        reportar(M_SEMANTICO, linea, "variable '%s' sin declarar", nombre);
        e.tipo = T_ERROR;
        return e;
    }
    tabla[i].usada = 1;
    if (!tabla[i].inicializada && !tabla[i].avisoSinValor) {
        reportar(M_ADVERTENCIA, linea, "'%s' se usa sin tener valor asignado", nombre);
        tabla[i].avisoSinValor = 1;
    }
    e.tipo = tabla[i].tipo;
    return e;
}

/* int op int -> int ; si alguno es float -> float (promocion) */
static Expr aritmetica(Expr a, Expr b) {
    Expr r;
    r.cero = 0;
    r.linea = b.linea;
    if (a.tipo == T_ERROR || b.tipo == T_ERROR) r.tipo = T_ERROR;
    else if (a.tipo == T_FLOAT || b.tipo == T_FLOAT) r.tipo = T_FLOAT;
    else r.tipo = T_INT;
    return r;
}

/* Los operadores relacionales producen un int (0 o 1) */
static Expr relacional(Expr a, int esIgualdad, int linea, Expr b) {
    Expr r;
    r.cero = 0;
    r.linea = b.linea;
    if (a.tipo == T_ERROR || b.tipo == T_ERROR) {
        r.tipo = T_ERROR;
        return r;
    }
    if (esIgualdad && (a.tipo == T_FLOAT || b.tipo == T_FLOAT))
        reportar(M_ADVERTENCIA, linea,
                 "comparar float con == o != puede dar resultados inexactos");
    r.tipo = T_INT;
    return r;
}

}


%union {
    struct { char *nombre; int linea; } id;
    struct { double valor; int linea; } num;
    struct { int esIgualdad; int linea; } rel;
    int tipoDecl;
    Expr expr;
}

%token INT FLOAT IF ELSE WHILE PRINT
%token <id>  ID
%token <num> NUM_ENTERO NUM_DECIMAL
%token <rel> OPREL
%token ASIG

%type <tipoDecl> tipo
%type <expr> expresion

/* De menor a mayor precedencia */
%nonassoc OPREL
%left '+' '-'
%left '*' '/'

%%

programa:
      lista_sentencias
    ;

lista_sentencias:
      %empty
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
      INT    { $$ = T_INT; }
    | FLOAT  { $$ = T_FLOAT; }
    ;

declaracion:
      tipo ID
        { declarar($2.nombre, $1, $2.linea, 0); }
    | tipo ID ASIG expresion
        {
            if ($1 == T_INT && $4.tipo == T_FLOAT)
                reportar(M_SEMANTICO, $2.linea,
                         "no se puede inicializar la variable int '%s' con un valor float (se pierde la parte decimal)",
                         $2.nombre);
            declarar($2.nombre, $1, $2.linea, 1);
        }
    ;

asignacion:
      ID ASIG expresion
        {
            int i = buscar($1.nombre);
            if (i < 0) {
                reportar(M_SEMANTICO, $1.linea, "variable '%s' sin declarar", $1.nombre);
            } else {
                if (tabla[i].tipo == T_INT && $3.tipo == T_FLOAT)
                    reportar(M_SEMANTICO, $1.linea,
                             "no se puede asignar un valor float a la variable int '%s' (se pierde la parte decimal)",
                             $1.nombre);
                tabla[i].inicializada = 1;
            }
        }
    ;

bloque:
      '{' { entrarAmbito(); } lista_sentencias '}' { salirAmbito(); }
    ;

if_sentencia:
      IF '(' expresion ')' bloque
    | IF '(' expresion ')' bloque ELSE bloque
    ;

while_sentencia:
      WHILE '(' expresion ')' bloque
    ;

print_sentencia:
      PRINT '(' expresion ')'
    ;

expresion:
      expresion '+' expresion   { $$ = aritmetica($1, $3); }
    | expresion '-' expresion   { $$ = aritmetica($1, $3); }
    | expresion '*' expresion   { $$ = aritmetica($1, $3); }
    | expresion '/' expresion
        {
            if ($3.cero)
                reportar(M_SEMANTICO, $3.linea, "no se puede dividir entre cero");
            $$ = aritmetica($1, $3);
        }
    | expresion OPREL expresion { $$ = relacional($1, $2.esIgualdad, $2.linea, $3); }
    | '(' expresion ')'         { $$ = $2; }
    | ID                        { $$ = usarVariable($1.nombre, $1.linea); }
    | NUM_ENTERO                { $$.tipo = T_INT;   $$.cero = ($1.valor == 0); $$.linea = $1.linea; }
    | NUM_DECIMAL               { $$.tipo = T_FLOAT; $$.cero = ($1.valor == 0); $$.linea = $1.linea; }
    ;

%%

void yyerror(const char *s) {
    (void)s;
    huboErrorSintactico = 1;
    if (yytext && yytext[0])
        reportar(M_SINTACTICO, yylineno, "error de sintaxis cerca de '%s'", yytext);
    else
        reportar(M_SINTACTICO, yylineno, "error de sintaxis: el codigo termina de forma inesperada");
}

void errorLexico(int linea, const char *texto) {
    reportar(M_LEXICO, linea, "caracter no reconocido '%s'", texto);
}

static int compararMensajes(const void *a, const void *b) {
    const Mensaje *x = (const Mensaje *)a, *y = (const Mensaje *)b;
    if (x->linea != y->linea) return x->linea - y->linea;
    return x->orden - y->orden;
}

int main(int argc, char **argv) {
    extern FILE *yyin;
    int i;
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            fprintf(stderr, "No se pudo abrir el archivo: %s\n", argv[1]);
            return 1;
        }
    }
    yyparse();

    if (!huboErrorSintactico) cerrarSimbolos(0);

    qsort(msgs, nMsg, sizeof(Mensaje), compararMensajes);

    /* Tabla de simbolos (solo si el programa se pudo analizar completo) */
    if (!huboErrorSintactico) {
        for (i = 0; i < nSim; i++)
            printf("SIMBOLO\t%s\t%s\t%d\t%d\t%s\t%s\n",
                   tabla[i].nombre, nombreTipo(tabla[i].tipo), tabla[i].nivel,
                   tabla[i].linea,
                   tabla[i].inicializada ? "si" : "no",
                   tabla[i].usada ? "si" : "no");
    }

    for (i = 0; i < nMsg; i++) {
        const char *etiqueta =
            msgs[i].clase == M_ADVERTENCIA ? "ADVERTENCIA" :
            msgs[i].clase == M_SEMANTICO   ? "ERROR_SEMANTICO" :
            msgs[i].clase == M_SINTACTICO  ? "ERROR_SINTACTICO" : "ERROR_LEXICO";
        printf("%s\t%d\t%s\n", etiqueta, msgs[i].linea, msgs[i].texto);
    }

    printf("ANALISIS_SEMANTICO\t%s\t%d\t%d\n",
           nErrores == 0 ? "correcto" : "incorrecto", nErrores, nAdvertencias);
    return nErrores == 0 ? 0 : 1;
}
