/*
 * intermedio.y
 * Generador de codigo intermedio para "MiniLang" (Flex + Bison).
 *
 * Genera CODIGO DE TRES DIRECCIONES en forma de cuadruplas
 * (operador, argumento 1, argumento 2, resultado). Funciona en una sola
 * pasada, igual que el analizador semantico:
 *   1. Bison reconoce la gramatica de MiniLang.
 *   2. Las acciones comprueban declaraciones y tipos (tabla de simbolos).
 *   3. Esas mismas acciones van escribiendo las cuadruplas.
 * Si el programa tiene algun error no se genera codigo.
 *
 * Instrucciones que se generan:
 *   =        x = a              asignacion / copia
 *   + - * /  t = a op b         aritmetica (/ entre dos float)
 *   div      t = a div b        division entera (int entre int)
 *   < > <= >= == !=  t = a op b comparacion; el resultado es 0 o 1
 *   label    L:                 etiqueta
 *   goto     goto L             salto incondicional
 *   ifFalse  ifFalse t goto L   salta si t vale 0
 *   print    print a            muestra un valor
 *
 * Uso:  intermedio archivo.txt
 */

%code requires {
    /* Atributos sintetizados de una expresion */
    typedef struct {
        int   tipo;     /* T_INT, T_FLOAT o T_ERROR */
        int   cero;     /* 1 si es la constante 0 (division entre cero) */
        int   linea;    /* linea donde termina la expresion */
        char *lugar;    /* donde queda el valor: variable, constante o temporal */
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
#define MAX_ANIDADOS 256

/* Clases de mensaje */
#define M_ADVERTENCIA 0
#define M_SEMANTICO   1
#define M_SINTACTICO  2
#define M_LEXICO      3

typedef struct {
    char nombre[64];
    char tac[80];        /* nombre unico que se usa en el codigo intermedio */
    int  tipo;
    int  nivel;
    int  idAmbito;
    int  linea;
    int  inicializada;
    int  usada;
    int  cerrado;
    int  avisoSinValor;
} Simbolo;

typedef struct {
    int  linea;
    int  clase;
    int  orden;
    char texto[256];
} Mensaje;

typedef struct {
    char *op, *arg1, *arg2, *res;
} Cuadrupla;

static Simbolo tabla[MAX_SIM];
static int nSim = 0;
static Mensaje msgs[MAX_MSG];
static int nMsg = 0;
static int nErrores = 0, nAdvertencias = 0;

static int pilaAmbitos[MAX_NIVEL + 1];
static int nivelActual = 0;
static int contadorAmbitos = 0;
static int huboErrorSintactico = 0;

static Cuadrupla *cuads = NULL;
static int nCuads = 0, capCuads = 0;
static int nTemporales = 0, nEtiquetas = 0;

/* Etiquetas pendientes de los if y los while que estan abiertos */
static int pilaEtiq[MAX_ANIDADOS];
static int cimaEtiq = 0;

int yylex(void);
void yyerror(const char *s);
void errorLexico(int linea, const char *texto);
extern int yylineno;
extern char *yytext;

/* ---------- Utilidades ---------- */

static void sinMemoria(void) {
    fprintf(stderr, "sin memoria\n");
    exit(2);
}

static char *copiar(const char *s) {
    char *r = malloc(strlen(s) + 1);
    if (!r) sinMemoria();
    strcpy(r, s);
    return r;
}

static char *fmt(const char *f, ...) {
    va_list ap;
    char buf[256];
    va_start(ap, f);
    vsnprintf(buf, sizeof(buf), f, ap);
    va_end(ap);
    return copiar(buf);
}

static void reportar(int clase, int linea, const char *f, ...) {
    va_list ap;
    if (nMsg >= MAX_MSG) return;
    msgs[nMsg].linea = linea;
    msgs[nMsg].clase = clase;
    msgs[nMsg].orden = nMsg;
    va_start(ap, f);
    vsnprintf(msgs[nMsg].texto, sizeof(msgs[nMsg].texto), f, ap);
    va_end(ap);
    nMsg++;
    if (clase == M_ADVERTENCIA) nAdvertencias++; else nErrores++;
}

/* "007" pasa a "7" */
static char *normalizarNumero(const char *t) {
    while (t[0] == '0' && t[1] >= '0' && t[1] <= '9') t++;
    return copiar(t);
}

/* ---------- Cuadruplas ---------- */

static void cuad(const char *op, const char *a1, const char *a2, const char *res) {
    if (nCuads == capCuads) {
        capCuads = capCuads ? capCuads * 2 : 64;
        cuads = realloc(cuads, (size_t)capCuads * sizeof(Cuadrupla));
        if (!cuads) sinMemoria();
    }
    cuads[nCuads].op   = copiar(op);
    cuads[nCuads].arg1 = copiar(a1);
    cuads[nCuads].arg2 = copiar(a2);
    cuads[nCuads].res  = copiar(res);
    nCuads++;
}

static char *nuevoTemporal(void) { return fmt("t%d", ++nTemporales); }

static int nuevaEtiqueta(void) { return ++nEtiquetas; }

static void ponerEtiqueta(int n) {
    char *e = fmt("L%d", n);
    cuad("label", "-", "-", e);
    free(e);
}

static void saltarA(int n) {
    char *e = fmt("L%d", n);
    cuad("goto", "-", "-", e);
    free(e);
}

static void saltarSiFalso(const char *cond, int n) {
    char *e = fmt("L%d", n);
    cuad("ifFalse", cond, "-", e);
    free(e);
}

static void apilar(int n) { if (cimaEtiq < MAX_ANIDADOS) pilaEtiq[cimaEtiq++] = n; }
static int desapilar(void) { return cimaEtiq > 0 ? pilaEtiq[--cimaEtiq] : 0; }

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

/* Parece un temporal (t1, t2...) */
static int pareceTemporal(const char *n) {
    int i;
    if (n[0] != 't' || !n[1]) return 0;
    for (i = 1; n[i]; i++)
        if (n[i] < '0' || n[i] > '9') return 0;
    return 1;
}

static int tacOcupado(const char *c) {
    int i;
    if (pareceTemporal(c)) return 1;
    for (i = 0; i < nSim; i++)
        if (strcmp(tabla[i].tac, c) == 0) return 1;
    return 0;
}

/* Dos variables de distintos bloques pueden llamarse igual. En el codigo
 * intermedio no hay bloques, asi que a la segunda se le agrega _2, _3... */
static void nombreUnico(const char *nombre, char *salida) {
    char cand[80];
    int k = 2;
    snprintf(cand, sizeof(cand), "%s", nombre);
    while (tacOcupado(cand))
        snprintf(cand, sizeof(cand), "%.60s_%d", nombre, k++);
    strcpy(salida, cand);
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
    nombreUnico(nombre, tabla[nSim].tac);
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

/* ---------- Expresiones ---------- */

static Expr usarVariable(const char *nombre, int linea) {
    Expr e;
    int i = buscar(nombre);
    e.cero = 0;
    e.linea = linea;
    if (i < 0) {
        reportar(M_SEMANTICO, linea, "variable '%s' sin declarar", nombre);
        e.tipo = T_ERROR;
        e.lugar = copiar(nombre);
        return e;
    }
    tabla[i].usada = 1;
    if (!tabla[i].inicializada && !tabla[i].avisoSinValor) {
        reportar(M_ADVERTENCIA, linea, "'%s' se usa sin tener valor asignado", nombre);
        tabla[i].avisoSinValor = 1;
    }
    e.tipo = tabla[i].tipo;
    e.lugar = copiar(tabla[i].tac);
    return e;
}

static Expr literal(int tipo, double v, const char *texto, int linea) {
    Expr e;
    e.tipo = tipo;
    e.cero = (v == 0);
    e.linea = linea;
    e.lugar = normalizarNumero(texto);
    return e;
}

/* int op int -> int ; si alguno es float -> float (promocion).
 * Entre dos int la division es entera y se escribe "div". */
static Expr aritmetica(Expr a, char op, Expr b) {
    Expr r;
    char opTexto[8];
    r.cero = 0;
    r.linea = b.linea;
    if (a.tipo == T_ERROR || b.tipo == T_ERROR) r.tipo = T_ERROR;
    else if (a.tipo == T_FLOAT || b.tipo == T_FLOAT) r.tipo = T_FLOAT;
    else r.tipo = T_INT;

    r.lugar = nuevoTemporal();
    if (op == '/' && a.tipo == T_INT && b.tipo == T_INT) strcpy(opTexto, "div");
    else { opTexto[0] = op; opTexto[1] = '\0'; }
    cuad(opTexto, a.lugar, b.lugar, r.lugar);
    return r;
}

/* Las comparaciones producen un int (0 o 1) */
static Expr relacional(Expr a, int esIgualdad, int linea, const char *op, Expr b) {
    Expr r;
    r.cero = 0;
    r.linea = b.linea;
    r.lugar = nuevoTemporal();
    cuad(op, a.lugar, b.lugar, r.lugar);
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
    struct { double valor; int linea; char *texto; } num;
    struct { int esIgualdad; int linea; char op[3]; } rel;
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

/* Una variable declarada sin valor arranca en 0 (igual que en el traductor) */
declaracion:
      tipo ID
        {
            declarar($2.nombre, $1, $2.linea, 0);
            { int i = buscarEnAmbitoActual($2.nombre);
              if (i >= 0) cuad("=", "0", "-", tabla[i].tac); }
        }
    | tipo ID ASIG expresion
        {
            if ($1 == T_INT && $4.tipo == T_FLOAT)
                reportar(M_SEMANTICO, $2.linea,
                         "no se puede inicializar la variable int '%s' con un valor float (se pierde la parte decimal)",
                         $2.nombre);
            declarar($2.nombre, $1, $2.linea, 1);
            { int i = buscarEnAmbitoActual($2.nombre);
              if (i >= 0) cuad("=", $4.lugar, "-", tabla[i].tac); }
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
                cuad("=", $3.lugar, "-", tabla[i].tac);
            }
        }
    ;

bloque:
      '{' { entrarAmbito(); }
      lista_sentencias
      '}' { salirAmbito(); }
    ;

/*  if (c) A            ifFalse c goto Lfin ; A ; Lfin:
 *  if (c) A else B     ifFalse c goto Lelse ; A ; goto Lfin ; Lelse: ; B ; Lfin:  */
if_sentencia:
      IF '(' expresion ')'
        { int l = nuevaEtiqueta(); saltarSiFalso($3.lugar, l); apilar(l); }
      bloque else_opcional
    ;

else_opcional:
      %empty
        { ponerEtiqueta(desapilar()); }
    | ELSE
        { int lFin = nuevaEtiqueta(), lElse = desapilar();
          saltarA(lFin); ponerEtiqueta(lElse); apilar(lFin); }
      bloque
        { ponerEtiqueta(desapilar()); }
    ;

/*  while (c) A         Linicio: ; ifFalse c goto Lfin ; A ; goto Linicio ; Lfin:  */
while_sentencia:
      WHILE
        { int l = nuevaEtiqueta(); ponerEtiqueta(l); apilar(l); }
      '(' expresion ')'
        { int l = nuevaEtiqueta(); saltarSiFalso($4.lugar, l); apilar(l); }
      bloque
        { int lFin = desapilar(), lInicio = desapilar();
          saltarA(lInicio); ponerEtiqueta(lFin); }
    ;

print_sentencia:
      PRINT '(' expresion ')'   { cuad("print", $3.lugar, "-", "-"); }
    ;

expresion:
      expresion '+' expresion   { $$ = aritmetica($1, '+', $3); }
    | expresion '-' expresion   { $$ = aritmetica($1, '-', $3); }
    | expresion '*' expresion   { $$ = aritmetica($1, '*', $3); }
    | expresion '/' expresion
        {
            if ($3.cero)
                reportar(M_SEMANTICO, $3.linea, "no se puede dividir entre cero");
            $$ = aritmetica($1, '/', $3);
        }
    | expresion OPREL expresion { $$ = relacional($1, $2.esIgualdad, $2.linea, $2.op, $3); }
    | '(' expresion ')'         { $$ = $2; }
    | ID                        { $$ = usarVariable($1.nombre, $1.linea); }
    | NUM_ENTERO                { $$ = literal(T_INT,   $1.valor, $1.texto, $1.linea); }
    | NUM_DECIMAL               { $$ = literal(T_FLOAT, $1.valor, $1.texto, $1.linea); }
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

static const char *etiquetaMensaje(int clase) {
    switch (clase) {
        case M_ADVERTENCIA: return "ADVERTENCIA";
        case M_SEMANTICO:   return "ERROR_SEMANTICO";
        case M_SINTACTICO:  return "ERROR_SINTACTICO";
        default:            return "ERROR_LEXICO";
    }
}

/* Una cuadrupla escrita como instruccion de tres direcciones */
static void imprimirInstruccion(const Cuadrupla *c) {
    if (strcmp(c->op, "label") == 0)        printf("%s:", c->res);
    else if (strcmp(c->op, "goto") == 0)    printf("    goto %s", c->res);
    else if (strcmp(c->op, "ifFalse") == 0) printf("    ifFalse %s goto %s", c->arg1, c->res);
    else if (strcmp(c->op, "print") == 0)   printf("    print %s", c->arg1);
    else if (strcmp(c->op, "=") == 0)       printf("    %s = %s", c->res, c->arg1);
    else                                    printf("    %s = %s %s %s", c->res, c->arg1, c->op, c->arg2);
}

int main(int argc, char **argv) {
    extern FILE *yyin;
    int i, ok;

    if (argc != 2) {
        fprintf(stderr, "Uso: intermedio archivo.txt\n");
        return 2;
    }
    yyin = fopen(argv[1], "r");
    if (!yyin) {
        fprintf(stderr, "No se pudo abrir el archivo: %s\n", argv[1]);
        return 1;
    }

    yyparse();
    if (!huboErrorSintactico) cerrarSimbolos(0);
    qsort(msgs, nMsg, sizeof(Mensaje), compararMensajes);
    ok = (nErrores == 0);

    for (i = 0; i < nMsg; i++)
        printf("%s\t%d\t%s\n", etiquetaMensaje(msgs[i].clase), msgs[i].linea, msgs[i].texto);
    printf("CODIGO_INTERMEDIO\t%s\t%d\t%d\t%d\t%d\n", ok ? "correcto" : "incorrecto",
           ok ? nCuads : 0, ok ? nTemporales : 0, nErrores, nAdvertencias);
    if (ok) {
        for (i = 0; i < nCuads; i++)
            printf("CUADRUPLA\t%d\t%s\t%s\t%s\t%s\n", i + 1,
                   cuads[i].op, cuads[i].arg1, cuads[i].arg2, cuads[i].res);
        for (i = 0; i < nCuads; i++) {
            printf("TAC\t");
            imprimirInstruccion(&cuads[i]);
            printf("\n");
        }
    }
    return ok ? 0 : 1;
}
