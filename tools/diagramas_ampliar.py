"""Diagramas de las páginas de ampliación del módulo 8: el Transformer y los modelos de difusión.

Uso: .venv/bin/python tools/diagramas_ampliar.py
Escribe en docs/img/diagramas/ los archivos transformer-*.svg y difusion-*.(svg|webp).
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "docs/img/diagramas"
OUT.mkdir(parents=True, exist_ok=True)
FONT = "font-family='Inter, Segoe UI, Helvetica, Arial, sans-serif'"
C = dict(ink="#1f2933", sub="#52606d", blue="#3b6fd8", teal="#14918a", amber="#d98a1c", red="#d1495b",
         violet="#7a5cc7", green="#3d9a50", line="#9aa5b1", bg="#ffffff", soft="#f3f5f8")


def svg(name, w, h, body):
    s = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' {FONT}>"
         f"<rect width='{w}' height='{h}' rx='14' fill='{C['bg']}'/>{body}</svg>")
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")


def t(x, y, s, size=15, fill=None, anchor="middle", weight=400, opacity=1):
    return (f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill or C['ink']}' text-anchor='{anchor}' "
            f"font-weight='{weight}' fill-opacity='{opacity}'>{s}</text>")


def box(x, y, w, h, lab, col, sub=None, size=15):
    s = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='{col}' fill-opacity='0.14' stroke='{col}' stroke-width='2'/>"
    s += t(x + w / 2, y + h / 2 + (-3 if sub else 5), lab, size, C['ink'], weight=600)
    if sub:
        s += t(x + w / 2, y + h / 2 + 17, sub, 12.5, C['sub'])
    return s


def arrow(x1, y1, x2, y2, col=None, width=2.2):
    col = col or C['line']
    a = math.atan2(y2 - y1, x2 - x1)
    L = 10
    p1 = (x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4))
    p2 = (x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{width}'/>"
            f"<polygon points='{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}' fill='{col}'/>")


def chips(palabras, x0, y, alto=36, hueco=8, por_letra=8.6, color=None, resaltar=()):
    """Dibuja palabras en cajitas y devuelve (svg, centros)."""
    s, centros, x = "", [], x0
    for p in palabras:
        w = len(p) * por_letra + 20
        hl = p in resaltar
        col = C['amber'] if hl else (color or C['line'])
        fondo = C['amber'] if hl else C['soft']
        s += (f"<rect x='{x:.1f}' y='{y}' width='{w:.1f}' height='{alto}' rx='8' fill='{fondo}' "
              f"fill-opacity='{0.3 if hl else 1}' stroke='{col}'/>")
        s += t(x + w / 2, y + alto / 2 + 5, p, 14.5, weight=700 if hl else 400)
        centros.append(x + w / 2)
        x += w + hueco
    return s, centros


def arco(x1, x2, y, peso, col):
    medio = (x1 + x2) / 2
    alto = 22 + abs(x1 - x2) * 0.33
    return (f"<path d='M {x1:.1f} {y} Q {medio:.1f} {y - alto:.1f} {x2:.1f} {y}' stroke='{col}' "
            f"stroke-opacity='{0.35 + 0.65 * peso:.2f}' stroke-width='{1.4 + peso * 4.5:.1f}' fill='none'/>")


# ------------------------------------------------------------------ Transformer
# T1. Antes (leer palabra a palabra) frente a Transformer (todas a la vez)
pal = ["El", "perro", "persigue", "al", "gato"]
xs = [90 + i * 145 for i in range(5)]
b = t(380, 36, "Antes: las redes leían una palabra detrás de otra", 16, C['violet'], weight=700)
for i, (x, p) in enumerate(zip(xs, pal)):
    op = [0.3, 0.45, 0.62, 0.8, 1][i]
    b += (f"<rect x='{x - 52}' y='56' width='104' height='40' rx='8' fill='{C['violet']}' fill-opacity='{0.14 * op:.2f}' "
          f"stroke='{C['violet']}' stroke-opacity='{op}' stroke-width='2'/>") + t(x, 81, p, 15, weight=600, opacity=op)
    if i < 4:
        b += arrow(x + 54, 76, xs[i + 1] - 56, 76, C['violet'])
b += t(380, 124, "Cuando llega a «gato», lo del principio ya se ha desdibujado. Y no se puede leer en paralelo: es lento.", 13, C['sub'])
b += t(380, 178, "Transformer: todas las palabras a la vez", 16, C['blue'], weight=700)
y2 = 268
for x, p in zip(xs, pal):
    b += (f"<rect x='{x - 52}' y='{y2}' width='104' height='40' rx='8' fill='{C['blue']}' fill-opacity='0.14' "
          f"stroke='{C['blue']}' stroke-width='2'/>") + t(x, y2 + 25, p, 15, weight=600)
for i in range(5):
    for j in range(i + 1, 5):
        medio = (xs[i] + xs[j]) / 2
        alto = 14 + (xs[j] - xs[i]) * 0.12
        b += f"<path d='M {xs[i]} {y2} Q {medio} {y2 - alto} {xs[j]} {y2}' stroke='{C['blue']}' stroke-opacity='0.55' stroke-width='1.8' fill='none'/>"
b += t(380, 336, "Cada palabra se conecta directamente con todas las demás, por lejos que estén, y se calcula todo a la vez.", 13, C['sub'])
svg("transformer-antes-ahora", 760, 356, b)

# T2. El camino: del texto al siguiente token
filas = [
    ("1 · Texto", C['sub'], None),
    ("2 · Tokens", C['teal'], None),
    ("3 · Vectores", C['violet'], "cada token se convierte en una lista de números (su significado) y su posición"),
    ("4 · Bloques Transformer", C['blue'], "cada capa: atención (mira las otras palabras) + una red neuronal"),
    ("5 · Siguiente token", C['amber'], None),
]
b = ""
for i, (lab, col, desc) in enumerate(filas):
    y = 24 + i * 92
    b += box(30, y, 230, 62, lab, col, size=16)
    if i < 4:
        b += arrow(145, y + 64, 145, y + 90, C['sub'])
    yc = y + 31
    if i == 0:
        b += t(290, yc + 6, "«El gato se sentó en la»", 17, anchor="start", weight=600)
    elif i == 1:
        s, _ = chips(["El", "gato", "se", "sentó", "en", "la"], 290, y + 13, alto=34, color=C['teal'])
        b += s
    elif i == 2:
        for k in range(6):
            xb = 290 + k * 52
            for m, h in enumerate([0.6, 0.25, 0.85, 0.45]):
                b += f"<rect x='{xb + m * 9}' y='{y + 8 + (1 - h) * 26:.1f}' width='7' height='{h * 26:.1f}' fill='{C['violet']}' fill-opacity='0.7'/>"
        b += t(290, y + 56, desc, 12.5, C['sub'], anchor="start")
    elif i == 3:
        for k in range(3):
            b += (f"<rect x='{300 + k * 8}' y='{y + 6 + k * 6}' width='120' height='26' rx='6' fill='{C['bg']}' "
                  f"stroke='{C['blue']}' stroke-width='1.8'/>")
        b += t(376, y + 36, "atención + red", 12.5, C['blue'], weight=600)
        b += t(450, y + 26, "× decenas de capas", 14, C['blue'], anchor="start", weight=700)
        b += t(290, y + 62, desc, 12.5, C['sub'], anchor="start")
    else:
        for k, (w, p) in enumerate([("alfombra", 0.31), ("silla", 0.22), ("cama", 0.17)]):
            xb = 290 + k * 150
            b += f"<rect x='{xb}' y='{y + 10}' width='{p * 300:.0f}' height='16' rx='4' fill='{C['amber']}' fill-opacity='{1 - k * 0.25}'/>"
            b += t(xb, y + 44, f"{w} {int(p * 100)} %", 13.5, anchor="start", weight=600)
svg("transformer-camino", 760, 480, b)

# T3. La atención cambia el significado: «banco»
b = t(380, 34, "La atención cambia el significado de una palabra según su contexto", 16, weight=700)
s, cx = chips(["En", "el", "parque", "me", "senté", "en", "un", "banco"], 30, 120, resaltar=("banco",))
b += s
for k, peso in [(2, 1.0), (4, 0.75), (7, 0)]:
    if k != 7:
        b += arco(cx[7], cx[k], 118, peso, C['red'])
b += t(530, 144, "«banco» = asiento", 16, C['teal'], anchor="start", weight=700)
s, cx = chips(["Para", "sacar", "dinero", "fui", "al", "banco"], 30, 238, resaltar=("banco",))
b += s
for k, peso in [(2, 1.0), (1, 0.6)]:
    b += arco(cx[5], cx[k], 236, peso, C['red'])
b += t(530, 262, "«banco» = entidad bancaria", 16, C['violet'], anchor="start", weight=700)
b += t(380, 306, "Las líneas salen de «banco» hacia las palabras en las que más se fija (cuanto más gruesa, más atención).", 13, C['sub'])
b += t(380, 326, "Su vector se mezcla con el de esas palabras: el modelo obtiene un «banco» distinto en cada frase.", 13, C['sub'])
svg("transformer-banco", 760, 346, b)

# T4. Generar: un token cada vez
pasos = [("El gato se", "sentó"), ("El gato se sentó", "en"), ("El gato se sentó en", "la")]
b = t(380, 34, "Generar texto: un token cada vez", 16, weight=700)
for i, (txt, nuevo) in enumerate(pasos):
    y = 66 + i * 78
    b += t(322, y + 27, f"«{txt}»", 15.5, anchor="end", weight=600)
    b += arrow(332, y + 22, 372, y + 22, C['sub'])
    b += box(378, y, 150, 44, "Transformer", C['blue'])
    b += arrow(530, y + 22, 570, y + 22, C['sub'])
    b += (f"<rect x='576' y='{y + 2}' width='96' height='40' rx='8' fill='{C['amber']}' fill-opacity='0.3' "
          f"stroke='{C['amber']}' stroke-width='2'/>") + t(624, y + 28, nuevo, 15.5, weight=700)
    if i < 2:
        b += (f"<path d='M 624 {y + 44} C 624 {y + 66}, 360 {y + 52}, 330 {y + 66}' stroke='{C['amber']}' "
              f"stroke-width='1.8' fill='none' stroke-dasharray='5 4'/>")
        b += f"<polygon points='330,{y + 66} 341,{y + 59} 339,{y + 70}' fill='{C['amber']}'/>"
        b += t(500, y + 76, "se añade al texto", 12, C['amber'], weight=600)
b += t(380, 316, "Cada token nuevo se añade al texto y el modelo vuelve a empezar con todo lo escrito.", 13, C['sub'])
b += t(380, 336, "Al generar, cada palabra solo puede fijarse en las anteriores: las siguientes todavía no existen.", 13, C['sub'])
svg("transformer-bucle", 760, 356, b)

# ------------------------------------------------------------------ Difusión
# D1. Entrenamiento: ensuciar y adivinar el ruido
b = t(380, 34, "Entrenamiento: ensuciar una imagen y aprender a adivinar el ruido", 16, weight=700)
b += box(30, 62, 210, 64, "Imagen + descripción", C['teal'], "«una casa con tejado rojo»")
b += arrow(242, 94, 282, 94, C['sub'])
b += box(286, 62, 190, 64, "Se le añade ruido", C['sub'], "una cantidad al azar")
b += arrow(478, 94, 518, 94, C['sub'])
b += box(522, 62, 210, 64, "La red adivina el ruido", C['blue'], "con ayuda de la descripción")
b += arrow(627, 128, 627, 178, C['sub'])
b += box(522, 182, 210, 64, "Se compara", C['red'], "con el ruido que se echó")
b += arrow(520, 214, 480, 214, C['sub'])
b += box(286, 182, 190, 64, "Error", C['red'], "cuánto se ha equivocado")
b += arrow(284, 214, 244, 214, C['sub'])
b += box(30, 182, 210, 64, "Se ajustan los pesos", C['violet'], "para equivocarse menos")
b += t(380, 288, "Se repite con millones de imágenes y niveles de ruido distintos. Al final, la red sabe", 13, C['sub'])
b += t(380, 308, "«limpiar» un poco cualquier imagen con ruido, y sabe qué aspecto tiene lo que describe el texto.", 13, C['sub'])
svg("difusion-entrenamiento", 760, 326, b)

# D2. Espacio latente
b = t(380, 34, "Espacio latente: trabajar con una versión comprimida de la imagen", 16, weight=700)
b += box(24, 70, 150, 80, "Imagen", C['teal'], "512 × 512 píxeles")
b += t(99, 172, "786 432 números", 12.5, C['sub'])
b += arrow(176, 110, 212, 110, C['sub'])
b += box(216, 80, 110, 60, "Comprime", C['sub'], size=14)
b += arrow(328, 110, 364, 110, C['sub'])
b += box(368, 86, 120, 48, "Latente", C['violet'], "64 × 64")
b += t(428, 172, "16 384 números", 12.5, C['sub'])
b += arrow(490, 110, 526, 110, C['sub'])
b += box(530, 80, 110, 60, "Descomprime", C['sub'], size=14)
b += arrow(642, 110, 678, 110, C['sub'])
b += box(680, 70, 60, 80, "Imagen", C['teal'], size=13)
b += (f"<path d='M 386 86 C 386 64, 470 64, 470 86' stroke='{C['amber']}' stroke-width='2' fill='none' stroke-dasharray='5 4'/>")
b += t(428, 52, "la difusión se hace aquí", 12.5, C['amber'], weight=700)
b += t(380, 212, "Unas 50 veces menos números: cada paso de quitar ruido es mucho más rápido.", 13, C['sub'])
b += t(380, 232, "Al final, la versión comprimida se «descomprime» en la imagen de tamaño completo.", 13, C['sub'])
svg("difusion-latente", 760, 252, b)


# ---------------------------------------------------- Difusión: imágenes ilustrativas (PIL)
def casa(W=220, cielo=(135, 196, 235), tejado=(190, 60, 55), puerta_x=98, sol=(150, 22), ventanas=2, suelo=(96, 168, 80)):
    im = Image.new("RGB", (W, W), cielo)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 150, W, W], fill=suelo)
    d.ellipse([sol[0], sol[1], sol[0] + 48, sol[1] + 48], fill=(250, 205, 60))
    d.polygon([(55, 95), (110, 50), (165, 95)], fill=tejado)
    d.rectangle([65, 95, 155, 160], fill=(240, 228, 205))
    d.rectangle([puerta_x, 120, puerta_x + 24, 160], fill=(120, 80, 50))
    huecos = [(75, 108), (130, 108)] if ventanas == 2 else [(75, 108)]
    for (vx, vy) in huecos:
        d.rectangle([vx, vy, vx + 17, vy + 17], fill=(120, 170, 220))
    return im


def mezcla(base, ruido_frac, desenfoque, semilla):
    rnd = random.Random(semilla)
    im = base.filter(ImageFilter.GaussianBlur(desenfoque)) if desenfoque else base.copy()
    p, q = im.load(), base.load()
    for yy in range(base.height):
        for xx in range(base.width):
            c = p[xx, yy]
            n = [rnd.gauss(128, 70) for _ in range(3)]
            p[xx, yy] = tuple(int(max(0, min(255, (1 - ruido_frac) * a + ruido_frac * m))) for a, m in zip(c, n))
    return im


def fuente(tam):
    for nombre in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nombre, tam)
        except OSError:
            pass
    return ImageFont.load_default()


# D3. Generación: del ruido a la imagen, guiado por el texto
W = 220
base = casa()
etapas = [("ruido puro", 1.0, 0), ("paso 15", 0.72, 16), ("paso 30", 0.45, 7), ("paso 45", 0.18, 2), ("paso 50", 0.0, 0)]
ancho = len(etapas) * (W + 20) + 20
tira = Image.new("RGB", (ancho, W + 120), "white")
dt = ImageDraw.Draw(tira)
f_t, f_s = fuente(22), fuente(18)
dt.text((20, 16), "Texto que escribimos: «una casa con tejado rojo y un sol»", fill=(31, 41, 51), font=f_t)
for k, (lab, r, blur) in enumerate(etapas):
    im = mezcla(base, r, blur, semilla=7)
    x = 20 + k * (W + 20)
    tira.paste(im, (x, 56))
    dt.text((x + W / 2, W + 76), lab, fill=(82, 96, 109), font=f_s, anchor="mm")
    if k < len(etapas) - 1:
        ax = x + W + 3
        dt.polygon([(ax, 56 + W / 2 - 7), (ax + 14, 56 + W / 2), (ax, 56 + W / 2 + 7)], fill=(82, 96, 109))
dt.text((ancho / 2, W + 104), "Primero aparecen las manchas grandes (cielo, suelo) y al final los detalles. (Ilustración)",
        fill=(82, 96, 109), font=f_s, anchor="mm")
tira.save(OUT / "difusion-generacion.webp", "WEBP", quality=88)

# D4. Mismo texto, distinto ruido de partida: imágenes distintas
variantes = [casa(),
             casa(cielo=(250, 190, 150), tejado=(90, 90, 160), puerta_x=70, sol=(20, 28), ventanas=1),
             casa(cielo=(170, 210, 245), tejado=(150, 100, 60), puerta_x=125, sol=(160, 10), suelo=(120, 150, 70))]
tira = Image.new("RGB", (3 * (W + 20) + 20, W + 96), "white")
dt = ImageDraw.Draw(tira)
dt.text((20, 16), "Mismo texto, «una casa con tejado y un sol», y tres ruidos de partida distintos", fill=(31, 41, 51), font=f_s)
for k, im in enumerate(variantes):
    x = 20 + k * (W + 20)
    tira.paste(im, (x, 50))
    dt.text((x + W / 2, W + 72), f"semilla {k + 1}", fill=(82, 96, 109), font=f_s, anchor="mm")
tira.save(OUT / "difusion-semillas.webp", "WEBP", quality=88)
print("Diagramas de ampliación listos")
