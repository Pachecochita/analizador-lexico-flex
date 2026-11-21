/*
 * traductor.y
 * Traductor de MiniLang a C++ o a JavaScript (Flex + Bison).
 *
 * Funciona en una sola pasada, igual que el analizador semantico:
 *   1. Bison reconoce la gramatica de MiniLang.
 *   2. Las acciones comprueban declaraciones y tipos (tabla de simbolos).
 *   3. Esas mismas acciones van escribiendo el codigo del lenguaje destino.
 * Si el programa tiene algun error no se genera codigo.
 *
 * Uso:  traductor archivo.txt cpp|js [--crudo]
 */

%code requires {
    /* Atributos sintetizados de una expresion */
    typedef struct {
        int   tipo;      /* T_INT, T_FLOAT o T_ERROR */
        int   cero;      /* 1 si es la constante 0 (division entre cero) */
        int   linea;     /* linea donde termina la expresion */
        int   rel;       /* 1 si en la raiz es una comparacion */
        int   conParen;  /* 1 si el codigo de esa comparacion ya va entre parentesis */
        char *codigo;    /* la expresion ya traducida al lenguaje destino */
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

#define D_CPP 0
#define D_JS  1

#define MAX_SIM 512
#define MAX_MSG 1024
#define MAX_NIVEL 63

/* Clases de mensaje */
#define M_ADVERTENCIA 0
#define M_SEMANTICO   1
#define M_SINTACTICO  2
#define M_LEXICO      3
#define M_TRADUCCION  4   /* el programa es valido en MiniLang pero no se puede traducir bien */

typedef struct {
    char nombre[64];
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

static Simbolo tabla[MAX_SIM];
static int nSim = 0;
static Mensaje msgs[MAX_MSG];
static int nMsg = 0;
static int nErrores = 0, nAdvertencias = 0;

static int pilaAmbitos[MAX_NIVEL + 1];
static int nivelActual = 0;
static int contadorAmbitos = 0;
static int huboErrorSintactico = 0;

static int destino = D_CPP;

int yylex(void);
void yyerror(const char *s);
void errorLexico(int linea, const char *texto);
extern int yylineno;
extern char *yytext;

/* ---------- Utilidades de texto ---------- */

static char *vfmt(const char *f, va_list ap) {
    size_t cap = 128;
    for (;;) {
        va_list copia;
        char *s = malloc(cap);
        int n;
        if (!s) { fprintf(stderr, "sin memoria\n"); exit(2); }
        va_copy(copia, ap);
        n = vsnprintf(s, cap, f, copia);
        va_end(copia);
        if (n >= 0 && (size_t)n < cap) return s;
        free(s);
        cap = (n >= 0) ? (size_t)n + 1 : cap * 2;
    }
}

/* Como sprintf, pero reserva la memoria que haga falta */
static char *fmt(const char *f, ...) {
    va_list ap;
    char *s;
    va_start(ap, f);
    s = vfmt(f, ap);
    va_end(ap);
    return s;
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

/* ---------- Codigo generado ---------- */

static char **lineas = NULL;
static int nLineas = 0, capLineas = 0;
static int sangria = 0;   /* nivel de sangria actual (4 espacios por nivel) */

static char *conSangria(const char *texto) {
    size_t n = (size_t)sangria * 4;
    char *l = malloc(n + strlen(texto) + 1);
    if (!l) { fprintf(stderr, "sin memoria\n"); exit(2); }
    memset(l, ' ', n);
    strcpy(l + n, texto);
    return l;
}

static void emitir(const char *f, ...) {
    va_list ap;
    char *texto;
    va_start(ap, f);
    texto = vfmt(f, ap);
    va_end(ap);
    if (nLineas == capLineas) {
        capLineas = capLineas ? capLineas * 2 : 64;
        lineas = realloc(lineas, (size_t)capLineas * sizeof(char *));
        if (!lineas) { fprintf(stderr, "sin memoria\n"); exit(2); }
    }
    lineas[nLineas++] = conSangria(texto);
    free(texto);
}

/* Cuando aparece un else, la llave "}" del if pasa a ser "} else {" */
static void abrirElse(void) {
    if (nLineas == 0) return;
    free(lineas[nLineas - 1]);
    lineas[nLineas - 1] = conSangria("} else {");
}

/* ---------- Nombres de variables en el lenguaje destino ---------- */

static const char *reservadasCpp[] = {
    "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool",
    "break", "case", "catch", "char", "char8_t", "char16_t", "char32_t", "class", "compl",
    "concept", "const", "consteval", "constexpr", "constinit", "const_cast", "continue",
    "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do", "double",
    "dynamic_cast", "enum", "explicit", "export", "extern", "false", "for", "friend",
    "goto", "inline", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq",
    "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register",
    "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static",
    "static_assert", "static_cast", "struct", "switch", "template", "this", "thread_local",
    "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using",
    "virtual", "void", "volatile", "wchar_t", "xor", "xor_eq",
    "NULL", "EOF", "linux", "unix",
    NULL
};

static const char *reservadasJs[] = {
    "await", "break", "case", "catch", "class", "const", "continue", "debugger", "default",
    "delete", "do", "enum", "export", "extends", "false", "finally", "for", "function",
    "implements", "import", "in", "instanceof", "interface", "let", "new", "null",
    "package", "private", "protected", "public", "return", "static", "super", "switch",
    "this", "throw", "true", "try", "typeof", "var", "void", "with", "yield",
    "arguments", "eval", "undefined", "NaN", "Infinity",
    "Math", "console", "Number",   /* los usa el codigo generado */
    NULL
};

static int esReservada(const char *n) {
    const char **p = (destino == D_CPP) ? reservadasCpp : reservadasJs;
    for (; *p; p++)
        if (strcmp(*p, n) == 0) return 1;
    return 0;
}

static int terminaEnMini(const char *s) {
    size_t n = strlen(s);
    return n >= 5 && strcmp(s + n - 5, "_mini") == 0;
}

/* Un nombre valido en MiniLang puede ser palabra reservada en el destino
 * (por ejemplo "class"). En ese caso se le agrega "_mini". Tambien se
 * cambian los que ya terminan en "_mini", para que dos nombres distintos
 * nunca lleguen a quedar iguales. */
static char *nombreDestino(const char *n) {
    if (esReservada(n) || terminaEnMini(n)) return fmt("%s_mini", n);
    return fmt("%s", n);
}

/* "007" pasa a "7": en C++ el cero inicial significa octal y en JavaScript
 * estricto es un error de sintaxis. */
static char *normalizarNumero(const char *t) {
    while (t[0] == '0' && t[1] >= '0' && t[1] <= '9') t++;
    return fmt("%s", t);
}

/* ((a < b)) -> a < b, para que el if no quede con parentesis de mas */
static char *sinParentesisExternos(const char *c) {
    size_t n = strlen(c);
    char *r;
    while (n >= 2 && c[0] == '(' && c[n - 1] == ')') {
        int prof = 0, envuelve = 1;
        size_t i;
        for (i = 0; i < n; i++) {
            if (c[i] == '(') prof++;
            else if (c[i] == ')') prof--;
            if (prof == 0 && i < n - 1) { envuelve = 0; break; }
        }
        if (!envuelve) break;
        c++;
        n -= 2;
    }
    r = malloc(n + 1);
    if (!r) { fprintf(stderr, "sin memoria\n"); exit(2); }
    memcpy(r, c, n);
    r[n] = '\0';
    return r;
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
    /* En MiniLang ocultar una variable solo es una advertencia, pero al traducir
     * es un problema: en JavaScript la variable de adentro existe desde el
     * inicio del bloque y usar la de afuera antes de declararla falla, y en
     * C++ "int x = x + 1" leeria la variable nueva en vez de la de afuera. */
    if (exterior >= 0)
        reportar(M_TRADUCCION, linea,
                 "la variable '%s' oculta a otra del bloque exterior (linea %d); usa otro nombre para poder traducir",
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

/* ---------- Expresiones: tipo y codigo ---------- */

/* En MiniLang una comparacion vale 0 o 1. En JavaScript da true o false,
 * asi que cuando se usa como valor se convierte con Number(). */
static char *valor(Expr e) {
    if (destino == D_JS && e.rel)
        return e.conParen ? fmt("Number%s", e.codigo) : fmt("Number(%s)", e.codigo);
    return e.codigo;
}

static Expr usarVariable(const char *nombre, int linea) {
    Expr e;
    int i = buscar(nombre);
    e.cero = 0;
    e.linea = linea;
    e.rel = 0;
    e.conParen = 0;
    e.codigo = nombreDestino(nombre);
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

static Expr literal(int tipo, double v, const char *texto, int linea) {
    Expr e;
    e.tipo = tipo;
    e.cero = (v == 0);
    e.linea = linea;
    e.rel = 0;
    e.conParen = 0;
    e.codigo = normalizarNumero(texto);
    if (tipo == T_INT && v > 2147483647.0)
        reportar(M_TRADUCCION, linea,
                 "el numero %s es demasiado grande para un int de 32 bits", e.codigo);
    return e;
}

static Expr parentesis(Expr a) {
    Expr r = a;
    r.codigo = fmt("(%s)", a.codigo);
    if (a.rel) r.conParen = 1;
    return r;
}

/* int op int -> int ; si alguno es float -> float (promocion).
 * La division entre dos int es entera: en C++ ya lo es, en JavaScript
 * hay que truncar el resultado. */
static Expr aritmetica(Expr a, char op, Expr b) {
    Expr r;
    r.cero = 0;
    r.linea = b.linea;
    r.rel = 0;
    r.conParen = 0;
    if (a.tipo == T_ERROR || b.tipo == T_ERROR) r.tipo = T_ERROR;
    else if (a.tipo == T_FLOAT || b.tipo == T_FLOAT) r.tipo = T_FLOAT;
    else r.tipo = T_INT;

    if (op == '/' && destino == D_JS && a.tipo == T_INT && b.tipo == T_INT)
        r.codigo = fmt("Math.trunc(%s / %s)", valor(a), valor(b));
    else
        r.codigo = fmt("%s %c %s", valor(a), op, valor(b));
    return r;
}

/* Las comparaciones producen un int (0 o 1) */
static Expr relacional(Expr a, int esIgualdad, int linea, const char *op, Expr b) {
    Expr r;
    const char *opDestino = op;
    r.cero = 0;
    r.linea = b.linea;
    r.rel = 1;
    r.conParen = 0;
    if (destino == D_JS) {
        if (strcmp(op, "==") == 0) opDestino = "===";
        else if (strcmp(op, "!=") == 0) opDestino = "!==";
    }
    r.codigo = fmt("%s %s %s", valor(a), opDestino, valor(b));
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

/* ---------- Sentencias ---------- */

/* Una variable declarada sin valor arranca en 0, asi las dos traducciones
 * se comportan igual (en JavaScript sin valor seria "undefined" y en C++ basura). */
static void emitirDeclaracion(int tipo, const char *nombre, const char *valorCodigo) {
    char *n = nombreDestino(nombre);
    if (destino == D_JS) emitir("let %s = %s;", n, valorCodigo);
    else emitir("%s %s = %s;", tipo == T_INT ? "int" : "double", n, valorCodigo);
    free(n);
}

static void emitirAsignacion(const char *nombre, Expr e) {
    char *n = nombreDestino(nombre);
    emitir("%s = %s;", n, valor(e));
    free(n);
}

static void emitirPrint(Expr e) {
    if (destino == D_JS)
        emitir("console.log(%s);", valor(e));
    else if (e.rel && !e.conParen)
        /* en C++ "<<" pesa mas que "<": "cout << a < b" no compila */
        emitir("std::cout << (%s) << std::endl;", e.codigo);
    else
        emitir("std::cout << %s << std::endl;", e.codigo);
}

static void emitirControl(const char *palabra, Expr cond) {
    char *c = sinParentesisExternos(cond.codigo);
    emitir("%s (%s) {", palabra, c);
    free(c);
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

declaracion:
      tipo ID
        {
            declarar($2.nombre, $1, $2.linea, 0);
            emitirDeclaracion($1, $2.nombre, "0");
        }
    | tipo ID ASIG expresion
        {
            if ($1 == T_INT && $4.tipo == T_FLOAT)
                reportar(M_SEMANTICO, $2.linea,
                         "no se puede inicializar la variable int '%s' con un valor float (se pierde la parte decimal)",
                         $2.nombre);
            declarar($2.nombre, $1, $2.linea, 1);
            emitirDeclaracion($1, $2.nombre, valor($4));
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
            emitirAsignacion($1.nombre, $3);
        }
    ;

bloque:
      '{' { entrarAmbito(); sangria++; }
      lista_sentencias
      '}' { salirAmbito(); sangria--; emitir("}"); }
    ;

if_sentencia:
      IF '(' expresion ')' { emitirControl("if", $3); } bloque else_opcional
    ;

else_opcional:
      %empty
    | ELSE { abrirElse(); } bloque
    ;

while_sentencia:
      WHILE '(' expresion ')' { emitirControl("while", $3); } bloque
    ;

print_sentencia:
      PRINT '(' expresion ')'   { emitirPrint($3); }
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
    | '(' expresion ')'         { $$ = parentesis($2); }
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
        case M_TRADUCCION:  return "ERROR_TRADUCCION";
        default:            return "ERROR_LEXICO";
    }
}

/* Escribe el programa completo: cabecera + cuerpo + cierre */
static void imprimirCodigo(const char *p) {
    int i;
    if (destino == D_CPP) {
        printf("%s// Traducido de MiniLang a C++\n", p);
        printf("%s#include <iostream>\n", p);
        printf("%s\n", p);
        printf("%sint main() {\n", p);
        for (i = 0; i < nLineas; i++) printf("%s%s\n", p, lineas[i]);
        printf("%s    return 0;\n", p);
        printf("%s}\n", p);
    } else {
        printf("%s// Traducido de MiniLang a JavaScript\n", p);
        printf("%s\"use strict\";\n", p);
        printf("%s\n", p);
        for (i = 0; i < nLineas; i++) printf("%s%s\n", p, lineas[i]);
    }
}

static int uso(void) {
    fprintf(stderr, "Uso: traductor archivo.txt cpp|js [--crudo]\n");
    return 2;
}

int main(int argc, char **argv) {
    extern FILE *yyin;
    int i, crudo = 0, ok;
    const char *archivo = NULL, *lenguaje = NULL;

    for (i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--crudo") == 0) crudo = 1;
        else if (!archivo) archivo = argv[i];
        else if (!lenguaje) lenguaje = argv[i];
        else return uso();
    }
    if (!archivo || !lenguaje) return uso();
    if (strcmp(lenguaje, "cpp") == 0) destino = D_CPP;
    else if (strcmp(lenguaje, "js") == 0) destino = D_JS;
    else return uso();

    yyin = fopen(archivo, "r");
    if (!yyin) {
        fprintf(stderr, "No se pudo abrir el archivo: %s\n", archivo);
        return 1;
    }

    sangria = (destino == D_CPP) ? 1 : 0;   /* en C++ el codigo va dentro de main */
    yyparse();
    if (!huboErrorSintactico) cerrarSimbolos(0);
    qsort(msgs, nMsg, sizeof(Mensaje), compararMensajes);
    ok = (nErrores == 0);

    if (crudo) {
        if (!ok) {
            for (i = 0; i < nMsg; i++)
                fprintf(stderr, "%s\t%d\t%s\n", etiquetaMensaje(msgs[i].clase), msgs[i].linea, msgs[i].texto);
            return 1;
        }
        imprimirCodigo("");
        return 0;
    }

    for (i = 0; i < nMsg; i++)
        printf("%s\t%d\t%s\n", etiquetaMensaje(msgs[i].clase), msgs[i].linea, msgs[i].texto);
    printf("TRADUCCION\t%s\t%s\t%d\t%d\n", ok ? "correcta" : "incorrecta",
           destino == D_CPP ? "C++" : "JavaScript", nErrores, nAdvertencias);
    if (ok) imprimirCodigo("CODIGO\t");
    return ok ? 0 : 1;
}
