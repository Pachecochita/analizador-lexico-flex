"""
gui.py
Interfaz grafica (Tkinter) para el Analizador Lexico de MiniLang.
Llama al ejecutable generado por Flex y muestra los tokens en una tabla.
"""

import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# En Windows el ejecutable se llama analizador.exe, en Linux/Mac "analizador"
NOMBRE_EJECUTABLE = "analizador.exe" if os.name == "nt" else "./analizador"


def ejecutar_analizador(ruta_codigo):
    """Corre el ejecutable del analizador sobre un archivo y devuelve su salida."""
    ruta_ejecutable = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_EJECUTABLE)
    resultado = subprocess.run(
        [ruta_ejecutable, ruta_codigo],
        capture_output=True,
        text=True,
    )
    return resultado


def analizar():
    codigo = texto_entrada.get("1.0", tk.END)
    if not codigo.strip():
        messagebox.showwarning("Aviso", "Escribe o carga codigo para analizar.")
        return

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(codigo)
        ruta_tmp = tmp.name

    try:
        resultado = ejecutar_analizador(ruta_tmp)
    except FileNotFoundError:
        messagebox.showerror(
            "Ejecutable no encontrado",
            f"No se encontro '{NOMBRE_EJECUTABLE}' en la carpeta del proyecto.\n"
            "Compila primero el analizador (ver README.md).",
        )
        os.remove(ruta_tmp)
        return
    finally:
        if os.path.exists(ruta_tmp):
            os.remove(ruta_tmp)

    for fila in tabla.get_children():
        tabla.delete(fila)

    total_tokens = 0
    total_errores = 0

    for linea in resultado.stdout.strip().split("\n"):
        if not linea:
            continue
        partes = linea.split("\t")
        if len(partes) == 2:
            tipo, lexema = partes
            tabla.insert("", tk.END, values=(tipo, lexema))
            total_tokens += 1
            if tipo == "ERROR_LEXICO":
                total_errores += 1

    etiqueta_estado.config(
        text=f"Tokens encontrados: {total_tokens}   |   Errores lexicos: {total_errores}"
    )

    if resultado.stderr:
        messagebox.showerror("Error del analizador", resultado.stderr)


def cargar_archivo():
    ruta = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            texto_entrada.delete("1.0", tk.END)
            texto_entrada.insert(tk.END, f.read())


def limpiar():
    texto_entrada.delete("1.0", tk.END)
    for fila in tabla.get_children():
        tabla.delete(fila)
    etiqueta_estado.config(text="")


# ---------- Interfaz ----------

ventana = tk.Tk()
ventana.title("Analizador Lexico - MiniLang (Flex)")
ventana.geometry("950x650")
ventana.minsize(700, 500)

frame_botones = tk.Frame(ventana)
frame_botones.pack(fill=tk.X, padx=10, pady=8)

tk.Button(frame_botones, text="Cargar archivo", command=cargar_archivo).pack(side=tk.LEFT)
tk.Button(
    frame_botones, text="Analizar", command=analizar, bg="#4CAF50", fg="white",
    font=("Arial", 10, "bold"), padx=12,
).pack(side=tk.LEFT, padx=8)
tk.Button(frame_botones, text="Limpiar", command=limpiar).pack(side=tk.LEFT)

tk.Label(ventana, text="Codigo fuente:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)

texto_entrada = tk.Text(ventana, height=12, font=("Consolas", 11), wrap="none")
texto_entrada.pack(fill=tk.X, padx=10, pady=(0, 8))
texto_entrada.insert(
    tk.END,
    "int x = 10;\n"
    "float y = 3.14;\n\n"
    "if (x >= y) {\n"
    "    print(x);\n"
    "}",
)

tk.Label(ventana, text="Tokens encontrados:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)

frame_tabla = tk.Frame(ventana)
frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

tabla = ttk.Treeview(frame_tabla, columns=("tipo", "lexema"), show="headings")
tabla.heading("tipo", text="Tipo de Token")
tabla.heading("lexema", text="Lexema")
tabla.column("tipo", width=250)
tabla.column("lexema", width=300)

scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)
tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

etiqueta_estado = tk.Label(ventana, text="", font=("Arial", 9), fg="#555")
etiqueta_estado.pack(anchor="w", padx=10, pady=(0, 8))

ventana.mainloop()
