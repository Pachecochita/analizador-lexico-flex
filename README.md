# Analizadores Léxico, Sintáctico y Semántico - MiniLang

Tres analizadores para el lenguaje de prueba **MiniLang**:

- **Léxico**, construido con **Flex** (`analizador.l`).
- **Sintáctico**, construido con **Flex + Bison** (`lexico_sintactico.l` + `sintactico.y`).
- **Semántico**, construido con **Flex + Bison** (`lexico_semantico.l` + `semantico.y`).

Una sola interfaz gráfica en **Python (Tkinter)** con tres pestañas llama a los tres ejecutables.

Proyecto de la asignatura de Compiladores, UTESA.

## Contenido del repositorio

```
analizador-lexico-flex/
├── analizador.l               # Especificación Flex del analizador lexico (imprime cada token)
├── analizador.exe             # Ejecutable del analizador lexico
├── lexico_sintactico.l        # Especificación Flex que alimenta tokens a Bison (sin imprimir)
├── sintactico.y                # Gramática Bison del analizador sintactico
├── sintactico.exe              # Ejecutable del analizador sintactico
├── lexico_semantico.l          # Especificación Flex del semantico (los tokens llevan valor)
├── semantico.y                 # Gramática Bison con las acciones semanticas
├── semantico.exe               # Ejecutable del analizador semantico
├── gui.py                      # Interfaz gráfica (Python / Tkinter, 3 pestañas)
├── prueba.txt                  # Archivo de prueba rápida (lexico)
├── pruebas/                    # Casos de prueba y resultados esperados
│   ├── prueba1_declaraciones.txt ... prueba5_programa_completo.txt
│   ├── esperado/                # Salida esperada del analizador lexico
│   └── sintactico/              # Casos de prueba del analizador sintactico
│       ├── valida1_declaraciones.txt, valida2_control.txt, valida3_expresiones.txt
│       ├── invalida1_falta_puntocoma.txt, invalida2_llave_sin_cerrar.txt,
│       │   invalida3_parentesis_mal_puesto.txt, invalida4_asignacion_vacia.txt
│       └── esperado/            # Salida esperada de cada caso
│   └── semantico/               # Casos de prueba del analizador semantico
│       ├── valida1_tipos.txt, valida2_ambitos.txt, valida3_if_else.txt
│       ├── advertencias1.txt, demo_errores_mixtos.txt
│       ├── invalida1_no_declarada.txt, invalida2_tipos.txt, invalida3_redeclaracion.txt,
│       │   invalida4_division_cero.txt, invalida5_sintaxis.txt
│       └── esperado/            # Salida esperada de cada caso
└── README.md
```

## Cómo ejecutar (Windows)

Requisito: tener **Python 3** instalado (Tkinter viene incluido).

1. Descargar o clonar el repositorio.
2. Dejar `gui.py`, `analizador.exe`, `sintactico.exe` y `semantico.exe` en la misma carpeta.
3. Abrir una terminal en esa carpeta y ejecutar:

```
python gui.py
```

4. En la ventana, cambiar entre las pestañas **Analisis Lexico**, **Analisis Sintactico** y
   **Analisis Semantico**. En cada una: escribir código o usar **Cargar archivo**, y presionar **Analizar**.

## Cómo compilar los analizadores desde el código fuente

Herramientas: **MSYS2** con `flex`, `bison` y `gcc` (https://www.msys2.org).

1. En la terminal *MSYS2 UCRT64*:
   ```
   pacman -S mingw-w64-ucrt-x86_64-toolchain flex bison
   ```
2. Agregar al PATH de Windows estas dos rutas y reiniciar la terminal / VS Code:
   - `C:\msys64\ucrt64\bin` (gcc, bison)
   - `C:\msys64\usr\bin` (flex)
3. Verificar:
   ```
   flex --version
   gcc --version
   bison --version
   ```
4. Compilar el analizador léxico, dentro de la carpeta del proyecto:
   ```
   flex analizador.l
   gcc lex.yy.c -o analizador.exe
   ```
5. Compilar el analizador sintáctico (genera primero las tablas de Bison,
   después el lexer que las usa, y al final une los dos `.c`):
   ```
   bison -d sintactico.y
   flex lexico_sintactico.l
   gcc sintactico.tab.c lex.yy.c -o sintactico.exe
   ```
   `bison -d` genera `sintactico.tab.c` y `sintactico.tab.h` (las definiciones
   de token que usa `lexico_sintactico.l`). El segundo `flex` sobrescribe el
   `lex.yy.c` del paso 4; si se quiere compilar ambos analizadores después de
   esto, hay que repetir el paso 4 también.
6. Compilar el analizador semántico. Aquí los archivos generados llevan nombre propio
   (`-o`), así que no pisa a los anteriores y el orden ya no importa:
   ```
   bison -d -o semantico.tab.c semantico.y
   flex -o lex_semantico.c lexico_semantico.l
   gcc semantico.tab.c lex_semantico.c -o semantico.exe
   ```
7. Pruebas rápidas por consola (opcional):
   ```
   .\analizador.exe prueba.txt
   .\sintactico.exe pruebas\sintactico\valida1_declaraciones.txt
   .\semantico.exe pruebas\semantico\demo_errores_mixtos.txt
   ```

## Lenguaje de prueba: "MiniLang"

Lenguaje simplificado de tipo C, pensado para ejercitar los tres analizadores. La tabla de abajo
describe sus tokens (la parte léxica); la gramática y las reglas de tipos van más adelante.

| Categoría | Descripción | Expresión regular / Elementos |
|---|---|---|
| Palabras reservadas | Se reconocen antes que los identificadores | `int` `float` `if` `else` `while` `print` |
| Identificadores | Letra o `_`, seguido de letras, dígitos o `_` | `[a-zA-Z_][a-zA-Z0-9_]*` |
| Números enteros | Uno o más dígitos | `[0-9]+` |
| Números decimales | Dígitos, punto, dígitos | `[0-9]+\.[0-9]+` |
| Operadores relacionales | | `==` `!=` `<` `>` `<=` `>=` |
| Operador de asignación | | `=` |
| Operadores aritméticos | | `+` `-` `*` `/` |
| Símbolos | | `(` `)` `{` `}` `;` `,` |
| Comentarios (se ignoran) | Línea y bloque | `// ...` y `/* ... */` |
| Espacios en blanco (se ignoran) | Espacio, tab, salto de línea | `[ \t\r\n]+` |
| Error léxico | Cualquier otro carácter | `.` (por ejemplo `@`, `$`, `#`, `!` solo) |

### Tipos de token que produce el analizador

`PALABRA_RESERVADA`, `IDENTIFICADOR`, `NUMERO_ENTERO`, `NUMERO_DECIMAL`, `OP_RELACIONAL`,
`OP_ASIGNACION`, `OP_SUMA`, `OP_RESTA`, `OP_MULTIPLICACION`, `OP_DIVISION`,
`PARENTESIS_IZQ`, `PARENTESIS_DER`, `LLAVE_IZQ`, `LLAVE_DER`, `PUNTO_COMA`, `COMA`, `ERROR_LEXICO`.

### Cómo decide Flex entre reglas

- Se elige siempre el **lexema más largo** posible (`>=` se reconoce completo y no como `>` y `=`).
- Si dos reglas reconocen la misma longitud, gana la que aparece **primero** en `analizador.l`
  (por eso `int` es palabra reservada y no identificador).

## Pruebas

Cada archivo de `pruebas/` tiene su salida esperada en `pruebas/esperado/`.
Para ejecutar una prueba: abrir `gui.py`, **Cargar archivo**, elegir el `.txt` y **Analizar**;
o por consola: `.\analizador.exe pruebas\prueba1_declaraciones.txt`.

| Prueba | Qué verifica | Tokens | Errores |
|---|---|---|---|
| `prueba1_declaraciones.txt` | Palabras reservadas, identificadores (incluye `_temp`, `valor2`), enteros y decimales | 25 | 0 |
| `prueba2_condicionales.txt` | `if`/`else`/`while` y los seis operadores relacionales | 71 | 0 |
| `prueba3_comentarios.txt` | Comentarios de línea y de bloque se ignoran | 15 | 0 |
| `prueba4_errores.txt` | Errores léxicos y casos límite | 44 | 5 |
| `prueba5_programa_completo.txt` | Programa completo con ciclo y condicional | 56 | 0 |

### Casos límite de `prueba4_errores.txt`

| Entrada | Resultado | Motivo |
|---|---|---|
| `5 @ 3` | `@` es `ERROR_LEXICO` | El carácter no pertenece al lenguaje |
| `3.` | `NUMERO_ENTERO 3` + `ERROR_LEXICO .` | Un decimal exige dígitos después del punto |
| `1.2.3` | `NUMERO_DECIMAL 1.2` + `ERROR_LEXICO .` + `NUMERO_ENTERO 3` | Reconoce el lexema más largo y sigue |
| `$valor` | `ERROR_LEXICO $` + `IDENTIFICADOR valor` | El error no detiene el análisis |
| `a ! b` | `!` es `ERROR_LEXICO` | Solo existe `!=`, no `!` suelto |
| `2abc` | `NUMERO_ENTERO 2` + `IDENTIFICADOR abc` | El analizador léxico no valida esto; lo detectaría el sintáctico |

## Gramática del analizador sintáctico (BNF simplificada)

```
programa          -> lista_sentencias

lista_sentencias   -> lista_sentencias sentencia
                    | (vacio)

sentencia          -> declaracion ';'
                    | asignacion ';'
                    | if_sentencia
                    | while_sentencia
                    | print_sentencia ';'

declaracion         -> tipo ID
                    | tipo ID '=' expresion

tipo                -> 'int' | 'float'

asignacion          -> ID '=' expresion

if_sentencia        -> 'if' '(' expresion ')' '{' lista_sentencias '}'
                    | 'if' '(' expresion ')' '{' lista_sentencias '}' 'else' '{' lista_sentencias '}'

while_sentencia     -> 'while' '(' expresion ')' '{' lista_sentencias '}'

print_sentencia     -> 'print' '(' expresion ')'

expresion           -> expresion '+' expresion
                    | expresion '-' expresion
                    | expresion '*' expresion
                    | expresion '/' expresion
                    | expresion OPREL expresion
                    | '(' expresion ')'
                    | ID | NUMERO_ENTERO | NUMERO_DECIMAL
```

`OPREL` agrupa `==`, `!=`, `<`, `>`, `<=`, `>=`.
Esta gramática reutiliza el mismo lenguaje MiniLang documentado arriba para el analizador léxico
(mismas palabras reservadas, identificadores, números y operadores); el sintáctico valida que
esos tokens aparezcan en un orden válido.

### Precedencia de operadores

Declarada en `sintactico.y` con `%left` y `%nonassoc`, de menor a mayor precedencia:

1. Operadores relacionales (`==`, `!=`, `<`, `>`, `<=`, `>=`) — no asociativos
2. `+` `-` — asociativos a la izquierda
3. `*` `/` — asociativos a la izquierda (se evalúan primero)

Así `2 + 3 * 4` se interpreta como `2 + (3 * 4)` y no como `(2 + 3) * 4`.

## Pruebas del analizador sintáctico

| Prueba | Qué verifica | Resultado esperado |
|---|---|---|
| `valida1_declaraciones.txt` | Declaraciones con y sin inicializar, asignación | Correcto |
| `valida2_control.txt` | `if`/`else`, `while`, operadores relacionales | Correcto |
| `valida3_expresiones.txt` | Expresiones con paréntesis anidados | Correcto |
| `invalida1_falta_puntocoma.txt` | Falta `;` al final de una declaración | Incorrecto (error de sintaxis) |
| `invalida2_llave_sin_cerrar.txt` | Bloque `{ }` sin cerrar | Incorrecto (error de sintaxis) |
| `invalida3_parentesis_mal_puesto.txt` | Falta `(` después de `while` | Incorrecto (error de sintaxis) |
| `invalida4_asignacion_vacia.txt` | Asignación sin expresión a la derecha | Incorrecto (error de sintaxis) |

Cada error reportado incluye el número de línea y el lexema donde Bison detectó el problema.

## Analizador semántico

El analizador sintáctico solo comprueba que las palabras estén en un orden válido. El semántico va un
paso más allá y comprueba que el programa **tenga sentido**: que las variables existan, que los tipos
sean compatibles, etc. Usa la misma gramática de MiniLang, pero cada regla lleva una acción en C que
consulta y actualiza una **tabla de símbolos** mientras Bison va reconociendo el programa
(traducción dirigida por la sintaxis).

### Qué verifica

| Verificación | Tipo de mensaje |
|---|---|
| Variable usada o asignada sin haberla declarado | Error |
| Variable declarada dos veces en el mismo bloque | Error |
| Asignar o inicializar un `int` con un valor `float` (se pierde la parte decimal) | Error |
| División entre la constante `0` o `0.0` | Error |
| Variable declarada que nunca se usa | Advertencia |
| Variable usada sin haberle dado valor | Advertencia |
| Variable que oculta a otra del mismo nombre en un bloque exterior | Advertencia |
| Comparar `float` con `==` o `!=` (puede ser inexacto) | Advertencia |

Un programa es **correcto** si no tiene errores; las advertencias no lo invalidan. Si el código tiene un
error léxico o sintáctico, también se reporta y el análisis se marca como incorrecto.

### Reglas de tipos

| Expresión | Tipo resultante |
|---|---|
| Literal entero (`5`) | `int` |
| Literal decimal (`2.5`) | `float` |
| Variable | El tipo con el que fue declarada |
| `int` `+ - * /` `int` | `int` |
| Si alguno de los dos es `float` | `float` (el `int` se promueve a `float`) |
| Comparación (`< > <= >= == !=`) | `int` (vale 0 o 1) |
| Expresión con un error previo | Se marca como error y no se repiten mensajes en cascada |

Asignar un `int` a una variable `float` es válido (promoción). Lo contrario es un error.

### Ámbitos

Cada bloque `{ ... }` de un `if`, `else` o `while` abre un ámbito nuevo. Una variable declarada dentro
del bloque deja de existir al cerrarlo; si se usa después, es un error de variable sin declarar.
Las variables de un bloque pueden tener el mismo nombre que las de uno exterior (la interior tiene
prioridad y se emite una advertencia).

### Atributos y acciones semánticas

Cada expresión calcula tres atributos a partir de sus hijas (atributos sintetizados): `tipo`, `cero`
(si es la constante 0) y `linea`.

| Producción | Acción semántica |
|---|---|
| `declaracion -> tipo ID` | Insertar `ID` en la tabla con ese tipo, sin valor inicial |
| `declaracion -> tipo ID = expresion` | Si el tipo es `int` y la expresión es `float`, error. Insertar `ID` con valor inicial |
| `asignacion -> ID = expresion` | Buscar `ID`; si no existe, error. Si es `int` y la expresión `float`, error. Marcarla como inicializada |
| `bloque -> { lista_sentencias }` | Al abrir, crear ámbito. Al cerrar, avisar de variables sin usar y cerrarlas |
| `expresion -> expresion op expresion` | Calcular el tipo según la tabla de reglas de tipos |
| `expresion -> expresion / expresion` | Además, si el divisor es la constante 0, error |
| `expresion -> ID` | Buscar `ID`; si no existe, error. Marcarla como usada. El tipo es el de la variable |
| `expresion -> NUM_ENTERO` / `NUM_DECIMAL` | Tipo `int` / `float` |

### Tabla de símbolos

Cada variable guarda: nombre, tipo, nivel de bloque (0 = global), línea donde se declaró, si tiene
valor inicial y si se usó. La interfaz la muestra completa al terminar el análisis, incluidas las
variables de bloques ya cerrados.

### Formato de salida (consola)

```
SIMBOLO<TAB>nombre<TAB>tipo<TAB>nivel<TAB>linea<TAB>inicializada<TAB>usada
ERROR_SEMANTICO | ERROR_SINTACTICO | ERROR_LEXICO | ADVERTENCIA <TAB>linea<TAB>mensaje
ANALISIS_SEMANTICO<TAB>correcto|incorrecto<TAB>total_errores<TAB>total_advertencias
```

### Pruebas del analizador semántico

Cada archivo de `pruebas/semantico/` tiene su salida esperada en `pruebas/semantico/esperado/`.

| Prueba | Qué verifica | Errores | Advertencias |
|---|---|---|---|
| `valida1_tipos.txt` | Promoción de `int` a `float` en expresiones | 0 | 0 |
| `valida2_ambitos.txt` | Variable declarada dentro de un `while` | 0 | 0 |
| `valida3_if_else.txt` | `if`/`else` con variables de distinto tipo | 0 | 0 |
| `advertencias1.txt` | Variable sin usar, sin valor, sombreada y `==` con `float` | 0 | 4 |
| `invalida1_no_declarada.txt` | Asignar y usar variables sin declarar | 2 | 0 |
| `invalida2_tipos.txt` | `float` hacia `int` en inicialización y asignación | 3 | 0 |
| `invalida3_redeclaracion.txt` | Misma variable declarada dos veces en un bloque | 2 | 0 |
| `invalida4_division_cero.txt` | División entre `0` y entre `0.0` | 2 | 0 |
| `invalida5_sintaxis.txt` | Falta una expresión: se reporta como error de sintaxis | 1 | 0 |
| `demo_errores_mixtos.txt` | Varios tipos de error y advertencia juntos | 3 | 2 |

### Limitaciones

- La división entre cero solo se detecta cuando el divisor es la constante `0` o `0.0`, no cuando
  el cero resulta de calcular algo como `2 - 2`.
- No se evalúan los valores de las expresiones, solo sus tipos.

