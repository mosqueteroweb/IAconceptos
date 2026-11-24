"""Diagramas propios de la segunda parte del curso (SVG en docs/img/diagramas)."""
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs/img/diagramas"
FONT = "font-family='Inter, Segoe UI, Helvetica, Arial, sans-serif'"
C = dict(ink="#1f2933", sub="#52606d", blue="#3b6fd8", teal="#14918a", amber="#d98a1c", red="#d1495b",
         violet="#7a5cc7", green="#3d9a50", line="#9aa5b1", bg="#ffffff", soft="#f3f5f8")


def svg(name, w, h, body):
    s = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' {FONT}>"
         f"<rect width='{w}' height='{h}' rx='14' fill='{C['bg']}'/>{body}</svg>")
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")


def t(x, y, s, size=15, fill=None, anchor="middle", weight=400, italic=False):
    st = " font-style='italic'" if italic else ""
    return (f"<text x='{x}' y='{y}' font-size='{size}' fill='{fill or C['ink']}' text-anchor='{anchor}' "
            f"font-weight='{weight}'{st}>{s}</text>")


def box(x, y, w, h, lab, col, sub=None, size=15, sub2=None):
    s = (f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='#ffffff'/>"
         f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='{col}' fill-opacity='0.14' stroke='{col}' stroke-width='2'/>")
    n = 1 + (sub is not None) + (sub2 is not None)
    y0 = y + h / 2 - (n - 1) * 9 + 5
    s += t(x + w / 2, y0, lab, size, C['ink'], weight=600)
    if sub:
        s += t(x + w / 2, y0 + 19, sub, 12, C['sub'])
    if sub2:
        s += t(x + w / 2, y0 + 36, sub2, 12, C['sub'])
    return s


def arrow(x1, y1, x2, y2, col=None, dash=False, w=2.2):
    col = col or C['line']
    a = math.atan2(y2 - y1, x2 - x1); L = 10
    p1 = (x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4)); p2 = (x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
    d = " stroke-dasharray='6 5'" if dash else ""
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}'{d}/>"
            f"<polygon points='{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}' fill='{col}'/>")


# 1. Ciclo de vida de un LLM (mapa de la segunda parte)
b = t(450, 36, "Ciclo de vida de un modelo de lenguaje", 19, weight=700)
etapas = [
    ("Pre-entrenamiento", "predecir el siguiente", "token con billones", C['blue'], "Módulo 21"),
    ("Modelo base", "sabe lenguaje,", "no sigue órdenes", C['sub'], ""),
    ("Ajuste (fine-tuning)", "instrucciones,", "estilo, tareas", C['teal'], "Módulo 18"),
    ("Compresión", "cuantización", "y destilación", C['violet'], "Módulos 19-20"),
    ("Inferencia", "chat, API, local,", "agentes", C['amber'], "Módulos 12-17"),
]
x = 20
for i, (lab, s1, s2, col, mod) in enumerate(etapas):
    b += box(x, 70, 160, 92, lab, col, s1, 14, s2)
    if mod:
        b += t(x + 80, 186, mod, 12, col, weight=600)
    if i < len(etapas) - 1:
        b += arrow(x + 160, 116, x + 180, 116)
    x += 176
b += t(450, 226, "«Crear tu propio LLM» (módulo 22) recorre el camino desde el ajuste hasta la inferencia en tu ordenador.", 13, C['sub'])
svg("ciclo-vida-llm", 900, 246, b)

# 2. Muestreo y temperatura
b = t(410, 34, "«El cielo de Madrid está…» — probabilidad del siguiente token", 17, weight=700)
palabras = ["despejado", "nublado", "azul", "gris", "precioso", "lleno", "morado"]
logits = [2.6, 2.2, 1.9, 1.3, 0.8, 0.2, -1.2]
def softmax(v, T):
    e = [math.exp(x / T) for x in v]; s = sum(e); return [x / s for x in e]
paneles = [(0.3, "Temperatura 0,3", "casi siempre la primera opción"), (1.0, "Temperatura 1", "reparte según el modelo"),
           (1.8, "Temperatura 1,8", "las raras ganan peso")]
for k, (T, tit, sub) in enumerate(paneles):
    ox = 20 + k * 268
    b += f"<rect x='{ox}' y='54' width='252' height='300' rx='10' fill='{C['soft']}'/>"
    b += t(ox + 126, 80, tit, 15, weight=700) + t(ox + 126, 99, sub, 12, C['sub'])
    ps = softmax(logits, T)
    acum = 0
    for i, (w, p) in enumerate(zip(palabras, ps)):
        y = 118 + i * 32
        dentro = acum < 0.9
        acum += p
        col = C['blue'] if dentro else C['line']
        b += t(ox + 82, y + 15, w, 12, C['ink'], anchor="end")
        b += f"<rect x='{ox + 90}' y='{y + 3}' width='{max(2, p * 140):.1f}' height='17' rx='3' fill='{col}'/>"
        b += t(ox + 96 + p * 140, y + 16, f"{p * 100:.0f} %", 11, C['sub'], anchor="start")
b += t(410, 376, "En azul, el «núcleo» de top-p = 0,9: solo se sortea entre esas palabras. Las grises quedan descartadas.", 13, C['sub'])
svg("muestreo", 820, 392, b)

# 3. Prefill y decodificación
b = t(410, 34, "Las dos fases de la inferencia", 18, weight=700)
b += f"<rect x='40' y='70' width='230' height='60' rx='8' fill='{C['violet']}' fill-opacity='0.2' stroke='{C['violet']}' stroke-width='2'/>"
b += t(155, 96, "Prefill: leer el prompt", 14, weight=600) + t(155, 116, "todos los tokens a la vez", 12, C['sub'])
for i in range(11):
    x = 290 + i * 46
    b += f"<rect x='{x}' y='70' width='38' height='60' rx='6' fill='{C['amber']}' fill-opacity='0.25' stroke='{C['amber']}' stroke-width='2'/>"
    b += t(x + 19, 105, f"t{i + 1}", 12, C['ink'])
b += t(540, 150, "Decodificación: un token cada vez (cada uno vuelve a entrar en el modelo)", 12, C['sub'])
b += arrow(40, 185, 270, 185, C['violet'])
b += t(155, 205, "Tiempo hasta el primer token (TTFT)", 13, C['violet'], weight=600)
b += arrow(290, 185, 790, 185, C['amber'])
b += t(540, 205, "Velocidad de generación: tokens por segundo (tok/s)", 13, C['amber'], weight=600)
b += t(410, 244, "El prefill depende sobre todo de la potencia de cálculo; la decodificación, del ancho de banda de memoria.", 13, C['sub'])
svg("prefill-decode", 820, 262, b)

# 4. Llamada a herramientas / MCP (diagrama de secuencia)
b = t(450, 34, "Cómo usa un modelo una herramienta (MCP)", 18, weight=700)
cols = [("Usuario", C['sub'], 100), ("Aplicación", C['blue'], 330), ("Modelo (LLM)", C['violet'], 570), ("Servidor MCP «reloj»", C['teal'], 800)]
for lab, col, x in cols:
    b += box(x - 90, 56, 180, 44, lab, col, size=14)
    b += f"<line x1='{x}' y1='100' x2='{x}' y2='420' stroke='{col}' stroke-width='2' stroke-dasharray='4 5' stroke-opacity='0.6'/>"
msgs = [(100, 330, "1 · «¿Qué hora es en Tokio?»", C['sub']),
        (330, 570, "2 · pregunta + lista de herramientas", C['blue']),
        (570, 330, "3 · pide: get_time(«Asia/Tokyo»)", C['violet']),
        (330, 800, "4 · la aplicación ejecuta la herramienta", C['blue']),
        (800, 330, "5 · resultado: 03:15", C['teal']),
        (330, 570, "6 · le pasa el resultado", C['blue']),
        (570, 330, "7 · «En Tokio son las 03:15»", C['violet']),
        (330, 100, "8 · respuesta final", C['blue'])]
for i, (x1, x2, lab, col) in enumerate(msgs):
    y = 135 + i * 37
    b += arrow(x1, y, x2 + (-8 if x2 > x1 else 8), y, col)
    b += t((x1 + x2) / 2, y - 7, lab, 12, col, weight=600)
b += t(450, 446, "El modelo nunca ejecuta nada: solo escribe la petición en formato estructurado (JSON) y la aplicación decide si la cumple.", 13, C['sub'])
svg("tool-calling", 900, 466, b)

# 5. Bucle de un agente y orquestador
b = t(450, 34, "Un agente es un modelo que trabaja en bucle", 18, weight=700)
cx, cy, r = 220, 205, 112
pasos = [("Pensar", "planifica el", "siguiente paso", C['violet'], -90), ("Actuar", "usa una", "herramienta", C['blue'], 30),
         ("Observar", "lee el", "resultado", C['teal'], 150)]
b += f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='none' stroke='{C['line']}' stroke-width='2' stroke-dasharray='5 6'/>"
for lab, s1, s2, col, ang in pasos:
    x = cx + r * math.cos(math.radians(ang)); y = cy + r * math.sin(math.radians(ang))
    b += box(x - 62, y - 32, 124, 64, lab, col, s1, 14, s2)
b += t(cx, cy - 2, "Objetivo", 14, C['ink'], weight=700) + t(cx, cy + 16, "«ordena mis", 12, C['sub']) + t(cx, cy + 31, "facturas»", 12, C['sub'])
b += t(cx, 370, "Repite hasta cumplir el objetivo (o pedir ayuda)", 12, C['sub'])
b += box(540, 70, 220, 60, "Orquestador", C['amber'], "reparte y revisa", 15)
for i, (lab, sub) in enumerate([("Agente investigador", "busca en la web"), ("Agente programador", "escribe código"),
                                ("Agente revisor", "comprueba el trabajo")]):
    y = 175 + i * 70
    b += box(600, y, 220, 54, lab, C['blue'], sub, 13)
    b += arrow(578, y + 27, 600, y + 27, C['amber'])
b += f"<line x1='578' y1='130' x2='578' y2='{175 + 2 * 70 + 27}' stroke='{C['amber']}' stroke-width='2.2'/>"
b += t(690, 400, "Varios agentes coordinados = sistema multiagente", 12, C['sub'])
svg("agente-bucle", 900, 416, b)

# 6. LoRA
b = t(410, 34, "LoRA: congelar el modelo y entrenar dos matrices pequeñas", 17, weight=700)
b += f"<rect x='60' y='70' width='220' height='220' fill='{C['blue']}' fill-opacity='0.15' stroke='{C['blue']}' stroke-width='2'/>"
for i in range(1, 11):
    b += f"<line x1='{60 + i * 20}' y1='70' x2='{60 + i * 20}' y2='290' stroke='{C['blue']}' stroke-opacity='0.25'/>"
    b += f"<line x1='60' y1='{70 + i * 20}' x2='280' y2='{70 + i * 20}' stroke='{C['blue']}' stroke-opacity='0.25'/>"
b += t(170, 175, "W", 34, C['blue'], weight=700) + t(170, 205, "pesos originales", 13, C['sub']) + t(170, 222, "(congelados)", 13, C['sub'])
b += t(170, 316, "4096 × 4096 ≈ 16,8 millones", 12, C['sub'])
b += t(322, 188, "+", 34, C['ink'], weight=700)
b += f"<rect x='370' y='70' width='24' height='220' fill='{C['amber']}' fill-opacity='0.3' stroke='{C['amber']}' stroke-width='2'/>"
b += t(382, 312, "A", 18, C['amber'], weight=700)
b += t(420, 188, "×", 26, C['ink'], weight=700)
b += f"<rect x='446' y='168' width='220' height='24' fill='{C['amber']}' fill-opacity='0.3' stroke='{C['amber']}' stroke-width='2'/>"
b += t(556, 222, "B", 18, C['amber'], weight=700)
b += t(520, 266, "rango r = 16: 2 × 4096 × 16", 12, C['sub']) + t(520, 284, "≈ 131 000 parámetros (0,8 %)", 12, C['amber'], weight=600)
b += t(720, 175, "=", 30, C['ink'], weight=700)
b += t(770, 172, "W'", 26, C['teal'], weight=700) + t(770, 194, "ajustado", 12, C['sub'])
b += t(410, 350, "Solo se entrenan A y B. El resultado es un «adaptador» de pocos MB que se suma al modelo original.", 13, C['sub'])
svg("lora", 820, 370, b)

# 7. Cuantización
b = t(410, 34, "Cuantizar: redondear cada peso a uno de pocos valores", 17, weight=700)
b += f"<line x1='60' y1='120' x2='760' y2='120' stroke='{C['ink']}' stroke-width='2'/>"
b += t(60, 145, "−1,0", 12, C['sub']) + t(410, 145, "0", 12, C['sub']) + t(760, 145, "+1,0", 12, C['sub'])
b += t(30, 95, "16 bits", 13, C['blue'], weight=700, anchor="start")
import random
random.seed(7)
pesos = [max(-0.98, min(0.98, random.gauss(0, 0.38))) for _ in range(70)]
for p in pesos:
    x = 410 + p * 350
    b += f"<line x1='{x:.1f}' y1='104' x2='{x:.1f}' y2='120' stroke='{C['blue']}' stroke-width='2'/>"
niveles = [-1 + 2 * i / 15 for i in range(16)]
b += f"<line x1='60' y1='240' x2='760' y2='240' stroke='{C['ink']}' stroke-width='2'/>"
b += t(30, 215, "4 bits: 16 niveles", 13, C['amber'], weight=700, anchor="start")
for n in niveles:
    x = 410 + n * 350
    b += f"<circle cx='{x:.1f}' cy='240' r='6' fill='{C['amber']}'/>"
for p in pesos[:26]:
    q = min(niveles, key=lambda n: abs(n - p))
    b += f"<line x1='{410 + p * 350:.1f}' y1='122' x2='{410 + q * 350:.1f}' y2='233' stroke='{C['line']}' stroke-opacity='0.6'/>"
b += t(410, 290, "Cada peso se guarda como el número del nivel más cercano (0-15) más una «escala» por bloque de pesos.", 13, C['sub'])
b += t(410, 312, "Un modelo de 8000 millones de parámetros pasa de ~16 GB (16 bits) a ~4,9 GB (Q4_K_M).", 13, C['sub'], weight=600)
svg("cuantizacion", 820, 332, b)

# 8. Destilación
b = t(450, 34, "Destilación: el estudiante imita las probabilidades del profesor", 17, weight=700)
b += box(20, 150, 120, 60, "Datos", C['sub'], "frases, preguntas")
b += box(220, 70, 200, 70, "Modelo profesor", C['blue'], "grande y lento", 15)
b += box(220, 220, 200, 70, "Modelo estudiante", C['teal'], "pequeño y rápido", 15)
b += arrow(140, 170, 220, 110) + arrow(140, 190, 220, 250)
def barras(ox, oy, vals, col):
    s = ""
    for i, v in enumerate(vals):
        s += f"<rect x='{ox + i * 34}' y='{oy + 60 - v * 60:.1f}' width='26' height='{v * 60:.1f}' rx='3' fill='{col}'/>"
    return s
b += barras(470, 60, [0.72, 0.2, 0.06, 0.02], C['blue']) + t(530, 145, "etiquetas blandas", 12, C['blue'], weight=600)
b += barras(470, 215, [0.5, 0.3, 0.12, 0.08], C['teal']) + t(530, 300, "predicción del estudiante", 12, C['teal'], weight=600)
b += arrow(420, 105, 462, 100) + arrow(420, 255, 462, 255)
b += box(660, 140, 220, 80, "Pérdida", C['amber'], "parecerse al profesor", 15, "+ acertar la etiqueta")
b += arrow(610, 100, 680, 140, C['blue']) + arrow(610, 255, 680, 220, C['teal'])
b += f"<path d='M770 220 C 770 330, 330 340, 320 292' fill='none' stroke='{C['amber']}' stroke-width='2.2' stroke-dasharray='6 5'/>"
b += arrow(321, 300, 320, 292, C['amber'])
b += t(560, 336, "se ajustan solo los pesos del estudiante", 12, C['amber'], weight=600)
svg("destilacion", 900, 356, b)

# 9. Flujo de una API
b = t(410, 34, "Qué pasa cuando llamas a la API de un modelo", 18, weight=700)
b += box(30, 90, 180, 80, "Tu programa", C['blue'], "curl, un agente,", sub2="JavaScript…")
b += box(610, 90, 180, 80, "Servidor del modelo", C['violet'], "OpenAI, Google,", sub2="o LM Studio local")
b += arrow(210, 112, 610, 112, C['blue'])
b += t(410, 98, "Petición HTTP POST + clave (API key)", 13, C['blue'], weight=600)
b += t(410, 134, "{ \"model\": \"…\", \"input\": \"Hola\" }", 12, C['ink'])
b += arrow(610, 158, 210, 158, C['violet'])
b += t(410, 184, "Respuesta en JSON: texto generado + tokens usados", 13, C['violet'], weight=600)
b += t(410, 230, "La API no recuerda nada entre peticiones: para conversar hay que reenviar el historial cada vez.", 13, C['sub'])
svg("api-flujo", 820, 250, b)

# 10. Skills frente a MCP
b = t(410, 34, "Habilidades y conectores: dos formas de ampliar un modelo", 17, weight=700)
b += box(300, 130, 220, 80, "Modelo / agente", C['violet'], "razona y decide", 16)
b += box(20, 70, 230, 200, "", C['amber'])
b += t(135, 98, "Habilidad (Skill)", 16, C['amber'], weight=700) + t(135, 120, "carpeta con SKILL.md", 12, C['sub'])
for i, s in enumerate(["instrucciones: «cómo se hace»", "plantillas y ejemplos", "scripts opcionales", "se carga solo cuando hace falta"]):
    b += t(40, 152 + i * 26, "• " + s, 12, C['ink'], anchor="start")
b += box(570, 70, 230, 200, "", C['teal'])
b += t(685, 98, "Conector (MCP)", 16, C['teal'], weight=700) + t(685, 120, "servidor con herramientas", 12, C['sub'])
for i, s in enumerate(["acceso a datos: Drive, correo…", "acciones: crear, enviar, buscar", "permisos de tu cuenta", "estándar abierto (2024)"]):
    b += t(590, 152 + i * 26, "• " + s, 12, C['ink'], anchor="start")
b += arrow(250, 170, 300, 170, C['amber']) + arrow(570, 170, 520, 170, C['teal'])
b += t(410, 300, "La habilidad enseña el procedimiento; el conector da acceso a las herramientas. Se combinan.", 13, C['sub'])
svg("skills-mcp", 820, 320, b)
print("Diagramas de la parte 2 generados")

# 11. Benchmark real de la práctica de cuantización (Qwen3-0.6B, Mac mini M2 Pro, llama.cpp con Metal)
datos = [("BF16", 1510, 124.2), ("Q8_0", 805, 120.3), ("Q4_K_M", 484, 160.8), ("Q2_K", 347, 195.0)]
b = t(320, 32, "Qwen3-0.6B cuantizado: tamaño y velocidad", 17, weight=700)
for k, (tit, idx, maxv, col, fmt) in enumerate([("Tamaño del archivo (MB)", 1, 1600, C['blue'], "{:.0f}"),
                                                ("Velocidad (tokens/s)", 2, 220, C['teal'], "{:.0f}")]):
    ox = 30 + k * 300
    b += t(ox + 135, 64, tit, 14, col, weight=700)
    b += f"<line x1='{ox}' y1='260' x2='{ox + 270}' y2='260' stroke='{C['line']}'/>"
    for i, d in enumerate(datos):
        v = d[idx]; h = v / maxv * 170; x = ox + 14 + i * 64
        b += f"<rect x='{x}' y='{260 - h:.1f}' width='44' height='{h:.1f}' rx='4' fill='{col}'/>"
        b += t(x + 22, 252 - h, fmt.format(v), 12, C['ink'], weight=600)
        b += t(x + 22, 280, d[0], 12, C['sub'])
b += t(320, 312, "Medido con el cuaderno del módulo 19 en un Mac mini M2 Pro (llama.cpp, GPU integrada).", 12, C['sub'])
svg("benchmark-cuantizacion", 640, 330, b)

print("Diagramas extra generados")
