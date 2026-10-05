# Analizadores Léxico y Sintáctico - MiniLang

Dos analizadores para el lenguaje de prueba **MiniLang**:

- **Léxico**, construido con **Flex** (`analizador.l`).
- **Sintáctico**, construido con **Flex + Bison** (`lexico_sintactico.l` + `sintactico.y`).

Una sola interfaz gráfica en **Python (Tkinter)** con dos pestañas llama a los dos ejecutables.

Proyecto de la asignatura de Compiladores, UTESA.

## Contenido del repositorio

```
analizador-lexico-flex/
├── analizador.l               # Especificación Flex del analizador lexico (imprime cada token)
├── analizador.exe             # Ejecutable del analizador lexico
├── lexico_sintactico.l        # Especificación Flex que alimenta tokens a Bison (sin imprimir)
├── sintactico.y                # Gramática Bison del analizador sintactico
├── sintactico.exe              # Ejecutable del analizador sintactico
├── gui.py                      # Interfaz gráfica (Python / Tkinter, 2 pestañas)
├── prueba.txt                  # Archivo de prueba rápida (lexico)
├── pruebas/                    # Casos de prueba y resultados esperados
│   ├── prueba1_declaraciones.txt ... prueba5_programa_completo.txt
│   ├── esperado/                # Salida esperada del analizador lexico
│   └── sintactico/              # Casos de prueba del analizador sintactico
│       ├── valida1_declaraciones.txt, valida2_control.txt, valida3_expresiones.txt
│       ├── invalida1_falta_puntocoma.txt, invalida2_llave_sin_cerrar.txt,
│       │   invalida3_parentesis_mal_puesto.txt, invalida4_asignacion_vacia.txt
│       └── esperado/            # Salida esperada de cada caso
└── README.md
```

## Cómo ejecutar (Windows)

Requisito: tener **Python 3** instalado (Tkinter viene incluido).

1. Descargar o clonar el repositorio.
2. Dejar `gui.py`, `analizador.exe` y `sintactico.exe` en la misma carpeta.
3. Abrir una terminal en esa carpeta y ejecutar:

```
python gui.py
```

4. En la ventana, cambiar entre las pestañas **Analisis Lexico** y **Analisis Sintactico**.
   En cada una: escribir código o usar **Cargar archivo**, y presionar **Analizar**.

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
6. Pruebas rápidas por consola (opcional):
   ```
   .\analizador.exe prueba.txt
   .\sintactico.exe pruebas\sintactico\valida1_declaraciones.txt
   ```

## Lenguaje de prueba: "MiniLang"

Lenguaje simplificado de tipo C, pensado solo para ejercitar el reconocimiento de tokens
(no hay análisis sintáctico ni semántico).

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
