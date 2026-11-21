"""Ejecuta las cuadruplas que genera intermedio y comprueba que el programa haga lo mismo que el original.
Uso: python interpretar_tac.py [carpeta_de_pruebas] [ejecutable]
(Para cada archivo .salida, ejecuta el .txt del mismo nombre y compara lo que imprime.)
"""
import subprocess, sys, glob, os, math
RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
def fmt(v):
    if isinstance(v, float) and v == int(v): v = int(v)
    if v == 0: return "0"
    return str(v)
def correr(cuads):
    labels = {c[5]: i for i, c in enumerate(cuads) if c[2] == "label"}
    mem, salida, pc, pasos = {}, [], 0, 0
    def val(x):
        try: return int(x)
        except ValueError:
            try: return float(x)
            except ValueError: return mem[x]
    while pc < len(cuads):
        pasos += 1
        if pasos > 5_000_000: raise RuntimeError("bucle infinito")
        _, _, op, a, b, r = cuads[pc]; pc += 1
        if op == "=": mem[r] = val(a)
        elif op == "label": pass
        elif op == "goto": pc = labels[r]
        elif op == "ifFalse":
            if val(a) == 0: pc = labels[r]
        elif op == "print": salida.append(fmt(val(a)))
        else:
            x, y = val(a), val(b)
            mem[r] = {"+": lambda: x+y, "-": lambda: x-y, "*": lambda: x*y,
                      "/": lambda: x/y, "div": lambda: math.trunc(x/y),
                      "<": lambda: int(x<y), ">": lambda: int(x>y), "<=": lambda: int(x<=y),
                      ">=": lambda: int(x>=y), "==": lambda: int(x==y), "!=": lambda: int(x!=y)}[op]()
    return salida
fallas = 0
carpeta = sys.argv[1] if len(sys.argv) > 1 else RAIZ + "/pruebas/intermedio"
exe = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAIZ, "intermedio.exe" if os.name == "nt" else "intermedio")
for sal in sorted(glob.glob(carpeta + "/*.salida")):
    txt = sal[:-7] + ".txt"
    r = subprocess.run([exe, txt], capture_output=True, text=True)
    cuads = [l.split("\t") for l in r.stdout.splitlines() if l.startswith("CUADRUPLA")]
    esperado = open(sal).read().split()
    obtenido = correr(cuads)
    ok = obtenido == esperado and r.returncode == 0
    fallas += (not ok)
    print(f"{os.path.basename(txt):34} {'ok' if ok else 'FALLA'}  ({len(cuads)} cuadruplas)")
    if not ok: print("   esperado:", esperado, "\n   obtenido:", obtenido)
print("fallas:", fallas)
