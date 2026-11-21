# Compilador MiniLang (Flex y Bison)

Un pequeño compilador para el lenguaje de prueba **MiniLang**, con estas partes:

- **Léxico**, construido con **Flex** (`analizador.l`).
- **Sintáctico**, construido con **Flex + Bison** (`lexico_sintactico.l` + `sintactico.y`).
- **Semántico**, construido con **Flex + Bison** (`lexico_semantico.l` + `semantico.y`).
- **Tabla de símbolos** (con ámbitos por bloque), que arma el analizador semántico y se muestra en su propia pestaña **Tabla de Simbolos**.
- **Generador de código intermedio** (código de tres direcciones, cuádruplas), con **Flex + Bison** (`lexico_intermedio.l` + `intermedio.y`).
- **Traductor** de MiniLang a **C++** o **JavaScript**, con **Flex + Bison** (`lexico_traductor.l` + `traductor.y`).

Una sola interfaz gráfica en **Python (Tkinter)** con seis pestañas llama a los ejecutables.

Documentación:
- [`docs/Manual_MiniLang.docx`](docs/Manual_MiniLang.docx): el lenguaje completo.
- [`docs/Documentacion_Compilador.docx`](docs/Documentacion_Compilador.docx): arquitectura del compilador, tabla de símbolos, código intermedio y plan de pruebas.

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
├── lexico_traductor.l          # Especificación Flex del traductor
├── traductor.y                 # Gramática Bison con la generación de código C++ / JavaScript
├── traductor.exe               # Ejecutable del traductor
├── lexico_intermedio.l         # Especificación Flex del generador de código intermedio
├── intermedio.y                # Gramática Bison que genera las cuádruplas
├── intermedio.exe              # Ejecutable del generador de código intermedio
├── gui.py                      # Interfaz gráfica (Python / Tkinter, 6 pestañas)
├── docs/
│   ├── Manual_MiniLang.docx           # Documentación completa del lenguaje
│   └── Documentacion_Compilador.docx  # Documentación del compilador y plan de pruebas
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
│   └── traductor/               # Casos de prueba del traductor
│       ├── valida1_aritmetica.txt ... valida8_programa_completo.txt (+ .salida con lo que debe imprimir)
│       ├── invalida1_sombreado.txt ... invalida4_sintaxis.txt
│       └── esperado/            # Traducción a .cpp y .js de cada caso válido
│   └── intermedio/              # Casos de prueba del generador de código intermedio
│       ├── valida1_aritmetica.txt ... valida8_programa_completo.txt, calificaciones.txt,
│       │   fibonacci.txt, fibonacci_pares.txt, anidado.txt, sombreado.txt (+ .salida)
│       ├── invalida_no_declarada.txt, invalida_division_cero.txt, invalida_sintaxis.txt
│       ├── interpretar_tac.py   # Ejecuta las cuádruplas y compara con el .salida
│       └── esperado/            # Código de tres direcciones esperado de cada caso
└── README.md
```

## Cómo ejecutar (Windows)

Requisito: tener **Python 3** instalado (Tkinter viene incluido).

1. Descargar o clonar el repositorio.
2. Dejar `gui.py`, `analizador.exe`, `sintactico.exe`, `semantico.exe`, `traductor.exe` e `intermedio.exe` en la misma carpeta.
3. Abrir una terminal en esa carpeta y ejecutar:

```
python gui.py
```

4. En la ventana, cambiar entre las pestañas **Analisis Lexico**, **Analisis Sintactico**,
   **Analisis Semantico**, **Tabla de Simbolos**, **Traductor** y **Codigo Intermedio**. En cada una: escribir código o usar
   **Cargar archivo**, y presionar **Analizar** (en el traductor, elegir C++ o JavaScript y presionar
   **Traducir**; en código intermedio, presionar **Generar**).

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
7. Compilar el traductor (mismo esquema de nombres propios con `-o`):
   ```
   bison -d -o traductor.tab.c traductor.y
   flex -o lex_traductor.c lexico_traductor.l
   gcc traductor.tab.c lex_traductor.c -o traductor.exe
   ```
8. Compilar el generador de código intermedio (también con nombres propios):
   ```
   bison -d -o intermedio.tab.c intermedio.y
   flex -o lex_intermedio.c lexico_intermedio.l
   gcc intermedio.tab.c lex_intermedio.c -o intermedio.exe
   ```
9. Pruebas rápidas por consola (opcional):
   ```
   .\analizador.exe prueba.txt
   .\sintactico.exe pruebas\sintactico\valida1_declaraciones.txt
   .\semantico.exe pruebas\semantico\demo_errores_mixtos.txt
   .\traductor.exe pruebas\traductor\valida8_programa_completo.txt cpp
   .\traductor.exe pruebas\traductor\valida8_programa_completo.txt js
   .\intermedio.exe pruebas\intermedio\fibonacci.txt
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

## Traductor (MiniLang a C++ / JavaScript)

Traduce un programa MiniLang correcto al lenguaje elegido. Usa traducción dirigida por la sintaxis:
las acciones de Bison construyen el texto del lenguaje destino mientras se reconoce cada regla, y
antes de generar nada se hace el mismo análisis semántico del apartado anterior. Si el programa tiene
errores no se genera código, solo se informan los errores.

### Uso

```
traductor.exe programa.txt cpp            # traduce a C++
traductor.exe programa.txt js             # traduce a JavaScript
traductor.exe programa.txt cpp --crudo    # solo el codigo (listo para redirigir a un archivo)
```

Para comprobar el resultado:

```
traductor.exe pruebas\traductor\valida8_programa_completo.txt cpp --crudo > salida.cpp
g++ salida.cpp -o salida.exe && salida.exe
traductor.exe pruebas\traductor\valida8_programa_completo.txt js --crudo > salida.js
node salida.js
```

### Formato de salida (consola, sin `--crudo`)

```
ADVERTENCIA | ERROR_SEMANTICO | ERROR_SINTACTICO | ERROR_LEXICO | ERROR_TRADUCCION <TAB>linea<TAB>mensaje
TRADUCCION<TAB>correcta|incorrecta<TAB>C++|JavaScript<TAB>total_errores<TAB>total_advertencias
CODIGO<TAB>linea de codigo traducido      (una por cada linea, solo si la traduccion es correcta)
```

### Equivalencias principales

| MiniLang | C++ | JavaScript |
|---|---|---|
| `int x = 5;` | `int x = 5;` | `let x = 5;` |
| `float y = 2.5;` | `double y = 2.5;` | `let y = 2.5;` |
| `int z;` | `int z = 0;` | `let z = 0;` |
| `print(x);` | `std::cout << x << std::endl;` | `console.log(x);` |
| `a / b` (ambos `int`) | `a / b` | `Math.trunc(a / b)` |
| `a < b` usado como valor | `a < b` | `Number(a < b)` |
| `a == b` / `a != b` | `a == b` / `a != b` | `a === b` / `a !== b` |

Además: los nombres que son palabras reservadas del destino (`class`, `new`, `Math`...) reciben el sufijo
`_mini`, y los literales con ceros a la izquierda se normalizan (`007` sale como `7`). El detalle de
cada decisión está en el manual (`docs/Manual_MiniLang.docx`, sección 9).

### Pruebas del traductor

Cada programa válido de `pruebas/traductor/` tiene su salida esperada (`.salida`) y su traducción en
`pruebas/traductor/esperado/`. Las ocho traducciones se compilaron con `g++` y se ejecutaron con `node`,
y todas imprimen lo mismo que el valor calculado a mano.

| Prueba | Qué verifica |
|---|---|
| `valida1_aritmetica.txt` | Operaciones y precedencia |
| `valida2_division_entera.txt` | División entera frente a decimal |
| `valida3_comparaciones.txt` | Comparaciones usadas como valores 0/1 |
| `valida4_control.txt` | `if`/`else` anidados y `while` |
| `valida5_nombres_reservados.txt` | Renombrado de identificadores |
| `valida6_ceros_iniciales.txt` | Normalización de literales |
| `valida7_sin_valor.txt` | Variables declaradas sin valor inicial |
| `valida8_programa_completo.txt` | Programa que combina todo lo anterior |
| `invalida1_sombreado.txt` | `ERROR_TRADUCCION`: variable que oculta a otra |
| `invalida2_numero_grande.txt` | `ERROR_TRADUCCION`: entero que no cabe en 32 bits |
| `invalida3_error_semantico.txt` | Errores semánticos: no se genera código |
| `invalida4_sintaxis.txt` | Error de sintaxis: no se genera código |

### Limitaciones de la traducción

- El sombreado de variables (declarar en un bloque una variable con el nombre de otra del bloque
  exterior) es solo una advertencia en el analizador semántico, pero el traductor lo rechaza, porque
  en JavaScript y en C++ el resultado no sería el mismo que en MiniLang.
- JavaScript imprime `-0` donde C++ imprime `0` (por ejemplo `(0 - 1) / 2`).
- Los decimales pueden verse distinto al imprimirse (`cout` muestra 6 cifras significativas).
- Los `int` de C++ son de 32 bits y se desbordan; en JavaScript no.
- Los comentarios no pasan al código traducido.
- MiniLang no tiene el menos unario: se escribe `0 - x`.

## Generador de código intermedio

Genera **código de tres direcciones** en forma de cuádruplas `(operador, arg1, arg2, resultado)`.
Hace las mismas comprobaciones que el analizador semántico y, si el programa no tiene errores, escribe
las cuádruplas. Las expresiones se descomponen con variables temporales (`t1`, `t2`...) y las
estructuras `if`, `if/else` y `while` se convierten en etiquetas (`L1`, `L2`...) y saltos.

```
intermedio.exe programa.txt
```

Ejemplo (`pruebas/intermedio/fibonacci.txt`):

```
    cantidad = 10              L1:
    anterior = 0                   t1 = contador <= cantidad
    actual = 1                     ifFalse t1 goto L2
    contador = 1                   print anterior
                                   ...
                                   goto L1
                               L2:
```

| Operador | Forma legible | Qué hace |
|---|---|---|
| `=` | `x = a` | Copia |
| `+ - * /` | `t = a + b` | Aritmética (`/` si algún operando es `float`) |
| `div` | `t = a div b` | División entera (`int` entre `int`) |
| `< > <= >= == !=` | `t = a < b` | Comparación, vale 1 o 0 |
| `label` / `goto` | `L1:` / `goto L1` | Etiqueta y salto |
| `ifFalse` | `ifFalse t goto L1` | Salta si `t` vale 0 |
| `print` | `print a` | Muestra un valor |

### Formato de salida (consola)

```
ADVERTENCIA | ERROR_SEMANTICO | ERROR_SINTACTICO | ERROR_LEXICO <TAB>linea<TAB>mensaje
CODIGO_INTERMEDIO<TAB>correcto|incorrecto<TAB>cuadruplas<TAB>temporales<TAB>errores<TAB>advertencias
CUADRUPLA<TAB>numero<TAB>operador<TAB>arg1<TAB>arg2<TAB>resultado     (solo si es correcto)
TAC<TAB>instruccion en forma legible                                    (solo si es correcto)
```

### Pruebas del generador de código intermedio

Los 13 programas válidos de `pruebas/intermedio/` tienen su salida esperada (`.salida`, calculada a mano).
El script `interpretar_tac.py` ejecuta las cuádruplas de cada uno con un intérprete sencillo y comprueba que
el programa haga lo mismo que el original:

```
python pruebas/intermedio/interpretar_tac.py
```

Debe terminar con `fallas: 0`. Los 3 casos inválidos (`invalida_*.txt`) no generan código y muestran el error.
El código de tres direcciones esperado de cada caso está en `pruebas/intermedio/esperado/`.

### Limitaciones

- No hay optimización: cada operación crea un temporal nuevo y las constantes no se calculan de antemano.
- Si dos variables de bloques distintos se llaman igual, la segunda recibe un sufijo (`x_2`).
- El traductor genera C++/JavaScript directamente desde la sintaxis; no parte de las cuádruplas.
