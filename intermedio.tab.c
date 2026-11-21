/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1





# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "intermedio.tab.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_INT = 3,                        /* INT  */
  YYSYMBOL_FLOAT = 4,                      /* FLOAT  */
  YYSYMBOL_IF = 5,                         /* IF  */
  YYSYMBOL_ELSE = 6,                       /* ELSE  */
  YYSYMBOL_WHILE = 7,                      /* WHILE  */
  YYSYMBOL_PRINT = 8,                      /* PRINT  */
  YYSYMBOL_ID = 9,                         /* ID  */
  YYSYMBOL_NUM_ENTERO = 10,                /* NUM_ENTERO  */
  YYSYMBOL_NUM_DECIMAL = 11,               /* NUM_DECIMAL  */
  YYSYMBOL_OPREL = 12,                     /* OPREL  */
  YYSYMBOL_ASIG = 13,                      /* ASIG  */
  YYSYMBOL_14_ = 14,                       /* '+'  */
  YYSYMBOL_15_ = 15,                       /* '-'  */
  YYSYMBOL_16_ = 16,                       /* '*'  */
  YYSYMBOL_17_ = 17,                       /* '/'  */
  YYSYMBOL_18_ = 18,                       /* ';'  */
  YYSYMBOL_19_ = 19,                       /* '{'  */
  YYSYMBOL_20_ = 20,                       /* '}'  */
  YYSYMBOL_21_ = 21,                       /* '('  */
  YYSYMBOL_22_ = 22,                       /* ')'  */
  YYSYMBOL_YYACCEPT = 23,                  /* $accept  */
  YYSYMBOL_programa = 24,                  /* programa  */
  YYSYMBOL_lista_sentencias = 25,          /* lista_sentencias  */
  YYSYMBOL_sentencia = 26,                 /* sentencia  */
  YYSYMBOL_tipo = 27,                      /* tipo  */
  YYSYMBOL_declaracion = 28,               /* declaracion  */
  YYSYMBOL_asignacion = 29,                /* asignacion  */
  YYSYMBOL_bloque = 30,                    /* bloque  */
  YYSYMBOL_31_1 = 31,                      /* $@1  */
  YYSYMBOL_if_sentencia = 32,              /* if_sentencia  */
  YYSYMBOL_33_2 = 33,                      /* $@2  */
  YYSYMBOL_else_opcional = 34,             /* else_opcional  */
  YYSYMBOL_35_3 = 35,                      /* $@3  */
  YYSYMBOL_while_sentencia = 36,           /* while_sentencia  */
  YYSYMBOL_37_4 = 37,                      /* $@4  */
  YYSYMBOL_38_5 = 38,                      /* $@5  */
  YYSYMBOL_print_sentencia = 39,           /* print_sentencia  */
  YYSYMBOL_expresion = 40                  /* expresion  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;



/* Unqualified %code blocks.  */
#line 36 "intermedio.y"

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


#line 467 "intermedio.tab.c"

#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_int8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  3
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   83

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  23
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  18
/* YYNRULES -- Number of rules.  */
#define YYNRULES  34
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  63

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   268


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      21,    22,    16,    14,     2,    15,     2,    17,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,    18,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    19,     2,    20,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_int16 yyrline[] =
{
       0,   384,   384,   388,   389,   393,   394,   395,   396,   397,
     401,   402,   407,   413,   426,   443,   443,   452,   451,   457,
     460,   459,   469,   471,   468,   478,   482,   483,   484,   485,
     491,   492,   493,   494,   495
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "INT", "FLOAT", "IF",
  "ELSE", "WHILE", "PRINT", "ID", "NUM_ENTERO", "NUM_DECIMAL", "OPREL",
  "ASIG", "'+'", "'-'", "'*'", "'/'", "';'", "'{'", "'}'", "'('", "')'",
  "$accept", "programa", "lista_sentencias", "sentencia", "tipo",
  "declaracion", "asignacion", "bloque", "$@1", "if_sentencia", "$@2",
  "else_opcional", "$@3", "while_sentencia", "$@4", "$@5",
  "print_sentencia", "expresion", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-53)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  ((Yyn) == YYTABLE_NINF)

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int8 yypact[] =
{
     -53,    10,    62,   -53,   -53,   -53,    -9,   -53,    -8,    11,
     -53,    19,    12,    23,   -53,   -53,    29,    -6,    14,    -6,
      -6,    24,   -53,   -53,   -53,   -53,   -53,   -53,    -6,    17,
      -6,    28,    60,    -6,    37,    -6,    -6,    -6,    -6,    -6,
     -53,    46,   -53,    60,   -53,    66,   -10,   -10,   -53,   -53,
      27,   -53,   -53,    30,    27,   -53,   -53,   -53,   -53,    18,
      27,   -53,   -53
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       3,     0,     2,     1,    10,    11,     0,    22,     0,     0,
       4,     0,     0,     0,     7,     8,     0,     0,     0,     0,
       0,    12,     5,     6,     9,    32,    33,    34,     0,     0,
       0,     0,    14,     0,     0,     0,     0,     0,     0,     0,
      17,     0,    25,    13,    31,    30,    26,    27,    28,    29,
       0,    23,    15,    19,     0,     3,    20,    18,    24,     0,
       0,    16,    21
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -53,   -53,    -7,   -53,   -53,   -53,   -53,   -52,   -53,   -53,
     -53,   -53,   -53,   -53,   -53,   -53,   -53,   -19
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
       0,     1,     2,    10,    11,    12,    13,    53,    55,    14,
      50,    57,    60,    15,    18,    54,    16,    29
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int8 yytable[] =
{
      31,    32,    58,    25,    26,    27,    38,    39,    62,    34,
       3,    41,    17,    19,    43,    28,    45,    46,    47,    48,
      49,     4,     5,     6,    20,     7,     8,     9,    21,    35,
      22,    36,    37,    38,    39,    30,    56,    33,    61,    40,
      35,    23,    36,    37,    38,    39,    52,    24,    59,    35,
      42,    36,    37,    38,    39,     0,     0,     0,    35,    44,
      36,    37,    38,    39,     0,     4,     5,     6,    51,     7,
       8,     9,    35,     0,    36,    37,    38,    39,    -1,     0,
      36,    37,    38,    39
};

static const yytype_int8 yycheck[] =
{
      19,    20,    54,     9,    10,    11,    16,    17,    60,    28,
       0,    30,    21,    21,    33,    21,    35,    36,    37,    38,
      39,     3,     4,     5,    13,     7,     8,     9,     9,    12,
      18,    14,    15,    16,    17,    21,     6,    13,    20,    22,
      12,    18,    14,    15,    16,    17,    19,    18,    55,    12,
      22,    14,    15,    16,    17,    -1,    -1,    -1,    12,    22,
      14,    15,    16,    17,    -1,     3,     4,     5,    22,     7,
       8,     9,    12,    -1,    14,    15,    16,    17,    12,    -1,
      14,    15,    16,    17
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,    24,    25,     0,     3,     4,     5,     7,     8,     9,
      26,    27,    28,    29,    32,    36,    39,    21,    37,    21,
      13,     9,    18,    18,    18,     9,    10,    11,    21,    40,
      21,    40,    40,    13,    40,    12,    14,    15,    16,    17,
      22,    40,    22,    40,    22,    40,    40,    40,    40,    40,
      33,    22,    19,    30,    38,    31,     6,    34,    30,    25,
      35,    20,    30
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    23,    24,    25,    25,    26,    26,    26,    26,    26,
      27,    27,    28,    28,    29,    31,    30,    33,    32,    34,
      35,    34,    37,    38,    36,    39,    40,    40,    40,    40,
      40,    40,    40,    40,    40
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     1,     0,     2,     2,     2,     1,     1,     2,
       1,     1,     2,     4,     3,     0,     4,     0,     7,     0,
       0,     3,     0,     0,     7,     4,     3,     3,     3,     3,
       3,     3,     1,     1,     1
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)




# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  yy_symbol_value_print (yyo, yykind, yyvaluep);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp,
                 int yyrule)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)]);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep)
{
  YY_USE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/* Lookahead token kind.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;




/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 10: /* tipo: INT  */
#line 401 "intermedio.y"
             { (yyval.tipoDecl) = T_INT; }
#line 1458 "intermedio.tab.c"
    break;

  case 11: /* tipo: FLOAT  */
#line 402 "intermedio.y"
             { (yyval.tipoDecl) = T_FLOAT; }
#line 1464 "intermedio.tab.c"
    break;

  case 12: /* declaracion: tipo ID  */
#line 408 "intermedio.y"
        {
            declarar((yyvsp[0].id).nombre, (yyvsp[-1].tipoDecl), (yyvsp[0].id).linea, 0);
            { int i = buscarEnAmbitoActual((yyvsp[0].id).nombre);
              if (i >= 0) cuad("=", "0", "-", tabla[i].tac); }
        }
#line 1474 "intermedio.tab.c"
    break;

  case 13: /* declaracion: tipo ID ASIG expresion  */
#line 414 "intermedio.y"
        {
            if ((yyvsp[-3].tipoDecl) == T_INT && (yyvsp[0].expr).tipo == T_FLOAT)
                reportar(M_SEMANTICO, (yyvsp[-2].id).linea,
                         "no se puede inicializar la variable int '%s' con un valor float (se pierde la parte decimal)",
                         (yyvsp[-2].id).nombre);
            declarar((yyvsp[-2].id).nombre, (yyvsp[-3].tipoDecl), (yyvsp[-2].id).linea, 1);
            { int i = buscarEnAmbitoActual((yyvsp[-2].id).nombre);
              if (i >= 0) cuad("=", (yyvsp[0].expr).lugar, "-", tabla[i].tac); }
        }
#line 1488 "intermedio.tab.c"
    break;

  case 14: /* asignacion: ID ASIG expresion  */
#line 427 "intermedio.y"
        {
            int i = buscar((yyvsp[-2].id).nombre);
            if (i < 0) {
                reportar(M_SEMANTICO, (yyvsp[-2].id).linea, "variable '%s' sin declarar", (yyvsp[-2].id).nombre);
            } else {
                if (tabla[i].tipo == T_INT && (yyvsp[0].expr).tipo == T_FLOAT)
                    reportar(M_SEMANTICO, (yyvsp[-2].id).linea,
                             "no se puede asignar un valor float a la variable int '%s' (se pierde la parte decimal)",
                             (yyvsp[-2].id).nombre);
                tabla[i].inicializada = 1;
                cuad("=", (yyvsp[0].expr).lugar, "-", tabla[i].tac);
            }
        }
#line 1506 "intermedio.tab.c"
    break;

  case 15: /* $@1: %empty  */
#line 443 "intermedio.y"
          { entrarAmbito(); }
#line 1512 "intermedio.tab.c"
    break;

  case 16: /* bloque: '{' $@1 lista_sentencias '}'  */
#line 445 "intermedio.y"
          { salirAmbito(); }
#line 1518 "intermedio.tab.c"
    break;

  case 17: /* $@2: %empty  */
#line 452 "intermedio.y"
        { int l = nuevaEtiqueta(); saltarSiFalso((yyvsp[-1].expr).lugar, l); apilar(l); }
#line 1524 "intermedio.tab.c"
    break;

  case 19: /* else_opcional: %empty  */
#line 458 "intermedio.y"
        { ponerEtiqueta(desapilar()); }
#line 1530 "intermedio.tab.c"
    break;

  case 20: /* $@3: %empty  */
#line 460 "intermedio.y"
        { int lFin = nuevaEtiqueta(), lElse = desapilar();
          saltarA(lFin); ponerEtiqueta(lElse); apilar(lFin); }
#line 1537 "intermedio.tab.c"
    break;

  case 21: /* else_opcional: ELSE $@3 bloque  */
#line 463 "intermedio.y"
        { ponerEtiqueta(desapilar()); }
#line 1543 "intermedio.tab.c"
    break;

  case 22: /* $@4: %empty  */
#line 469 "intermedio.y"
        { int l = nuevaEtiqueta(); ponerEtiqueta(l); apilar(l); }
#line 1549 "intermedio.tab.c"
    break;

  case 23: /* $@5: %empty  */
#line 471 "intermedio.y"
        { int l = nuevaEtiqueta(); saltarSiFalso((yyvsp[-1].expr).lugar, l); apilar(l); }
#line 1555 "intermedio.tab.c"
    break;

  case 24: /* while_sentencia: WHILE $@4 '(' expresion ')' $@5 bloque  */
#line 473 "intermedio.y"
        { int lFin = desapilar(), lInicio = desapilar();
          saltarA(lInicio); ponerEtiqueta(lFin); }
#line 1562 "intermedio.tab.c"
    break;

  case 25: /* print_sentencia: PRINT '(' expresion ')'  */
#line 478 "intermedio.y"
                                { cuad("print", (yyvsp[-1].expr).lugar, "-", "-"); }
#line 1568 "intermedio.tab.c"
    break;

  case 26: /* expresion: expresion '+' expresion  */
#line 482 "intermedio.y"
                                { (yyval.expr) = aritmetica((yyvsp[-2].expr), '+', (yyvsp[0].expr)); }
#line 1574 "intermedio.tab.c"
    break;

  case 27: /* expresion: expresion '-' expresion  */
#line 483 "intermedio.y"
                                { (yyval.expr) = aritmetica((yyvsp[-2].expr), '-', (yyvsp[0].expr)); }
#line 1580 "intermedio.tab.c"
    break;

  case 28: /* expresion: expresion '*' expresion  */
#line 484 "intermedio.y"
                                { (yyval.expr) = aritmetica((yyvsp[-2].expr), '*', (yyvsp[0].expr)); }
#line 1586 "intermedio.tab.c"
    break;

  case 29: /* expresion: expresion '/' expresion  */
#line 486 "intermedio.y"
        {
            if ((yyvsp[0].expr).cero)
                reportar(M_SEMANTICO, (yyvsp[0].expr).linea, "no se puede dividir entre cero");
            (yyval.expr) = aritmetica((yyvsp[-2].expr), '/', (yyvsp[0].expr));
        }
#line 1596 "intermedio.tab.c"
    break;

  case 30: /* expresion: expresion OPREL expresion  */
#line 491 "intermedio.y"
                                { (yyval.expr) = relacional((yyvsp[-2].expr), (yyvsp[-1].rel).esIgualdad, (yyvsp[-1].rel).linea, (yyvsp[-1].rel).op, (yyvsp[0].expr)); }
#line 1602 "intermedio.tab.c"
    break;

  case 31: /* expresion: '(' expresion ')'  */
#line 492 "intermedio.y"
                                { (yyval.expr) = (yyvsp[-1].expr); }
#line 1608 "intermedio.tab.c"
    break;

  case 32: /* expresion: ID  */
#line 493 "intermedio.y"
                                { (yyval.expr) = usarVariable((yyvsp[0].id).nombre, (yyvsp[0].id).linea); }
#line 1614 "intermedio.tab.c"
    break;

  case 33: /* expresion: NUM_ENTERO  */
#line 494 "intermedio.y"
                                { (yyval.expr) = literal(T_INT,   (yyvsp[0].num).valor, (yyvsp[0].num).texto, (yyvsp[0].num).linea); }
#line 1620 "intermedio.tab.c"
    break;

  case 34: /* expresion: NUM_DECIMAL  */
#line 495 "intermedio.y"
                                { (yyval.expr) = literal(T_FLOAT, (yyvsp[0].num).valor, (yyvsp[0].num).texto, (yyvsp[0].num).linea); }
#line 1626 "intermedio.tab.c"
    break;


#line 1630 "intermedio.tab.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (YY_("syntax error"));
    }

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 498 "intermedio.y"


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
