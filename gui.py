"""
gui.py
Interfaz grafica (Tkinter) para los analizadores de MiniLang.
Pestana 1: Analisis Lexico     -> analizador.exe  (Flex)
Pestana 2: Analisis Sintactico -> sintactico.exe  (Flex + Bison)
Pestana 3: Analisis Semantico  -> semantico.exe   (Flex + Bison)
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

CODIGO_EJEMPLO = (
    "int x = 10;\n"
    "float y = 3.14;\n\n"
    "if (x >= y) {\n"
    "    print(x);\n"
    "}"
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


def ejecutar(nombre_exe, ruta_codigo):
    ruta_ejecutable = os.path.join(CARPETA, nombre_exe)
    return subprocess.run(
        [ruta_ejecutable, ruta_codigo],
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


def correr_analizador(nombre_exe, codigo):
    """Guarda el codigo en un archivo temporal y corre el ejecutable.
    Devuelve el resultado o None si no se pudo ejecutar."""
    ruta_tmp = guardar_temporal(codigo)
    try:
        return ejecutar(nombre_exe, ruta_tmp)
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


# ---------- Interfaz ----------

ventana = tk.Tk()
ventana.title("Analizadores MiniLang - Flex y Bison")
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

if __name__ == "__main__":
    ventana.mainloop()
