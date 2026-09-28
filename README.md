# Analizador Léxico - MiniLang

Analizador léxico construido con **Flex**, con una interfaz gráfica en **Python (Tkinter)**
que permite escribir o cargar código, analizarlo y ver la lista de tokens encontrados.

## 1. Lenguaje de prueba: "MiniLang"

Se documenta aquí el lenguaje utilizado para probar el analizador (punto 2 del ejercicio).
Es un lenguaje simplificado de tipo C, pensado solo para ejercitar el reconocimiento de tokens
(no tiene análisis sintáctico ni semántico).

### Palabras reservadas
`int`, `float`, `if`, `else`, `while`, `print`

### Identificadores
Empiezan con una letra o guion bajo, seguido de letras, dígitos o guiones bajos.
Expresión regular: `[a-zA-Z_][a-zA-Z0-9_]*`
Ejemplos válidos: `x`, `contador`, `_temp`, `valor2`

### Números
- Enteros: `[0-9]+` → ej. `10`, `2024`
- Decimales: `[0-9]+\.[0-9]+` → ej. `3.14`, `0.5`

### Operadores
| Categoría        | Símbolos                     |
|-------------------|-------------------------------|
| Relacionales      | `==` `!=` `<` `>` `<=` `>=`  |
| Asignación         | `=`                           |
| Aritméticos        | `+` `-` `*` `/`              |

### Símbolos de puntuación
`(` `)` `{` `}` `;` `,`

### Comentarios (se ignoran, no generan token)
- De línea: `// comentario`
- De bloque: `/* comentario */`

### Espacios en blanco
Espacios, tabulaciones y saltos de línea se ignoran.

### Errores léxicos
Cualquier carácter que no calce con ninguna regla anterior se reporta como `ERROR_LEXICO`
(por ejemplo `@`, `$`, `#`).

### Ejemplo de código de entrada
```
int x = 10;
float y = 3.14;

if (x >= y) {
    print(x);
} else {
    print(y);
}
```

### Salida esperada (tipo de token + lexema)
```
PALABRA_RESERVADA   int
IDENTIFICADOR       x
OP_ASIGNACION       =
NUMERO_ENTERO       10
PUNTO_COMA          ;
...
```

## 2. Estructura del proyecto

```
analizador-lexico/
├── analizador.l      # Reglas léxicas (Flex)
├── gui.py             # Interfaz gráfica (Python/Tkinter)
├── README.md
└── .gitignore
```

## 3. Instalación en Windows (MSYS2)

1. Descargar e instalar MSYS2 desde https://www.msys2.org
2. Abrir la terminal **"MSYS2 UCRT64"** y ejecutar:
   ```
   pacman -Syu
   pacman -S mingw-w64-ucrt-x86_64-toolchain flex
   ```
3. Agregar `C:\msys64\ucrt64\bin` a la variable de entorno PATH de Windows,
   para poder usar `gcc` y `flex` desde la terminal normal (CMD/PowerShell) o desde VS Code.
4. Verificar en una terminal nueva:
   ```
   flex --version
   gcc --version
   ```
5. Instalar Python desde https://python.org (marcar "Add Python to PATH" durante la instalación).
   Tkinter viene incluido automáticamente.

## 4. Compilar el analizador

Desde la carpeta del proyecto, en la terminal (CMD, PowerShell o la terminal integrada de VS Code):

```
flex analizador.l
gcc lex.yy.c -o analizador.exe -lfl
```

Esto genera `analizador.exe`. Puedes probarlo directamente en consola así:

```
analizador.exe prueba.txt
```

## 5. Ejecutar la interfaz gráfica

Con `analizador.exe` ya compilado en la misma carpeta:

```
python gui.py
```

Se abre la ventana donde puedes escribir o cargar código, presionar **"Analizar"**
y ver la tabla de tokens.

## 6. Subir el proyecto a GitHub

```
git init
git add analizador.l gui.py README.md .gitignore
git commit -m "Analizador lexico MiniLang con Flex y GUI en Python"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
git push -u origin main
```

Sube también el ejecutable (`analizador.exe`) como parte de la entrega si el profesor
lo pide adjunto por separado, además del código fuente en GitHub.
