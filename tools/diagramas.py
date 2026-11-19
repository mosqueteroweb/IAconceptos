"""Genera los diagramas propios del curso (SVG y WEBP) en docs/img/diagramas."""
import math, random
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "docs/img/diagramas"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "font-family='Inter, Segoe UI, Helvetica, Arial, sans-serif'"
C = dict(ink="#1f2933", sub="#52606d", blue="#3b6fd8", teal="#14918a", amber="#d98a1c", red="#d1495b",
         violet="#7a5cc7", green="#3d9a50", line="#9aa5b1", bg="#ffffff", soft="#f3f5f8")

def svg(name, w, h, body):
    s = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' {FONT}>"
         f"<rect width='{w}' height='{h}' rx='14' fill='{C['bg']}'/>{body}</svg>")
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")

def t(x, y, s, size=15, fill=None, anchor="middle", weight=400):
    return f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill or C['ink']}' text-anchor='{anchor}' font-weight='{weight}'>{s}</text>"

# 1. IA ⊃ ML ⊃ DL ⊃ IA generativa
b = ""
for r, col, lab, y in [(250, C['blue'], "Inteligencia Artificial", 70), (190, C['teal'], "Machine Learning", 135),
                       (130, C['violet'], "Deep Learning", 200), (70, C['amber'], "IA generativa", 268)]:
    b += f"<circle cx='300' cy='{290 + (250 - r) * 0.0}' r='{r}' fill='{col}' fill-opacity='0.13' stroke='{col}' stroke-width='2'/>"
b = ""
rings = [(255, C['blue'], "Inteligencia Artificial", "sistemas que hacen tareas «inteligentes»"),
         (195, C['teal'], "Machine Learning", "aprenden patrones a partir de datos"),
         (135, C['violet'], "Deep Learning", "redes neuronales con muchas capas"),
         (72, C['amber'], "IA generativa", "crean contenido nuevo")]
cy = 300
for r, col, lab, desc in rings:
    b += f"<circle cx='320' cy='{cy + 255 - r}' r='{r}' fill='{col}' fill-opacity='0.12' stroke='{col}' stroke-width='2.5'/>"
for r, col, lab, desc in rings:
    top = cy + 255 - 2 * r
    yy = top + (34 if r > 80 else 62)
    b += t(320, yy, lab, 19 if r > 80 else 16, col, weight=700) + t(320, yy + 20, desc, 13, C['sub'])
svg("ia-ml-dl", 640, 570, b)

# 2. Programación tradicional vs ML
def box(x, y, w, h, lab, col, sub=None):
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='{col}' fill-opacity='0.14' stroke='{col}' stroke-width='2'/>"
    s += t(x + w / 2, y + h / 2 + (0 if sub else 5), lab, 15, C['ink'], weight=600)
    if sub: s += t(x + w / 2, y + h / 2 + 20, sub, 12, C['sub'])
    return s
def arrow(x1, y1, x2, y2, col=None):
    col = col or C['line']
    a = math.atan2(y2 - y1, x2 - x1); L = 10
    p1 = (x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4)); p2 = (x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='2.2'/>"
            f"<polygon points='{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}' fill='{col}'/>")
b = t(370, 40, "Programación tradicional", 18, C['blue'], weight=700)
b += box(60, 70, 170, 50, "Reglas", C['blue'], "escritas por una persona") + box(60, 140, 170, 50, "Datos", C['blue'])
b += box(330, 105, 150, 50, "Programa", C['sub']) + box(570, 105, 130, 50, "Respuestas", C['green'])
b += arrow(230, 95, 330, 122) + arrow(230, 165, 330, 140) + arrow(480, 130, 570, 130)
b += t(370, 250, "Machine Learning", 18, C['teal'], weight=700)
b += box(60, 280, 170, 50, "Datos", C['teal']) + box(60, 350, 170, 50, "Respuestas", C['teal'], "ejemplos etiquetados")
b += box(330, 315, 150, 50, "Entrenamiento", C['sub']) + box(570, 315, 130, 50, "Reglas", C['amber'], "= el modelo")
b += arrow(230, 305, 330, 332) + arrow(230, 375, 330, 350) + arrow(480, 340, 570, 340)
svg("programacion-vs-ml", 760, 430, b)

# 3. Supervisado vs no supervisado (dispersión)
random.seed(4)
def cloud(cx, cy, n, sd):
    return [(random.gauss(cx, sd), random.gauss(cy, sd)) for _ in range(n)]
A, B, Cc = cloud(110, 230, 28, 26), cloud(230, 120, 28, 26), cloud(250, 260, 28, 24)
def panel(ox, title, groups, labeled):
    s = f"<clipPath id='c{ox}'><rect x='{ox}' y='60' width='340' height='300' rx='10'/></clipPath><rect x='{ox}' y='60' width='340' height='300' rx='10' fill='{C['soft']}'/>" + t(ox + 170, 42, title, 17, weight=700) + f"<g clip-path='url(#c{ox})'>"
    cols = [C['blue'], C['red'], C['green']]
    for gi, g in enumerate(groups):
        for (x, y) in g:
            if labeled:
                col = cols[gi]
                s += f"<circle cx='{ox + x:.1f}' cy='{y:.1f}' r='6' fill='{col}'/>"
            else:
                s += f"<circle cx='{ox + x:.1f}' cy='{y:.1f}' r='6' fill='{C['line']}'/>"
    return s + "</g>"
b = panel(20, "Supervisado: datos con etiqueta", [A, B, Cc], True)
for (x2, y2) in [(20, 120), (360, 140), (200, 360)]:
    b += f"<line x1='{20 + 175}' y1='190' x2='{x2}' y2='{y2}' stroke='{C['ink']}' stroke-dasharray='6 5' stroke-width='2'/>"
b += t(190, 385, "el modelo aprende la frontera entre clases", 13, C['sub'])
b += panel(400, "No supervisado: sin etiquetas", [A, B, Cc], False)
for (cx, cy, r, col) in [(110, 230, 70, C['blue']), (230, 120, 70, C['red']), (250, 262, 64, C['green'])]:
    b += f"<circle cx='{400 + cx}' cy='{cy}' r='{r}' fill='none' stroke='{col}' stroke-width='2.5' stroke-dasharray='7 5'/>"
b += t(570, 385, "el algoritmo descubre los grupos (clustering)", 13, C['sub'])
svg("supervisado-vs-no-supervisado", 760, 405, b)

# 4. Neurona artificial
b = ""
ins = [("x₁", "w₁", 90), ("x₂", "w₂", 170), ("x₃", "w₃", 250)]
for x, w, y in ins:
    b += f"<circle cx='70' cy='{y}' r='26' fill='{C['blue']}' fill-opacity='0.15' stroke='{C['blue']}' stroke-width='2'/>" + t(70, y + 6, x, 18, weight=600)
    b += arrow(96, y, 318, 170 + (y - 170) * 0.25, C['line']) + t(200, (y + 170) / 2 - 10 + (y - 170) * 0.1, w, 15, C['amber'], weight=700)
b += f"<circle cx='370' cy='170' r='52' fill='{C['teal']}' fill-opacity='0.15' stroke='{C['teal']}' stroke-width='2.5'/>"
b += t(370, 166, "Σ + b", 20, weight=700) + t(370, 190, "suma ponderada", 11, C['sub'])
b += arrow(422, 170, 488, 170)
b += f"<rect x='490' y='130' width='120' height='80' rx='12' fill='{C['violet']}' fill-opacity='0.14' stroke='{C['violet']}' stroke-width='2'/>"
b += f"<path d='M 505 190 L 540 190 Q 552 190 556 175 Q 560 150 595 150' stroke='{C['violet']}' stroke-width='3' fill='none'/>" + t(550, 228, "activación", 13, C['sub'])
b += arrow(612, 170, 680, 170) + t(712, 176, "salida", 15, weight=600)
b += t(70, 300, "entradas", 13, C['sub']) + t(200, 300, "pesos (importancia)", 13, C['sub']) + t(370, 300, "b = sesgo", 13, C['sub'])
svg("neurona", 770, 320, b)

# 5. Red neuronal por capas
layers = [(3, "Entrada", C['blue']), (5, "Oculta 1", C['teal']), (5, "Oculta 2", C['teal']), (4, "Oculta 3", C['teal']), (2, "Salida", C['amber'])]
xs = [80 + i * 150 for i in range(len(layers))]
pos = []
for (n, _, _), x in zip(layers, xs):
    pos.append([(x, 200 + (j - (n - 1) / 2) * 62) for j in range(n)])
b = ""
for i in range(len(pos) - 1):
    for (x1, y1) in pos[i]:
        for (x2, y2) in pos[i + 1]:
            b += f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{C['line']}' stroke-opacity='0.55' stroke-width='1.2'/>"
for (n, lab, col), ps, x in zip(layers, pos, xs):
    for (px, py) in ps:
        b += f"<circle cx='{px}' cy='{py}' r='17' fill='{C['bg']}' stroke='{col}' stroke-width='3'/>"
    b += t(x, 382, lab, 14, col, weight=700)
b += t(90, 200 - 100 - 25, "", 1)
b += t(xs[-1] + 0, 200 - 31 - 30, "gato 0,93", 12, C['sub']) + t(xs[-1], 200 + 31 + 40, "perro 0,07", 12, C['sub'])
b += arrow(80, 30, 680, 30, C['sub']) + t(380, 22, "propagación hacia delante (forward)", 13, C['sub'])
svg("red-por-capas", 760, 400, b)

# 6. Siguiente token
words = [("alfombra", 0.31), ("silla", 0.22), ("cama", 0.17), ("ventana", 0.09), ("mesa", 0.07), ("plátano", 0.001)]
b = t(30, 44, "«El gato se sentó en la …»", 20, anchor="start", weight=700) + t(30, 70, "probabilidad que asigna el modelo a cada posible continuación", 13, C['sub'], anchor="start")
for i, (w, p) in enumerate(words):
    y = 100 + i * 42
    b += t(150, y + 21, w, 15, anchor="end", weight=600)
    b += f"<rect x='165' y='{y + 4}' width='{max(3, p * 1500):.0f}' height='26' rx='5' fill='{C['teal'] if i == 0 else C['blue']}' fill-opacity='{1 if i == 0 else 0.55}'/>"
    b += t(165 + max(3, p * 1500) + 10, y + 22, f"{p * 100:.1f} %".replace(".", ","), 13, C['sub'], anchor="start")
svg("siguiente-token", 720, 365, b)

# 7. Atención
toks = ["El", "gato", "no", "cruzó", "la", "calle", "porque", "estaba", "cansado"]
xs = [50 + i * 78 for i in range(len(toks))]
b = t(380, 36, "Atención: ¿a qué palabras «mira» el modelo al procesar «cansado»?", 15, weight=700)
for x, w in zip(xs, toks):
    hl = w in ("cansado",)
    b += f"<rect x='{x - 34}' y='190' width='68' height='36' rx='8' fill='{C['amber'] if hl else C['soft']}' fill-opacity='{0.3 if hl else 1}' stroke='{C['amber'] if hl else C['line']}'/>" + t(x, 214, w, 14, weight=600 if hl else 400)
for target, wgt in [(1, 0.9), (3, 0.25), (5, 0.35), (7, 0.3)]:
    x1, x2 = xs[-1], xs[target]
    mid = (x1 + x2) / 2; hgt = 40 + (x1 - x2) * 0.32
    b += f"<path d='M {x1} 188 Q {mid} {188 - hgt} {x2} 188' stroke='{C['red']}' stroke-opacity='{wgt}' stroke-width='{1.5 + wgt * 5:.1f}' fill='none'/>"
b += t(380, 262, "La línea más gruesa va a «gato»: el modelo entiende que quien está cansado es el gato, no la calle.", 13, C['sub'])
svg("atencion", 760, 285, b)

# 8. Pila de software
stack = [("5 · Código y arquitectura del modelo", "scripts propios en Python", C['amber']),
         ("4 · Librerías de alto nivel", "Hugging Face Transformers · PEFT · Accelerate", C['violet']),
         ("3 · Entrenamiento distribuido", "PyTorch FSDP · DeepSpeed · Megatron", C['teal']),
         ("2 · Framework de Deep Learning", "PyTorch · JAX", C['blue']),
         ("1 · Drivers y runtimes", "CUDA · cuDNN · NCCL (o ROCm en AMD)", C['green']),
         ("0 · Hardware", "GPUs · red InfiniBand · almacenamiento NVMe", C['sub'])]
b = ""
for i, (lab, sub, col) in enumerate(stack):
    w = 330 + i * 70; x = 380 - w / 2; y = 20 + i * 66
    b += f"<rect x='{x}' y='{y}' width='{w}' height='56' rx='10' fill='{col}' fill-opacity='0.15' stroke='{col}' stroke-width='2'/>"
    b += t(380, y + 24, lab, 15, weight=700) + t(380, y + 44, sub, 12.5, C['sub'])
svg("pila-software", 760, 420, b)

# 9. Pirámide de riesgos AI Act
lv = [("Riesgo inaceptable", "prohibido", C['red']), ("Alto riesgo", "requisitos estrictos", C['amber']),
      ("Riesgo limitado", "obligación de transparencia", "#c9b52a"), ("Riesgo mínimo", "sin obligaciones nuevas", C['green'])]
b = ""; top = 30; H = 300; base = 600
for i, (lab, sub, col) in enumerate(lv):
    y0 = top + i * H / 4; y1 = top + (i + 1) * H / 4
    w0 = base * (i / 4) + 40 * (i == 0) * 0; w1 = base * ((i + 1) / 4)
    cx = 300
    b += f"<polygon points='{cx - w0 / 2},{y0} {cx + w0 / 2},{y0} {cx + w1 / 2},{y1} {cx - w1 / 2},{y1}' fill='{col}' fill-opacity='0.85' stroke='#fff' stroke-width='3'/>"
    b += t(cx + w1 / 2 + 20, (y0 + y1) / 2 - 2, lab, 15, anchor="start", weight=700) + t(cx + w1 / 2 + 20, (y0 + y1) / 2 + 17, sub, 12.5, C['sub'], anchor="start")
b += t(380, 360, "Reglamento Europeo de IA (UE 2024/1689): las obligaciones dependen del riesgo", 13, C['sub'])
svg("ai-act-riesgos", 760, 380, b)

# 10. Ciclo de entrenamiento
steps = [("1 · Predicción", "forward", C['blue']), ("2 · Error", "función de pérdida", C['red']),
         ("3 · Retropropagación", "¿quién tuvo la culpa?", C['violet']), ("4 · Ajuste de pesos", "descenso del gradiente", C['teal'])]
b = ""; cx, cy, R = 380, 210, 135
for i, (lab, sub, col) in enumerate(steps):
    a = -math.pi / 2 + i * math.pi / 2
    x, y = cx + R * 1.45 * math.cos(a), cy + R * math.sin(a)
    b += f"<rect x='{x - 105}' y='{y - 30}' width='210' height='60' rx='12' fill='{col}' fill-opacity='0.14' stroke='{col}' stroke-width='2'/>" + t(x, y - 3, lab, 15, weight=700) + t(x, y + 17, sub, 12.5, C['sub'])
for i in range(4):
    a1 = -math.pi / 2 + i * math.pi / 2 + 0.42; a2 = a1 + math.pi / 2 - 0.84
    x1, y1 = cx + R * 0.9 * math.cos(a1), cy + R * 0.75 * math.sin(a1); x2, y2 = cx + R * 0.9 * math.cos(a2), cy + R * 0.75 * math.sin(a2)
    b += arrow(x1, y1, x2, y2, C['sub'])
b += t(cx, cy - 4, "se repite", 15, C['sub'], weight=600) + t(cx, cy + 16, "millones de veces", 13, C['sub'])
svg("ciclo-entrenamiento", 760, 420, b)
print("SVG ok")

# 11. Difusión (imagen real con ruido creciente)
from PIL import Image, ImageDraw
import random as rnd
W = 220
base = Image.new("RGB", (W, W), (135, 196, 235)); d = ImageDraw.Draw(base)
d.rectangle([0, 150, W, W], fill=(96, 168, 80)); d.ellipse([150, 22, 198, 70], fill=(250, 205, 60))
d.polygon([(55, 95), (110, 50), (165, 95)], fill=(190, 60, 55)); d.rectangle([65, 95, 155, 160], fill=(240, 228, 205))
d.rectangle([98, 120, 122, 160], fill=(120, 80, 50)); d.rectangle([75, 108, 92, 125], fill=(120, 170, 220)); d.rectangle([130, 108, 147, 125], fill=(120, 170, 220))
levels = [0, 0.25, 0.5, 0.75, 1.0]
strip = Image.new("RGB", (len(levels) * (W + 20) + 20, W + 70), "white"); ds = ImageDraw.Draw(strip)
px = base.load(); rnd.seed(1)
for k, a in enumerate(levels):
    im = base.copy(); p = im.load()
    for yy in range(W):
        for xx in range(W):
            r, g, bb = px[xx, yy]
            n = [rnd.gauss(128, 70) for _ in range(3)]
            p[xx, yy] = tuple(int(max(0, min(255, (1 - a) * c + a * m))) for c, m in zip((r, g, bb), n))
    strip.paste(im, (20 + k * (W + 20), 20))
    ds.text((20 + k * (W + 20) + 70, W + 32), f"ruido {int(a * 100)} %", fill=(60, 60, 60))
strip.save(OUT / "difusion.webp", "WEBP", quality=88)
print("difusion ok")
