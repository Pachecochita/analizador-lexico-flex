"""
gui.py
Interfaz grafica (Tkinter) para los analizadores de MiniLang.
Pestana 1: Analisis Lexico     -> llama a analizador.exe (Flex)
Pestana 2: Analisis Sintactico -> llama a sintactico.exe (Flex + Bison)
"""

import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

CARPETA = os.path.dirname(os.path.abspath(__file__))
EXE_LEXICO = "analizador.exe" if os.name == "nt" else "./analizador"
EXE_SINTACTICO = "sintactico.exe" if os.name == "nt" else "./sintactico"

CODIGO_EJEMPLO = (
    "int x = 10;\n"
    "float y = 3.14;\n\n"
    "if (x >= y) {\n"
    "    print(x);\n"
    "}"
)


def ejecutar(nombre_exe, ruta_codigo):
    ruta_ejecutable = os.path.join(CARPETA, nombre_exe)
    return subprocess.run([ruta_ejecutable, ruta_codigo], capture_output=True, text=True)


def guardar_temporal(codigo):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(codigo)
        return tmp.name


# ---------- Pestana Lexico ----------

def analizar_lexico():
    codigo = texto_lexico.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para analizar.")
        return

    ruta_tmp = guardar_temporal(codigo)
    try:
        resultado = ejecutar(EXE_LEXICO, ruta_tmp)
    except FileNotFoundError:
        messagebox.showerror("Ejecutable no encontrado", f"No se encontro '{EXE_LEXICO}'.\nCompila primero (ver README.md).")
        os.remove(ruta_tmp)
        return
    finally:
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)

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
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            texto_lexico.delete("1.0", tk.END)
            texto_lexico.insert(tk.END, f.read())


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

    ruta_tmp = guardar_temporal(codigo)
    try:
        resultado = ejecutar(EXE_SINTACTICO, ruta_tmp)
    except FileNotFoundError:
        messagebox.showerror("Ejecutable no encontrado", f"No se encontro '{EXE_SINTACTICO}'.\nCompila primero (ver README.md).")
        os.remove(ruta_tmp)
        return
    finally:
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)

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
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            texto_sintactico.delete("1.0", tk.END)
            texto_sintactico.insert(tk.END, f.read())


def limpiar_sintactico():
    texto_sintactico.delete("1.0", tk.END)
    salida_texto.config(state="normal")
    salida_texto.delete("1.0", tk.END)
    salida_texto.config(state="disabled")
    estado_sintactico.config(text="")


# ---------- Interfaz ----------

ventana = tk.Tk()
ventana.title("Analizadores MiniLang - Flex y Bison")
ventana.geometry("950x680")
ventana.minsize(750, 550)

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

ventana.mainloop()
