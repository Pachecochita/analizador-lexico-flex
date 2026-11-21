"""
gui.py
Interfaz grafica (Tkinter) para los analizadores de MiniLang.
Pestana 1: Analisis Lexico     -> analizador.exe  (Flex)
Pestana 2: Analisis Sintactico -> sintactico.exe  (Flex + Bison)
Pestana 3: Analisis Semantico  -> semantico.exe   (Flex + Bison)
Pestana 4: Tabla de Simbolos   -> semantico.exe   (la tabla que arma el analizador semantico)
Pestana 5: Traductor           -> traductor.exe   (Flex + Bison)
Pestana 6: Codigo Intermedio   -> intermedio.exe  (Flex + Bison)
"""

import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

CARPETA = os.path.dirname(os.path.abspath(__file__))
EXE_LEXICO = "analizador.exe" if os.name == "nt" else "./analizador"
EXE_SINTACTICO = "sintactico.exe" if os.name == "nt" else "./sintactico"
EXE_SEMANTICO = "semantico.exe" if os.name == "nt" else "./semantico"
EXE_TRADUCTOR = "traductor.exe" if os.name == "nt" else "./traductor"
EXE_INTERMEDIO = "intermedio.exe" if os.name == "nt" else "./intermedio"

CODIGO_EJEMPLO = (
    "int x = 10;\n"
    "float y = 3.14;\n\n"
    "if (x >= y) {\n"
    "    print(x);\n"
    "}"
)

CODIGO_EJEMPLO_SIMBOLOS = (
    "int total = 0;\n"
    "float promedio = 8.5;\n"
    "int i = 1;\n"
    "while (i <= 3) {\n"
    "    int cuadrado = i * i;\n"
    "    total = total + cuadrado;\n"
    "    i = i + 1;\n"
    "}\n"
    "print(total);\n"
)

CODIGO_EJEMPLO_SEMANTICO = (
    "int edad = 20;\n"
    "float promedio = 8.5;\n"
    "int resultado = promedio * 2;\n"
    "if (edad >= 18) {\n"
    "    int mayor = 1;\n"
    "    print(total);\n"
    "}"
)

CODIGO_EJEMPLO_TRADUCTOR = (
    "int n = 5;\n"
    "int suma = 0;\n"
    "int i = 1;\n\n"
    "while (i <= n) {\n"
    "    suma = suma + i;\n"
    "    i = i + 1;\n"
    "}\n"
    "print(suma);\n"
    "print(suma / 2);\n"
)


def ejecutar(nombre_exe, ruta_codigo, *extra):
    ruta_ejecutable = os.path.join(CARPETA, nombre_exe)
    return subprocess.run(
        [ruta_ejecutable, ruta_codigo, *extra],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def guardar_temporal(codigo):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(codigo)
        return tmp.name


def leer_archivo_en(texto_widget, carpeta_inicial=None):
    ruta = filedialog.askopenfilename(
        initialdir=carpeta_inicial,
        filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")],
    )
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            texto_widget.delete("1.0", tk.END)
            texto_widget.insert(tk.END, f.read())


def correr_analizador(nombre_exe, codigo, *extra):
    """Guarda el codigo en un archivo temporal y corre el ejecutable.
    Devuelve el resultado o None si no se pudo ejecutar."""
    ruta_tmp = guardar_temporal(codigo)
    try:
        return ejecutar(nombre_exe, ruta_tmp, *extra)
    except FileNotFoundError:
        messagebox.showerror(
            "Ejecutable no encontrado",
            f"No se encontro '{nombre_exe}' en la carpeta del proyecto.\n"
            "Compila primero (ver README.md).",
        )
        return None
    finally:
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)


# ---------- Pestana Lexico ----------

def analizar_lexico():
    codigo = texto_lexico.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para analizar.")
        return

    resultado = correr_analizador(EXE_LEXICO, codigo)
    if resultado is None:
        return

    for fila in tabla_lexico.get_children():
        tabla_lexico.delete(fila)

    total_tokens = 0
    total_errores = 0
    for linea in resultado.stdout.strip().split("\n"):
        if not linea:
            continue
        partes = linea.split("\t")
        if len(partes) == 2:
            tipo, lexema = partes
            tabla_lexico.insert("", tk.END, values=(tipo, lexema))
            total_tokens += 1
            if tipo == "ERROR_LEXICO":
                total_errores += 1

    estado_lexico.config(text=f"Tokens encontrados: {total_tokens}   |   Errores lexicos: {total_errores}")
    if resultado.stderr:
        messagebox.showerror("Error del analizador", resultado.stderr)


def cargar_archivo_lexico():
    leer_archivo_en(texto_lexico)


def limpiar_lexico():
    texto_lexico.delete("1.0", tk.END)
    for fila in tabla_lexico.get_children():
        tabla_lexico.delete(fila)
    estado_lexico.config(text="")


# ---------- Pestana Sintactico ----------

def analizar_sintactico():
    codigo = texto_sintactico.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para analizar.")
        return

    resultado = correr_analizador(EXE_SINTACTICO, codigo)
    if resultado is None:
        return

    salida_texto.config(state="normal")
    salida_texto.delete("1.0", tk.END)

    correcto = "ANALISIS_SINTACTICO\tcorrecto" in resultado.stdout

    if correcto:
        salida_texto.insert(tk.END, "Analisis sintactico correcto.\n\n", "ok")
        salida_texto.insert(tk.END, "El codigo respeta la gramatica de MiniLang:\n")
        salida_texto.insert(tk.END, "declaraciones, asignaciones, if/else, while, print\n")
        salida_texto.insert(tk.END, "y expresiones aritmeticas/relacionales bien formadas.")
    else:
        salida_texto.insert(tk.END, "Analisis sintactico incorrecto.\n\n", "error")
        for linea in resultado.stderr.strip().split("\n"):
            if linea:
                salida_texto.insert(tk.END, linea + "\n")

    salida_texto.config(state="disabled")
    estado_sintactico.config(
        text="Resultado: CORRECTO" if correcto else "Resultado: INCORRECTO",
        fg="#2e7d32" if correcto else "#c62828",
    )


def cargar_archivo_sintactico():
    leer_archivo_en(texto_sintactico)


def limpiar_sintactico():
    texto_sintactico.delete("1.0", tk.END)
    salida_texto.config(state="normal")
    salida_texto.delete("1.0", tk.END)
    salida_texto.config(state="disabled")
    estado_sintactico.config(text="")


# ---------- Pestana Semantico ----------

ETIQUETAS_MENSAJE = {
    "ERROR_SEMANTICO": ("Error semantico", "error"),
    "ERROR_SINTACTICO": ("Error sintactico", "error"),
    "ERROR_LEXICO": ("Error lexico", "error"),
    "ADVERTENCIA": ("Advertencia", "aviso"),
}


def limpiar_resultados_semantico():
    for fila in tabla_simbolos.get_children():
        tabla_simbolos.delete(fila)
    for fila in tabla_mensajes.get_children():
        tabla_mensajes.delete(fila)


def analizar_semantico():
    codigo = texto_semantico.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para analizar.")
        return

    resultado = correr_analizador(EXE_SEMANTICO, codigo)
    if resultado is None:
        return

    limpiar_resultados_semantico()

    correcto = False
    n_errores = 0
    n_avisos = 0

    for linea in resultado.stdout.strip().split("\n"):
        partes = linea.split("\t")
        if not partes or not partes[0]:
            continue
        clave = partes[0]

        if clave == "SIMBOLO" and len(partes) == 7:
            _, nombre, tipo, nivel, linea_decl, inicializada, usada = partes
            ambito = "global" if nivel == "0" else f"bloque {nivel}"
            tabla_simbolos.insert("", tk.END, values=(nombre, tipo, ambito, linea_decl, inicializada, usada))

        elif clave in ETIQUETAS_MENSAJE and len(partes) == 3:
            etiqueta, tag = ETIQUETAS_MENSAJE[clave]
            tabla_mensajes.insert("", tk.END, values=(etiqueta, partes[1], partes[2]), tags=(tag,))

        elif clave == "ANALISIS_SEMANTICO" and len(partes) == 4:
            correcto = partes[1] == "correcto"
            n_errores = int(partes[2])
            n_avisos = int(partes[3])

    if resultado.stderr.strip():
        messagebox.showerror("Error del analizador", resultado.stderr)

    estado_semantico.config(
        text=("Resultado: CORRECTO" if correcto else "Resultado: INCORRECTO")
        + f"   |   Errores: {n_errores}   |   Advertencias: {n_avisos}",
        fg="#2e7d32" if correcto else "#c62828",
    )


def cargar_archivo_semantico():
    carpeta = os.path.join(CARPETA, "pruebas", "semantico")
    leer_archivo_en(texto_semantico, carpeta if os.path.isdir(carpeta) else None)


def limpiar_semantico():
    texto_semantico.delete("1.0", tk.END)
    limpiar_resultados_semantico()
    estado_semantico.config(text="")


# ---------- Pestana Tabla de Simbolos ----------

def generar_tabla_simbolos():
    codigo = texto_simbolos.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para generar la tabla.")
        return

    resultado = correr_analizador(EXE_SEMANTICO, codigo)
    if resultado is None:
        return

    for fila in tabla_simbolos_t.get_children():
        tabla_simbolos_t.delete(fila)

    n_simbolos = 0
    ambitos = set()
    n_errores = 0
    for linea in resultado.stdout.split("\n"):
        partes = linea.rstrip("\r").split("\t")
        if partes[0] == "SIMBOLO" and len(partes) == 7:
            _, nombre, tipo, nivel, linea_decl, inicializada, usada = partes
            ambito = "global" if nivel == "0" else f"bloque {nivel}"
            ambitos.add(ambito)
            n_simbolos += 1
            tabla_simbolos_t.insert("", tk.END, values=(nombre, tipo, ambito, linea_decl, inicializada, usada))
        elif partes[0] == "ANALISIS_SEMANTICO" and len(partes) == 4:
            n_errores = int(partes[2])

    if resultado.stderr.strip():
        messagebox.showerror("Error del analizador", resultado.stderr)

    texto = f"Simbolos: {n_simbolos}   |   Ambitos distintos: {len(ambitos)}"
    if n_errores:
        texto += f"   |   El programa tiene {n_errores} error(es); ver la pestana Analisis Semantico"
    estado_simbolos.config(text=texto, fg="#c62828" if n_errores else "#2e7d32")


def cargar_archivo_simbolos():
    carpeta = os.path.join(CARPETA, "pruebas", "semantico")
    leer_archivo_en(texto_simbolos, carpeta if os.path.isdir(carpeta) else None)


def limpiar_simbolos():
    texto_simbolos.delete("1.0", tk.END)
    for fila in tabla_simbolos_t.get_children():
        tabla_simbolos_t.delete(fila)
    estado_simbolos.config(text="")


# ---------- Pestana Traductor ----------

ETIQUETAS_TRADUCTOR = dict(ETIQUETAS_MENSAJE, ERROR_TRADUCCION=("Error de traduccion", "error"))
EXTENSION_DESTINO = {"cpp": ".cpp", "js": ".js"}


def escribir_codigo_traducido(texto):
    salida_traduccion.config(state="normal")
    salida_traduccion.delete("1.0", tk.END)
    salida_traduccion.insert(tk.END, texto)
    salida_traduccion.config(state="disabled")


def traducir():
    codigo = texto_traductor.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para traducir.")
        return

    resultado = correr_analizador(EXE_TRADUCTOR, codigo, destino_var.get())
    if resultado is None:
        return

    for fila in tabla_mensajes_t.get_children():
        tabla_mensajes_t.delete(fila)

    correcta = False
    n_errores = 0
    n_avisos = 0
    lineas_codigo = []

    for linea in resultado.stdout.split("\n"):
        partes = linea.rstrip("\r").split("\t", 1) if linea.startswith("CODIGO\t") else linea.split("\t")
        if not partes or not partes[0]:
            continue
        clave = partes[0]

        if clave == "CODIGO" and len(partes) == 2:
            lineas_codigo.append(partes[1])
        elif clave in ETIQUETAS_TRADUCTOR and len(partes) == 3:
            etiqueta, tag = ETIQUETAS_TRADUCTOR[clave]
            tabla_mensajes_t.insert("", tk.END, values=(etiqueta, partes[1], partes[2]), tags=(tag,))
        elif clave == "TRADUCCION" and len(partes) == 5:
            correcta = partes[1] == "correcta"
            n_errores = int(partes[3])
            n_avisos = int(partes[4])

    escribir_codigo_traducido("\n".join(lineas_codigo) + "\n" if correcta else "")

    if resultado.stderr.strip():
        messagebox.showerror("Error del traductor", resultado.stderr)

    estado_traductor.config(
        text=("Traduccion: CORRECTA" if correcta else "Traduccion: NO SE PUDO TRADUCIR")
        + f"   |   Errores: {n_errores}   |   Advertencias: {n_avisos}",
        fg="#2e7d32" if correcta else "#c62828",
    )


def copiar_traduccion():
    codigo = salida_traduccion.get("1.0", tk.END).strip()
    if not codigo:
        messagebox.showwarning("Aviso", "Todavia no hay codigo traducido para copiar.")
        return
    ventana.clipboard_clear()
    ventana.clipboard_append(codigo + "\n")


def guardar_traduccion():
    codigo = salida_traduccion.get("1.0", tk.END).strip()
    if not codigo:
        messagebox.showwarning("Aviso", "Todavia no hay codigo traducido para guardar.")
        return
    ext = EXTENSION_DESTINO[destino_var.get()]
    ruta = filedialog.asksaveasfilename(
        defaultextension=ext,
        filetypes=[("Codigo traducido", "*" + ext), ("Todos", "*.*")],
    )
    if ruta:
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            f.write(codigo + "\n")


def cargar_archivo_traductor():
    carpeta = os.path.join(CARPETA, "pruebas", "traductor")
    leer_archivo_en(texto_traductor, carpeta if os.path.isdir(carpeta) else None)


def limpiar_traductor():
    texto_traductor.delete("1.0", tk.END)
    escribir_codigo_traducido("")
    for fila in tabla_mensajes_t.get_children():
        tabla_mensajes_t.delete(fila)
    estado_traductor.config(text="")


# ---------- Pestana Codigo Intermedio ----------

CODIGO_EJEMPLO_INTERMEDIO = (
    "int a = 4;\n"
    "int b = 3;\n"
    "int resultado = a * b + 2;\n"
    "if (resultado > 10) {\n"
    "    print(resultado);\n"
    "} else {\n"
    "    print(0);\n"
    "}\n"
)


def escribir_tac(texto):
    salida_tac.config(state="normal")
    salida_tac.delete("1.0", tk.END)
    salida_tac.insert(tk.END, texto)
    salida_tac.config(state="disabled")


def limpiar_resultados_intermedio():
    for fila in tabla_cuadruplas.get_children():
        tabla_cuadruplas.delete(fila)
    for fila in tabla_mensajes_i.get_children():
        tabla_mensajes_i.delete(fila)
    escribir_tac("")


def generar_intermedio():
    codigo = texto_intermedio.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para generar.")
        return

    resultado = correr_analizador(EXE_INTERMEDIO, codigo)
    if resultado is None:
        return

    limpiar_resultados_intermedio()

    correcto = False
    n_cuads = n_temps = n_errores = n_avisos = 0
    lineas_tac = []

    for linea in resultado.stdout.split("\n"):
        linea = linea.rstrip("\r")
        if linea.startswith("TAC\t"):
            lineas_tac.append(linea[4:])
            continue
        partes = linea.split("\t")
        if not partes or not partes[0]:
            continue
        clave = partes[0]

        if clave == "CUADRUPLA" and len(partes) == 6:
            tabla_cuadruplas.insert("", tk.END, values=tuple(partes[1:]))
        elif clave in ETIQUETAS_MENSAJE and len(partes) == 3:
            etiqueta, tag = ETIQUETAS_MENSAJE[clave]
            tabla_mensajes_i.insert("", tk.END, values=(etiqueta, partes[1], partes[2]), tags=(tag,))
        elif clave == "CODIGO_INTERMEDIO" and len(partes) == 6:
            correcto = partes[1] == "correcto"
            n_cuads, n_temps = int(partes[2]), int(partes[3])
            n_errores, n_avisos = int(partes[4]), int(partes[5])

    escribir_tac("\n".join(lineas_tac) + "\n" if lineas_tac else "")

    if resultado.stderr.strip():
        messagebox.showerror("Error del generador", resultado.stderr)

    estado_intermedio.config(
        text=("Codigo intermedio: CORRECTO" if correcto else "Codigo intermedio: NO SE PUDO GENERAR")
        + f"   |   Cuadruplas: {n_cuads}   |   Temporales: {n_temps}"
        + f"   |   Errores: {n_errores}   |   Advertencias: {n_avisos}",
        fg="#2e7d32" if correcto else "#c62828",
    )


def cargar_archivo_intermedio():
    carpeta = os.path.join(CARPETA, "pruebas", "intermedio")
    leer_archivo_en(texto_intermedio, carpeta if os.path.isdir(carpeta) else None)


def limpiar_intermedio():
    texto_intermedio.delete("1.0", tk.END)
    limpiar_resultados_intermedio()
    estado_intermedio.config(text="")


# ---------- Interfaz ----------

ventana = tk.Tk()
ventana.title("Compilador MiniLang - Flex y Bison")
ventana.geometry("1000x780")
ventana.minsize(800, 600)

notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

# --- Pestana 1: Lexico ---
pestana_lexico = tk.Frame(notebook)
notebook.add(pestana_lexico, text="Analisis Lexico")

frame_botones_l = tk.Frame(pestana_lexico)
frame_botones_l.pack(fill=tk.X, padx=10, pady=8)
tk.Button(frame_botones_l, text="Cargar archivo", command=cargar_archivo_lexico).pack(side=tk.LEFT)
tk.Button(frame_botones_l, text="Analizar", command=analizar_lexico, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), padx=12).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones_l, text="Limpiar", command=limpiar_lexico).pack(side=tk.LEFT)

tk.Label(pestana_lexico, text="Codigo fuente:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
texto_lexico = tk.Text(pestana_lexico, height=10, font=("Consolas", 11), wrap="none")
texto_lexico.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_lexico.insert(tk.END, CODIGO_EJEMPLO)

tk.Label(pestana_lexico, text="Tokens encontrados:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
frame_tabla = tk.Frame(pestana_lexico)
frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

tabla_lexico = ttk.Treeview(frame_tabla, columns=("tipo", "lexema"), show="headings")
tabla_lexico.heading("tipo", text="Tipo de Token")
tabla_lexico.heading("lexema", text="Lexema")
tabla_lexico.column("tipo", width=250)
tabla_lexico.column("lexema", width=300)
scrollbar_l = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_lexico.yview)
tabla_lexico.configure(yscrollcommand=scrollbar_l.set)
tabla_lexico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_l.pack(side=tk.RIGHT, fill=tk.Y)

estado_lexico = tk.Label(pestana_lexico, text="", font=("Arial", 9), fg="#555")
estado_lexico.pack(anchor="w", padx=10, pady=(0, 8))

# --- Pestana 2: Sintactico ---
pestana_sintactico = tk.Frame(notebook)
notebook.add(pestana_sintactico, text="Analisis Sintactico")

frame_botones_s = tk.Frame(pestana_sintactico)
frame_botones_s.pack(fill=tk.X, padx=10, pady=8)
tk.Button(frame_botones_s, text="Cargar archivo", command=cargar_archivo_sintactico).pack(side=tk.LEFT)
tk.Button(frame_botones_s, text="Analizar", command=analizar_sintactico, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), padx=12).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones_s, text="Limpiar", command=limpiar_sintactico).pack(side=tk.LEFT)

tk.Label(pestana_sintactico, text="Codigo fuente:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
texto_sintactico = tk.Text(pestana_sintactico, height=12, font=("Consolas", 11), wrap="none")
texto_sintactico.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_sintactico.insert(tk.END, CODIGO_EJEMPLO)

tk.Label(pestana_sintactico, text="Resultado:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
salida_texto = tk.Text(pestana_sintactico, height=10, font=("Consolas", 11), state="disabled", bg="#f5f5f5")
salida_texto.tag_config("ok", foreground="#2e7d32", font=("Consolas", 11, "bold"))
salida_texto.tag_config("error", foreground="#c62828", font=("Consolas", 11, "bold"))
salida_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

estado_sintactico = tk.Label(pestana_sintactico, text="", font=("Arial", 10, "bold"))
estado_sintactico.pack(anchor="w", padx=10, pady=(0, 8))

# --- Pestana 3: Semantico ---
pestana_semantico = tk.Frame(notebook)
notebook.add(pestana_semantico, text="Analisis Semantico")

frame_botones_m = tk.Frame(pestana_semantico)
frame_botones_m.pack(fill=tk.X, padx=10, pady=8)
tk.Button(frame_botones_m, text="Cargar archivo", command=cargar_archivo_semantico).pack(side=tk.LEFT)
tk.Button(frame_botones_m, text="Analizar", command=analizar_semantico, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), padx=12).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones_m, text="Limpiar", command=limpiar_semantico).pack(side=tk.LEFT)

tk.Label(pestana_semantico, text="Codigo fuente:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
texto_semantico = tk.Text(pestana_semantico, height=9, font=("Consolas", 11), wrap="none")
texto_semantico.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_semantico.insert(tk.END, CODIGO_EJEMPLO_SEMANTICO)

tk.Label(pestana_semantico, text="Tabla de simbolos:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
frame_simbolos = tk.Frame(pestana_semantico)
frame_simbolos.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))

tabla_simbolos = ttk.Treeview(
    frame_simbolos, height=6, show="headings",
    columns=("nombre", "tipo", "ambito", "linea", "inicializada", "usada"),
)
for col, titulo, ancho in (
    ("nombre", "Nombre", 200), ("tipo", "Tipo", 90), ("ambito", "Ambito", 110),
    ("linea", "Linea decl.", 90), ("inicializada", "Con valor inicial", 130), ("usada", "Usada", 80),
):
    tabla_simbolos.heading(col, text=titulo)
    tabla_simbolos.column(col, width=ancho, anchor="w")
scroll_sim = ttk.Scrollbar(frame_simbolos, orient="vertical", command=tabla_simbolos.yview)
tabla_simbolos.configure(yscrollcommand=scroll_sim.set)
tabla_simbolos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_sim.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(pestana_semantico, text="Errores y advertencias:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
frame_mensajes = tk.Frame(pestana_semantico)
frame_mensajes.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

tabla_mensajes = ttk.Treeview(
    frame_mensajes, height=6, show="headings", columns=("tipo", "linea", "mensaje"),
)
tabla_mensajes.heading("tipo", text="Tipo")
tabla_mensajes.heading("linea", text="Linea")
tabla_mensajes.heading("mensaje", text="Mensaje")
tabla_mensajes.column("tipo", width=130, anchor="w")
tabla_mensajes.column("linea", width=60, anchor="w")
tabla_mensajes.column("mensaje", width=700, anchor="w")
tabla_mensajes.tag_configure("error", foreground="#c62828")
tabla_mensajes.tag_configure("aviso", foreground="#b26a00")
scroll_msg = ttk.Scrollbar(frame_mensajes, orient="vertical", command=tabla_mensajes.yview)
tabla_mensajes.configure(yscrollcommand=scroll_msg.set)
tabla_mensajes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_msg.pack(side=tk.RIGHT, fill=tk.Y)

estado_semantico = tk.Label(pestana_semantico, text="", font=("Arial", 10, "bold"))
estado_semantico.pack(anchor="w", padx=10, pady=(0, 8))

# --- Pestana 4: Tabla de Simbolos ---
pestana_simbolos = tk.Frame(notebook)
notebook.add(pestana_simbolos, text="Tabla de Simbolos")

frame_botones_ts = tk.Frame(pestana_simbolos)
frame_botones_ts.pack(fill=tk.X, padx=10, pady=8)
tk.Button(frame_botones_ts, text="Cargar archivo", command=cargar_archivo_simbolos).pack(side=tk.LEFT)
tk.Button(frame_botones_ts, text="Generar tabla", command=generar_tabla_simbolos, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), padx=12).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones_ts, text="Limpiar", command=limpiar_simbolos).pack(side=tk.LEFT)

tk.Label(pestana_simbolos, text="Codigo MiniLang:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
texto_simbolos = tk.Text(pestana_simbolos, height=10, font=("Consolas", 11), wrap="none")
texto_simbolos.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_simbolos.insert(tk.END, CODIGO_EJEMPLO_SIMBOLOS)

tk.Label(pestana_simbolos, text="Tabla de simbolos:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
frame_tabla_ts = tk.Frame(pestana_simbolos)
frame_tabla_ts.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))
tabla_simbolos_t = ttk.Treeview(
    frame_tabla_ts, show="headings",
    columns=("nombre", "tipo", "ambito", "linea", "inicializada", "usada"),
)
for col, titulo, ancho in (
    ("nombre", "Nombre", 220), ("tipo", "Tipo", 100), ("ambito", "Ambito", 130),
    ("linea", "Linea decl.", 100), ("inicializada", "Con valor inicial", 150), ("usada", "Usada", 100),
):
    tabla_simbolos_t.heading(col, text=titulo)
    tabla_simbolos_t.column(col, width=ancho, anchor="w")
scroll_ts = ttk.Scrollbar(frame_tabla_ts, orient="vertical", command=tabla_simbolos_t.yview)
tabla_simbolos_t.configure(yscrollcommand=scroll_ts.set)
tabla_simbolos_t.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_ts.pack(side=tk.RIGHT, fill=tk.Y)

estado_simbolos = tk.Label(pestana_simbolos, text="", font=("Arial", 10, "bold"))
estado_simbolos.pack(anchor="w", padx=10, pady=(0, 8))

# --- Pestana 5: Traductor ---
pestana_traductor = tk.Frame(notebook)
notebook.add(pestana_traductor, text="Traductor")

frame_botones_t = tk.Frame(pestana_traductor)
frame_botones_t.pack(fill=tk.X, padx=10, pady=8)
tk.Button(frame_botones_t, text="Cargar archivo", command=cargar_archivo_traductor).pack(side=tk.LEFT)
tk.Label(frame_botones_t, text="   Traducir a:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
destino_var = tk.StringVar(value="cpp")
tk.Radiobutton(frame_botones_t, text="C++", variable=destino_var, value="cpp").pack(side=tk.LEFT)
tk.Radiobutton(frame_botones_t, text="JavaScript", variable=destino_var, value="js").pack(side=tk.LEFT)
tk.Button(frame_botones_t, text="Traducir", command=traducir, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), padx=12).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones_t, text="Limpiar", command=limpiar_traductor).pack(side=tk.LEFT)

tk.Label(pestana_traductor, text="Codigo MiniLang:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
texto_traductor = tk.Text(pestana_traductor, height=9, font=("Consolas", 11), wrap="none")
texto_traductor.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_traductor.insert(tk.END, CODIGO_EJEMPLO_TRADUCTOR)

frame_titulo_salida = tk.Frame(pestana_traductor)
frame_titulo_salida.pack(fill=tk.X, padx=10)
tk.Label(frame_titulo_salida, text="Codigo traducido:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
tk.Button(frame_titulo_salida, text="Guardar como...", command=guardar_traduccion).pack(side=tk.RIGHT)
tk.Button(frame_titulo_salida, text="Copiar", command=copiar_traduccion).pack(side=tk.RIGHT, padx=6)

frame_salida_t = tk.Frame(pestana_traductor)
frame_salida_t.pack(fill=tk.BOTH, expand=True, padx=10, pady=(2, 8))
salida_traduccion = tk.Text(frame_salida_t, height=11, font=("Consolas", 11), wrap="none",
                            state="disabled", bg="#f5f5f5")
scroll_trad = ttk.Scrollbar(frame_salida_t, orient="vertical", command=salida_traduccion.yview)
salida_traduccion.configure(yscrollcommand=scroll_trad.set)
salida_traduccion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_trad.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(pestana_traductor, text="Errores y advertencias:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
frame_mensajes_t = tk.Frame(pestana_traductor)
frame_mensajes_t.pack(fill=tk.X, padx=10, pady=(0, 5))
tabla_mensajes_t = ttk.Treeview(
    frame_mensajes_t, height=4, show="headings", columns=("tipo", "linea", "mensaje"),
)
tabla_mensajes_t.heading("tipo", text="Tipo")
tabla_mensajes_t.heading("linea", text="Linea")
tabla_mensajes_t.heading("mensaje", text="Mensaje")
tabla_mensajes_t.column("tipo", width=150, anchor="w")
tabla_mensajes_t.column("linea", width=60, anchor="w")
tabla_mensajes_t.column("mensaje", width=680, anchor="w")
tabla_mensajes_t.tag_configure("error", foreground="#c62828")
tabla_mensajes_t.tag_configure("aviso", foreground="#b26a00")
scroll_msg_t = ttk.Scrollbar(frame_mensajes_t, orient="vertical", command=tabla_mensajes_t.yview)
tabla_mensajes_t.configure(yscrollcommand=scroll_msg_t.set)
tabla_mensajes_t.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_msg_t.pack(side=tk.RIGHT, fill=tk.Y)

estado_traductor = tk.Label(pestana_traductor, text="", font=("Arial", 10, "bold"))
estado_traductor.pack(anchor="w", padx=10, pady=(0, 8))

# --- Pestana 6: Codigo Intermedio ---
pestana_intermedio = tk.Frame(notebook)
notebook.add(pestana_intermedio, text="Codigo Intermedio")

frame_botones_i = tk.Frame(pestana_intermedio)
frame_botones_i.pack(fill=tk.X, padx=10, pady=8)
tk.Button(frame_botones_i, text="Cargar archivo", command=cargar_archivo_intermedio).pack(side=tk.LEFT)
tk.Button(frame_botones_i, text="Generar", command=generar_intermedio, bg="#4CAF50", fg="white",
          font=("Arial", 10, "bold"), padx=12).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones_i, text="Limpiar", command=limpiar_intermedio).pack(side=tk.LEFT)

tk.Label(pestana_intermedio, text="Codigo MiniLang:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
texto_intermedio = tk.Text(pestana_intermedio, height=8, font=("Consolas", 11), wrap="none")
texto_intermedio.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_intermedio.insert(tk.END, CODIGO_EJEMPLO_INTERMEDIO)

frame_titulos_i = tk.Frame(pestana_intermedio)
frame_titulos_i.pack(fill=tk.X, padx=10)
tk.Label(frame_titulos_i, text="Cuadruplas (operador, arg 1, arg 2, resultado):",
         font=("Arial", 10, "bold")).pack(side=tk.LEFT)

frame_centro_i = tk.Frame(pestana_intermedio)
frame_centro_i.pack(fill=tk.BOTH, expand=True, padx=10, pady=(2, 8))

frame_cuads = tk.Frame(frame_centro_i)
frame_cuads.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tabla_cuadruplas = ttk.Treeview(
    frame_cuads, height=8, show="headings", columns=("n", "op", "arg1", "arg2", "res"),
)
for col, titulo, ancho in (
    ("n", "#", 40), ("op", "Operador", 80), ("arg1", "Arg 1", 90), ("arg2", "Arg 2", 90), ("res", "Resultado", 100),
):
    tabla_cuadruplas.heading(col, text=titulo)
    tabla_cuadruplas.column(col, width=ancho, anchor="w")
scroll_cuads = ttk.Scrollbar(frame_cuads, orient="vertical", command=tabla_cuadruplas.yview)
tabla_cuadruplas.configure(yscrollcommand=scroll_cuads.set)
tabla_cuadruplas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_cuads.pack(side=tk.RIGHT, fill=tk.Y)

frame_tac = tk.Frame(frame_centro_i)
frame_tac.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
salida_tac = tk.Text(frame_tac, height=8, width=34, font=("Consolas", 11), wrap="none",
                     state="disabled", bg="#f5f5f5")
scroll_tac = ttk.Scrollbar(frame_tac, orient="vertical", command=salida_tac.yview)
salida_tac.configure(yscrollcommand=scroll_tac.set)
salida_tac.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_tac.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(pestana_intermedio, text="Errores y advertencias:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
frame_mensajes_i = tk.Frame(pestana_intermedio)
frame_mensajes_i.pack(fill=tk.X, padx=10, pady=(0, 5))
tabla_mensajes_i = ttk.Treeview(
    frame_mensajes_i, height=3, show="headings", columns=("tipo", "linea", "mensaje"),
)
tabla_mensajes_i.heading("tipo", text="Tipo")
tabla_mensajes_i.heading("linea", text="Linea")
tabla_mensajes_i.heading("mensaje", text="Mensaje")
tabla_mensajes_i.column("tipo", width=130, anchor="w")
tabla_mensajes_i.column("linea", width=60, anchor="w")
tabla_mensajes_i.column("mensaje", width=700, anchor="w")
tabla_mensajes_i.tag_configure("error", foreground="#c62828")
tabla_mensajes_i.tag_configure("aviso", foreground="#b26a00")
scroll_msg_i = ttk.Scrollbar(frame_mensajes_i, orient="vertical", command=tabla_mensajes_i.yview)
tabla_mensajes_i.configure(yscrollcommand=scroll_msg_i.set)
tabla_mensajes_i.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_msg_i.pack(side=tk.RIGHT, fill=tk.Y)

estado_intermedio = tk.Label(pestana_intermedio, text="", font=("Arial", 10, "bold"))
estado_intermedio.pack(anchor="w", padx=10, pady=(0, 8))

if __name__ == "__main__":
    ventana.mainloop()
