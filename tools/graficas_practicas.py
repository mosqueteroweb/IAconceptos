# /// script
# dependencies = ["matplotlib"]
# ///
"""Gráficas de los ejemplos resueltos de las prácticas, con los datos reales medidos en el Mac (M2 Pro).

uv run tools/graficas_practicas.py   →   docs/img/practicas/*.svg
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
DATOS = json.loads((RAIZ / "tools/datos_graficas_practicas.json").read_text())
SALIDA = RAIZ / "docs/img/practicas"
SALIDA.mkdir(parents=True, exist_ok=True)
AZUL, VERDE, NARANJA, GRIS = "#3b6fd8", "#14918a", "#e07a2e", "#6b7280"
plt.rcParams.update({"font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none",
                     "figure.facecolor": "white", "axes.facecolor": "white"})

def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(SALIDA / f"{nombre}.svg")
    plt.close(fig)

# Práctica 14: velocidad y primer token por pregunta
p = DATOS["p14"]; preguntas = ["1. Fotosíntesis", "2. Consejos", "3. Traducción", "4. Tren", "5. Poema"]
fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.9))
x = range(len(preguntas)); w = 0.38
for i, (m, nombre, color) in enumerate([("google/gemma-4-e2b", "Gemma 4 E2B Q4_K_M", AZUL), ("qwen/qwen3-1.7b", "Qwen3 1.7B MLX 8 bits", VERDE)]):
    a.bar([j + (i - .5) * w for j in x], p[m]["tps"], w, label=nombre, color=color)
    b.bar([j + (i - .5) * w for j in x], [v * 1000 for v in p[m]["ttft"]], w, label=nombre, color=color)
for eje, titulo, unidad in ((a, "Velocidad de generación (media de 3)", "tokens/s"), (b, "Tiempo hasta el primer token (media de 3)", "milisegundos")):
    eje.set_xticks(list(x)); eje.set_xticklabels([q.split(". ")[1] for q in preguntas], rotation=0)
    eje.set_title(titulo, fontsize=10); eje.set_ylabel(unidad); eje.grid(axis="y", alpha=.3)
fig.legend(*a.get_legend_handles_labels(), loc="upper center", ncol=2, frameon=False, fontsize=9)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig(SALIDA / "p14-benchmark.svg"); plt.close(fig)

# Práctica 18: pérdida por paso, 3 y 6 épocas
fig, a = plt.subplots(figsize=(7.5, 3.6))
for e, color in (("6", NARANJA), ("3", AZUL)):
    v = DATOS["p18"][e]; a.plot(range(1, len(v) + 1), v, color=color, lw=1.6, label=f"{e} épocas ({len(v)} pasos)")
a.set_xlabel("paso de entrenamiento"); a.set_ylabel("pérdida de entrenamiento"); a.grid(alpha=.3); a.legend()
a.set_title("Asistente formal (Qwen3-1.7B, LoRA en Mac, datos en formato de chat)", fontsize=10)
guardar(fig, "p18-perdida")

# Práctica 19: tamaño frente a perplejidad
versiones = ["BF16", "Q8_0", "Q4_K_M", "Q2_K"]; tam = [1509, 805, 484, 347]; ppl = [56.42, 56.43, 62.21, 885.30]
fig, a = plt.subplots(figsize=(7, 3.8))
a.plot(tam, ppl, "o-", color=AZUL); a.set_yscale("log")
for t, p_, v in zip(tam, ppl, versiones):
    a.annotate(f"{v}\n{p_:.2f}".replace(".", ","), (t, p_), textcoords="offset points", xytext=(-42, -8) if v == "Q2_K" else (8, 6), fontsize=9)
a.set_xlabel("tamaño del archivo (MB)"); a.set_ylabel("perplejidad (escala logarítmica)"); a.grid(alpha=.3, which="both")
a.set_xlim(1600, 280); a.set_ylim(40, 1500); a.set_title("Qwen3-0.6B: cuanto más comprimido, peor predice (el «codo» está tras Q4_K_M)", fontsize=10)
guardar(fig, "p19-tamano-perplejidad")

# Práctica 20: pérdida del estudiante
v = DATOS["p20"]
fig, a = plt.subplots(figsize=(7, 3.4))
a.plot(range(1, len(v) + 1), v, color=VERDE, lw=1.6)
a.set_xlabel("paso de entrenamiento"); a.set_ylabel("pérdida de entrenamiento"); a.grid(alpha=.3)
a.set_title("Destilación: Qwen3-0.6B aprendiendo de Gemma 4 E2B (110 respuestas, 3 épocas)", fontsize=10)
guardar(fig, "p20-perdida")

# Práctica 21: las tres ejecuciones
fig, ejes = plt.subplots(1, 3, figsize=(11, 3.5))
for eje, (clave, titulo) in zip(ejes, (("4capas", "Por defecto (4 capas, 3,2 M)"), ("2capas", "Con 2 capas (1,7 M)"), ("llama", "nano-Llama (15,8 M)"))):
    pasos, ent, val = zip(*DATOS["p21"][clave])
    eje.plot(pasos, ent, "o-", ms=3, color=AZUL, label="entrenamiento"); eje.plot(pasos, val, "o-", ms=3, color=NARANJA, label="validación")
    eje.set_title(titulo, fontsize=10); eje.set_xlabel("paso"); eje.grid(alpha=.3)
ejes[0].set_ylabel("pérdida"); ejes[0].legend(fontsize=8)
guardar(fig, "p21-perdidas")
print("Gráficas en", SALIDA)
