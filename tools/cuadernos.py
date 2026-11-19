"""Genera los cuadernos de Colab del curso en notebooks/.

Cada cuaderno está pensado para quien no programa: se ejecuta celda a celda
(botón ▶ o Mayús+Intro) y cada paso viene explicado en lenguaje llano.
"""
from pathlib import Path
import nbformat as nbf

OUT = Path(__file__).resolve().parent.parent / "notebooks"
OUT.mkdir(exist_ok=True)
REPO = "mosqueteroweb/IAconceptos"


def colab_badge(name):
    url = f"https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{name}"
    return f"[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({url})"


def build(name, cells):
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
        "accelerator": "GPU",
        "colab": {"provenance": []},
    }
    out = []
    for kind, src in cells:
        src = src.strip("\n")
        out.append(nbf.v4.new_markdown_cell(src) if kind == "md" else nbf.v4.new_code_cell(src))
    nb.cells = out
    nbf.write(nb, OUT / name)


INTRO = """
> **Cómo usar este cuaderno.** No hace falta saber programar. Ejecuta las celdas **en orden**, de arriba abajo,
> con el botón ▶ que aparece a su izquierda (o con **Mayús + Intro**). Lee el texto que hay antes de cada celda:
> explica qué va a pasar. Si algo falla, usa *Entorno de ejecución → Reiniciar y ejecutar todo*.
"""

# ---------------------------------------------------------------------------
# 1. Pre-entrenamiento de un nano-modelo con el Quijote
# ---------------------------------------------------------------------------
build("nanomodelo-quijote.ipynb", [
    ("md", f"""
# Práctica: pre-entrenar un nano-modelo con el Quijote

{colab_badge("nanomodelo-quijote.ipynb")}

Vamos a **entrenar desde cero** un modelo de lenguaje diminuto (unos 3 millones de parámetros) usando solo el texto de
*Don Quijote de la Mancha*. Es la misma receta que el pre-entrenamiento de un LLM gigante —tokenizar, predecir el
siguiente token, corregir el error millones de veces—, pero a escala de juguete.

{INTRO}

**Antes de empezar:** en Colab, menú *Entorno de ejecución → Cambiar tipo de entorno de ejecución → GPU T4*.
Con GPU tarda unos 3 minutos; sin GPU, unos 15.

Basado en el ejemplo [nanoGPT](https://github.com/karpathy/nanoGPT) de Andrej Karpathy. Material del curso
[IAconceptos](https://mosqueteroweb.github.io/IAconceptos/) · MosqueteroWeb · CC BY-SA 4.0.
"""),
    ("md", """
## Paso 1. Descargar el libro

Descargamos el texto completo del Quijote desde el [Proyecto Gutenberg](https://www.gutenberg.org/ebooks/2000)
(dominio público) y quitamos la licencia que Gutenberg añade al principio y al final. Si el servidor principal no
responde, el código prueba con dos copias espejo.
"""),
    ("code", """
import urllib.request

FUENTES = [
    "https://www.gutenberg.org/cache/epub/2000/pg2000.txt",
    "https://gutenberg.pglaf.org/2/0/0/2000/2000-0.txt",
    "https://mirrors.xmission.com/gutenberg/2/0/0/2000/2000-0.txt",
]
texto = None
for url in FUENTES:
    try:
        peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        bruto = urllib.request.urlopen(peticion, timeout=30).read().decode("utf-8")
        if "START OF" in bruto:
            texto = bruto
            break
    except Exception as error:
        print("No se pudo usar", url, "→", error)

inicio = texto.index("START OF")
inicio = texto.index("\\n", inicio) + 1
fin = texto.index("*** END OF")
texto = texto[inicio:fin].strip()
print(f"Caracteres del libro: {len(texto):,}")
print(texto[:400])
"""),
    ("md", """
## Paso 2. El tokenizador

Un modelo solo entiende números. Nuestro tokenizador será el más simple posible: **cada carácter es un token**.
El vocabulario es la lista de caracteres distintos que aparecen en el libro (letras, tildes, signos…), y a cada uno
le damos un número. Los LLM reales usan tokens de **sub-palabra** (trozos como «caball» + «ero»), pero la idea es la misma.
"""),
    ("code", """
caracteres = sorted(set(texto))
tamano_vocabulario = len(caracteres)
a_numero = {c: i for i, c in enumerate(caracteres)}
a_caracter = {i: c for i, c in enumerate(caracteres)}

def codificar(cadena):
    return [a_numero[c] for c in cadena]

def decodificar(numeros):
    return "".join(a_caracter[n] for n in numeros)

print("Vocabulario:", "".join(caracteres))
print("Tamaño del vocabulario:", tamano_vocabulario)
print("«DON QUIJOTE» en tokens:", codificar("DON QUIJOTE"))
print("Y de vuelta a texto:", decodificar(codificar("DON QUIJOTE")))
"""),
    ("md", """
## Paso 3. Preparar los datos

Convertimos el libro entero en una larga lista de números. Guardamos el 90 % para **entrenar** y el 10 % final
para **validar**: son páginas que el modelo nunca verá durante el entrenamiento y que sirven para comprobar si
generaliza o solo memoriza.

La tarea del modelo será siempre la misma: dado un trozo de texto, **predecir el siguiente carácter**.
"""),
    ("code", """
import torch

torch.manual_seed(1605)  # año de la primera edición: así los resultados son repetibles
dispositivo = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
print("Entrenaremos en:", dispositivo)

datos = torch.tensor(codificar(texto), dtype=torch.long)
corte = int(0.9 * len(datos))
datos_entreno, datos_validacion = datos[:corte], datos[corte:]

CONTEXTO = 128   # cuántos caracteres "mira hacia atrás" el modelo
LOTE = 32        # cuántos fragmentos procesa a la vez

def lote(parte):
    fuente = datos_entreno if parte == "entreno" else datos_validacion
    posiciones = torch.randint(len(fuente) - CONTEXTO, (LOTE,))
    x = torch.stack([fuente[p:p + CONTEXTO] for p in posiciones])
    y = torch.stack([fuente[p + 1:p + CONTEXTO + 1] for p in posiciones])  # el mismo texto, desplazado un carácter
    return x.to(dispositivo), y.to(dispositivo)

x, y = lote("entreno")
print("Entrada :", repr(decodificar(x[0][:40].tolist())))
print("Objetivo:", repr(decodificar(y[0][:40].tolist())))
"""),
    ("md", """
## Paso 4. La arquitectura: un Transformer en miniatura

Esta celda define el modelo. No hace falta entenderla línea a línea: es un **Transformer** como el de los módulos 5 y 8,
con sus piezas clave:

- **Embeddings**: convierten cada token (y su posición) en un vector de números.
- **Atención**: cada carácter «mira» a los anteriores para decidir qué es relevante.
- **Bloques apilados**: repetimos atención + red neuronal 4 veces.
- **Cabeza de salida**: da una probabilidad para cada carácter del vocabulario.
"""),
    ("code", """
import torch.nn as nn
from torch.nn import functional as F

DIM = 256       # tamaño de los vectores (embeddings)
CABEZAS = 4     # cabezas de atención
CAPAS = 4       # bloques Transformer
DROPOUT = 0.2   # apaga neuronas al azar durante el entrenamiento para evitar memorizar

class Bloque(nn.Module):
    def __init__(self):
        super().__init__()
        self.norma1 = nn.LayerNorm(DIM)
        self.atencion = nn.MultiheadAttention(DIM, CABEZAS, dropout=DROPOUT, batch_first=True)
        self.norma2 = nn.LayerNorm(DIM)
        self.red = nn.Sequential(nn.Linear(DIM, 4 * DIM), nn.GELU(), nn.Linear(4 * DIM, DIM), nn.Dropout(DROPOUT))

    def forward(self, x):
        T = x.shape[1]
        mascara = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1)  # no mirar el futuro
        h = self.norma1(x)
        x = x + self.atencion(h, h, h, attn_mask=mascara, need_weights=False)[0]
        return x + self.red(self.norma2(x))

class NanoModelo(nn.Module):
    def __init__(self):
        super().__init__()
        self.tokens = nn.Embedding(tamano_vocabulario, DIM)
        self.posiciones = nn.Embedding(CONTEXTO, DIM)
        self.bloques = nn.Sequential(*[Bloque() for _ in range(CAPAS)])
        self.norma = nn.LayerNorm(DIM)
        self.salida = nn.Linear(DIM, tamano_vocabulario)

    def forward(self, idx, objetivos=None):
        T = idx.shape[1]
        x = self.tokens(idx) + self.posiciones(torch.arange(T, device=idx.device))
        logits = self.salida(self.norma(self.bloques(x)))
        perdida = None
        if objetivos is not None:
            perdida = F.cross_entropy(logits.view(-1, logits.size(-1)), objetivos.view(-1))
        return logits, perdida

    @torch.no_grad()
    def generar(self, idx, nuevos, temperatura=0.8):
        for _ in range(nuevos):
            logits, _ = self(idx[:, -CONTEXTO:])
            probabilidades = F.softmax(logits[:, -1, :] / temperatura, dim=-1)
            siguiente = torch.multinomial(probabilidades, num_samples=1)  # muestreo: no siempre el más probable
            idx = torch.cat([idx, siguiente], dim=1)
        return idx

modelo = NanoModelo().to(dispositivo)
print(f"Parámetros del modelo: {sum(p.numel() for p in modelo.parameters()) / 1e6:.2f} millones")
"""),
    ("md", """
## Paso 5. Antes de entrenar: un modelo que no sabe nada

Sus parámetros son números al azar, así que genera caracteres sin sentido. Fíjate en el resultado para compararlo
después.
"""),
    ("code", """
def escribir(comienzo="DON QUIJOTE", caracteres=300, temperatura=0.8):
    modelo.eval()
    inicio = torch.tensor([codificar(comienzo)], dtype=torch.long, device=dispositivo)
    print(decodificar(modelo.generar(inicio, caracteres, temperatura)[0].tolist()))
    modelo.train()

escribir()
"""),
    ("md", """
## Paso 6. El pre-entrenamiento

Este es el bucle que, a gran escala, cuesta millones de euros. En cada paso:

1. Tomamos 32 fragmentos del libro al azar.
2. El modelo predice el siguiente carácter en cada posición.
3. Medimos el error con la **pérdida** (*loss*): cuanto más baja, mejor predice.
4. La **retropropagación** ajusta un poquito los 3 millones de parámetros para reducir ese error.

Cada 500 pasos mostramos la pérdida con textos de entrenamiento y de validación. Si las dos bajan juntas, el modelo
está aprendiendo de verdad; si la de validación se queda atrás, empieza a memorizar.
"""),
    ("code", """
import time

PASOS = 5000
optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4)
historial = []

@torch.no_grad()
def evaluar():
    modelo.eval()
    resultado = {}
    for parte in ("entreno", "validacion"):
        resultado[parte] = torch.stack([modelo(*lote(parte))[1] for _ in range(50)]).mean().item()
    modelo.train()
    return resultado

comienzo = time.time()
for paso in range(PASOS + 1):
    if paso % 500 == 0:
        p = evaluar()
        historial.append((paso, p["entreno"], p["validacion"]))
        print(f"Paso {paso:5d} · pérdida entreno {p['entreno']:.3f} · validación {p['validacion']:.3f} · {time.time() - comienzo:4.0f} s")
    if paso == PASOS:
        break
    x, y = lote("entreno")
    _, perdida = modelo(x, y)
    optimizador.zero_grad(set_to_none=True)
    perdida.backward()
    optimizador.step()
"""),
    ("code", """
import matplotlib.pyplot as plt

pasos, entreno, validacion = zip(*historial)
plt.figure(figsize=(7, 4))
plt.plot(pasos, entreno, marker="o", label="entrenamiento")
plt.plot(pasos, validacion, marker="o", label="validación")
plt.xlabel("pasos de entrenamiento"); plt.ylabel("pérdida (menos es mejor)")
plt.title("Así aprende el nano-modelo"); plt.legend(); plt.grid(alpha=0.3)
plt.show()
"""),
    ("md", """
## Paso 7. ¡A escribir como Cervantes (más o menos)!

Ahora el modelo ha aprendido la ortografía, las palabras frecuentes y hasta el ritmo de los diálogos del libro.
No esperes coherencia: con 3 millones de parámetros y un solo libro no puede entender la historia. Pero compáralo
con el Paso 5.

Prueba a cambiar el **comienzo** y la **temperatura**: baja (0,3) da textos repetitivos y «seguros»; alta (1,3) da
textos más locos. Es el mismo parámetro que ajustas en LM Studio o ChatGPT (módulo 12).
"""),
    ("code", """
escribir("DON QUIJOTE", temperatura=0.8)
print("\\n" + "-" * 60 + "\\n")
escribir("—Mire vuestra merced", temperatura=0.5)
"""),
    ("md", """
## ¿Y puedo usarlo en LM Studio?

No directamente. LM Studio y Ollama cargan arquitecturas conocidas (Llama, Qwen, Gemma…) en formato GGUF, y la
nuestra es casera. Para eso habría que reescribirla con una arquitectura estándar de Hugging Face. Lo importante
de esta práctica es otra cosa: **has hecho un pre-entrenamiento completo**, con los mismos pasos que un modelo
gigante. La diferencia es de escala: datos (2 MB frente a decenas de billones de tokens), parámetros (3 millones
frente a cientos de miles de millones) y cómputo (minutos en una GPU frente a meses en miles).

**Para seguir:** cambia `CAPAS`, `DIM` o `PASOS` y observa cómo cambian el tiempo y la pérdida. O sustituye el
Quijote por otro libro de Gutenberg.
"""),
])

# ---------------------------------------------------------------------------
# 2. Cuantización con llama.cpp
# ---------------------------------------------------------------------------
build("cuantizacion.ipynb", [
    ("md", f"""
# Práctica: cuantizar un modelo con llama.cpp

{colab_badge("cuantizacion.ipynb")}

Vamos a tomar un modelo pequeño en su formato original (16 bits por parámetro) y a **comprimirlo** a 8, 4 y 2 bits
con [llama.cpp](https://github.com/ggml-org/llama.cpp), la misma herramienta que usan por dentro LM Studio y Ollama.
Después compararemos tamaño, velocidad y calidad de respuesta.

{INTRO}

**No necesita GPU**: funciona en el entorno gratuito normal de Colab (CPU). Tarda unos 10 minutos.

El modelo es [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) (Alibaba, licencia Apache 2.0, sin registro).
Material del curso [IAconceptos](https://mosqueteroweb.github.io/IAconceptos/) · MosqueteroWeb · CC BY-SA 4.0.
"""),
    ("md", """
## Paso 1. Instalar llama.cpp

Descargamos la última versión ya compilada de llama.cpp desde GitHub (no hay que compilar nada) y el *script* de
conversión, que está escrito en Python.
"""),
    ("code", """
import json, platform, subprocess, sys, tarfile, urllib.request, os
from pathlib import Path

sistema = platform.system()
sufijo = "bin-ubuntu-x64.tar.gz" if sistema == "Linux" else "bin-macos-arm64.tar.gz"
version = json.load(urllib.request.urlopen("https://api.github.com/repos/ggml-org/llama.cpp/releases?per_page=1"))[0]
paquete = next(a for a in version["assets"] if a["name"].endswith(sufijo) and a["name"].startswith("llama-"))
print("Descargando", paquete["name"])
urllib.request.urlretrieve(paquete["browser_download_url"], "llama.tar.gz")
with tarfile.open("llama.tar.gz") as t:
    t.extractall("llama", filter="data")
BIN = next(p.parent for p in Path("llama").rglob("llama-quantize"))
print("Programas en:", BIN)

# El script de conversión de la misma versión
etiqueta = version["tag_name"]
subprocess.run(["git", "clone", "--depth", "1", "--branch", etiqueta,
                "https://github.com/ggml-org/llama.cpp.git", "llama-src"], check=True, capture_output=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "llama-src/requirements/requirements-convert_hf_to_gguf.txt"], check=True)
print("Listo:", etiqueta)
"""),
    ("md", """
## Paso 2. Descargar el modelo original

Bajamos el modelo tal y como lo publica su autor en Hugging Face: pesos en formato *safetensors* a 16 bits.
"""),
    ("code", """
from huggingface_hub import snapshot_download

carpeta = snapshot_download("Qwen/Qwen3-0.6B", local_dir="qwen-original")
tamano = sum(f.stat().st_size for f in Path(carpeta).glob("*.safetensors"))
print(f"Tamaño de los pesos originales: {tamano / 1e9:.2f} GB")
"""),
    ("md", """
## Paso 3. Convertir a GGUF (sin cuantizar todavía)

**GGUF** es el formato de archivo único que entienden LM Studio, Ollama y llama.cpp: guarda en un solo fichero los
pesos, el tokenizador y la información de la arquitectura. Primero lo convertimos manteniendo los 16 bits (BF16).
"""),
    ("code", """
subprocess.run([sys.executable, "llama-src/convert_hf_to_gguf.py", "qwen-original",
                "--outtype", "bf16", "--outfile", "qwen-bf16.gguf"], check=True, capture_output=True)
print(f"qwen-bf16.gguf: {Path('qwen-bf16.gguf').stat().st_size / 1e9:.2f} GB")
"""),
    ("md", """
## Paso 4. Cuantizar a varios niveles

Ahora sí: `llama-quantize` redondea cada peso a menos bits. Probamos tres niveles:

| Tipo | Bits aprox. | Qué es |
|---|---|---|
| `Q8_0` | 8,5 | Casi sin pérdida. Redondeo simple a 8 bits. |
| `Q4_K_M` | 4,8 | El equilibrio habitual: el que verás más en LM Studio. |
| `Q2_K` | 2,6 | Compresión extrema: se nota la pérdida de calidad. |
"""),
    ("code", """
tamanos = {"BF16": Path("qwen-bf16.gguf").stat().st_size / 1e6}
for tipo in ["Q8_0", "Q4_K_M", "Q2_K"]:
    salida = f"qwen-{tipo}.gguf"
    subprocess.run([str(BIN / "llama-quantize"), "qwen-bf16.gguf", salida, tipo], check=True, capture_output=True)
    tamanos[tipo] = Path(salida).stat().st_size / 1e6
    print(f"{tipo:7s} → {tamanos[tipo]:6.0f} MB  ({100 * tamanos[tipo] / tamanos['BF16']:.0f} % del original)")
"""),
    ("md", """
## Paso 5. Comparar velocidad y respuestas

Hacemos la misma pregunta a cada versión y medimos cuántos **tokens por segundo** genera. Con temperatura 0 el modelo
elige siempre la palabra más probable, así las diferencias se deben solo a la cuantización.
"""),
    ("code", """
import re

PREGUNTA = "Explica en dos frases qué es la fotosíntesis."
# Plantilla de chat de Qwen3: así el modelo sabe que es una conversación (y /no_think le pide responder sin "pensar")
PROMPT = f"<|im_start|>user\\n{PREGUNTA} /no_think<|im_end|>\\n<|im_start|>assistant\\n<think>\\n\\n</think>\\n\\n"
resultados = {}
for tipo in ["BF16", "Q8_0", "Q4_K_M", "Q2_K"]:
    archivo = "qwen-bf16.gguf" if tipo == "BF16" else f"qwen-{tipo}.gguf"
    r = subprocess.run([str(BIN / "llama-completion"), "-m", archivo, "-p", PROMPT, "-n", "120",
                        "--temp", "0", "--repeat-penalty", "1.1", "-no-cnv", "--no-warmup", "--no-display-prompt"],
                       capture_output=True, text=True)
    velocidad = re.search(r"eval time.*?([\\d.]+) tokens per second", r.stderr.split("prompt eval time")[-1])
    resultados[tipo] = float(velocidad.group(1)) if velocidad else float("nan")
    print(f"=== {tipo} · {resultados[tipo]:.1f} tokens/s ===")
    print(r.stdout.strip()[:600], "\\n")
"""),
    ("code", """
import matplotlib.pyplot as plt

tipos = list(resultados)
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.8))
a.bar(tipos, [tamanos[t] for t in tipos], color="#3b6fd8"); a.set_title("Tamaño del archivo (MB)")
b.bar(tipos, [resultados[t] for t in tipos], color="#14918a"); b.set_title("Velocidad (tokens/s)")
for eje in (a, b):
    eje.grid(axis="y", alpha=0.3)
plt.tight_layout(); plt.show()
"""),
    ("md", """
## Paso 6. Llévatelo a LM Studio

Descarga el archivo `qwen-Q4_K_M.gguf` (panel de archivos de la izquierda → tres puntos → Descargar). En LM Studio,
abre una terminal y ejecuta `lms import qwen-Q4_K_M.gguf`, o arrastra el archivo a la ventana de *My Models*.

**Para pensar:** ¿la versión `Q2_K` contesta igual de bien? ¿Merece la pena el ahorro? En modelos grandes (30 000
millones de parámetros o más) la pérdida de `Q4_K_M` apenas se nota; en uno tan pequeño como este, sí.
"""),
])

# ---------------------------------------------------------------------------
# 3. Destilación de un clasificador de sentimientos
# ---------------------------------------------------------------------------
build("destilacion.ipynb", [
    ("md", f"""
# Práctica: destilar un modelo profesor en un modelo estudiante

{colab_badge("destilacion.ipynb")}

Un modelo **profesor** (DistilBERT, 67 millones de parámetros), ya entrenado para saber si una reseña de cine en
inglés es positiva o negativa, va a enseñar a un modelo **estudiante** 15 veces más pequeño (BERT-tiny,
4,4 millones). La pregunta de la práctica: ¿puede el profesor sustituir a las personas que etiquetan datos?

{INTRO}

**Antes de empezar:** en Colab, *Entorno de ejecución → Cambiar tipo → GPU T4*. Tarda unos 10 minutos.

Datos: [SST-2](https://huggingface.co/datasets/stanfordnlp/sst2), reseñas de cine en inglés etiquetadas por personas.
Material del curso [IAconceptos](https://mosqueteroweb.github.io/IAconceptos/) · MosqueteroWeb · CC BY-SA 4.0.
"""),
    ("code", """
!pip install -q transformers datasets scikit-learn accelerate
"""),
    ("md", """
## Paso 1. El profesor, el estudiante y los datos

- **Profesor:** `distilbert-base-uncased-finetuned-sst-2-english`, ya especializado en sentimientos.
- **Estudiante:** `google/bert_uncased_L-2_H-128_A-2` (conocido como *BERT-tiny*), un BERT minúsculo que todavía no
  sabe nada de sentimientos.
- **Datos:** 30 000 frases de entrenamiento y las 872 de validación de SST-2.

Los dos modelos comparten el mismo vocabulario (el de BERT en minúsculas), así que leen exactamente los mismos tokens.
"""),
    ("code", """
import torch, time
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification

torch.manual_seed(0)
PROFESOR = "distilbert-base-uncased-finetuned-sst-2-english"
ESTUDIANTE = "google/bert_uncased_L-2_H-128_A-2"  # «BERT-tiny»: 2 capas, 128 dimensiones
dispositivo = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

tokenizador = AutoTokenizer.from_pretrained(PROFESOR)
profesor = AutoModelForSequenceClassification.from_pretrained(PROFESOR).to(dispositivo).eval()

datos = load_dataset("stanfordnlp/sst2")
mezclado = datos["train"].shuffle(seed=0)

def tokenizar(lote):
    return tokenizador(lote["sentence"], truncation=True, max_length=64)
pocas = mezclado.select(range(1_000)).map(tokenizar, batched=True).rename_column("label", "labels")
muchas = mezclado.select(range(30_000)).map(tokenizar, batched=True).rename_column("label", "labels")
validacion = datos["validation"].map(tokenizar, batched=True).rename_column("label", "labels")

millones = lambda m: sum(p.numel() for p in m.parameters()) / 1e6
print(f"Profesor: {millones(profesor):.1f} M parámetros")
print(f"Estudiante: {millones(AutoModelForSequenceClassification.from_pretrained(ESTUDIANTE, num_labels=2)):.1f} M parámetros")
"""),
    ("md", """
## Paso 2. Lo que sabe el profesor: «etiquetas blandas»

El profesor no solo dice «positiva»: da una **probabilidad** para cada opción. Esa información extra —que una frase
es *casi* positiva, o que duda— es el «conocimiento oscuro» que el estudiante intentará copiar. Fíjate también en que
el profesor **no es perfecto**.
"""),
    ("code", """
frases = ["A masterpiece, moving and beautifully acted.",
          "It was fine, I guess, but I wouldn't watch it again.",
          "Two hours of my life I will never get back."]
with torch.no_grad():
    entradas = tokenizador(frases, return_tensors="pt", padding=True).to(dispositivo)
    probabilidades = torch.softmax(profesor(**entradas).logits, dim=-1)
for frase, (neg, pos) in zip(frases, probabilidades.tolist()):
    print(f"{pos:6.1%} positiva · {neg:6.1%} negativa  ←  {frase}")
"""),
    ("md", """
## Paso 3. El entrenador de destilación

El estudiante destilado **no ve las etiquetas humanas**. Su único objetivo es que sus probabilidades se parezcan a las
del profesor. Las dos distribuciones se «suavizan» con una **temperatura** (2) para que se vean mejor los matices, y la
diferencia entre ellas se mide con la *divergencia de Kullback-Leibler*.
"""),
    ("code", """
import torch.nn.functional as F
from transformers import Trainer, TrainingArguments, DataCollatorWithPadding
from sklearn.metrics import accuracy_score

TEMPERATURA = 2.0

class EntrenadorDestilacion(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        inputs.pop("labels")                      # ¡las etiquetas humanas se tiran!
        salida = model(**inputs)
        profesor.to(model.device)
        with torch.no_grad():
            logits_profesor = profesor(**inputs).logits
        perdida = F.kl_div(F.log_softmax(salida.logits / TEMPERATURA, dim=-1),
                           F.softmax(logits_profesor / TEMPERATURA, dim=-1),
                           reduction="batchmean") * TEMPERATURA ** 2
        return (perdida, salida) if return_outputs else perdida

def metricas(prediccion):
    return {"accuracy": accuracy_score(prediccion.label_ids, prediccion.predictions.argmax(-1))}

def entrenar(datos, clase=Trainer, epocas=3):
    modelo = AutoModelForSequenceClassification.from_pretrained(ESTUDIANTE, num_labels=2)
    argumentos = TrainingArguments(output_dir="salida", num_train_epochs=epocas, learning_rate=1e-3,
                                   per_device_train_batch_size=64, per_device_eval_batch_size=128,
                                   eval_strategy="no", save_strategy="no", report_to=[], logging_steps=100)
    entrenador = clase(model=modelo, args=argumentos, train_dataset=datos, eval_dataset=validacion,
                       data_collator=DataCollatorWithPadding(tokenizador), compute_metrics=metricas)
    entrenador.train()
    return modelo, entrenador.evaluate()["eval_accuracy"]
"""),
    ("md", """
## Paso 4. Entrenar tres estudiantes

Entrenamos tres copias idénticas del estudiante, que solo se diferencian en de quién aprenden:

1. **1 000 frases etiquetadas por personas.** Lo que tendrías si etiquetar a mano fuera caro.
2. **30 000 frases etiquetadas por personas.** El caso ideal, y el más caro.
3. **Las mismas 30 000 frases, sin etiquetas humanas, aprendiendo solo del profesor.**
"""),
    ("code", """
_, acierto_pocas = entrenar(pocas, epocas=5)
_, acierto_muchas = entrenar(muchas)
estudiante, acierto_destilado = entrenar(muchas, clase=EntrenadorDestilacion)
"""),
    ("md", """
## Paso 5. Resultados
"""),
    ("code", """
evaluador = Trainer(model=profesor, args=TrainingArguments(output_dir="salida", report_to=[], per_device_eval_batch_size=128),
                    data_collator=DataCollatorWithPadding(tokenizador), compute_metrics=metricas)
acierto_profesor = evaluador.evaluate(validacion)["eval_accuracy"]

def velocidad(modelo, repeticiones=20):
    modelo = modelo.to(dispositivo).eval()
    entradas = tokenizador(list(validacion["sentence"][:128]), return_tensors="pt", padding=True).to(dispositivo)
    with torch.no_grad():
        modelo(**entradas)
        inicio = time.time()
        for _ in range(repeticiones):
            modelo(**entradas)
    return 128 * repeticiones / (time.time() - inicio)

print(f"{'':42s}{'Acierto':>9s}{'Frases/s':>10s}")
print(f"{'Profesor (67 M)':42s}{acierto_profesor:9.1%}{velocidad(profesor):10.0f}")
print(f"{'Estudiante · 1 000 etiquetas humanas':42s}{acierto_pocas:9.1%}")
print(f"{'Estudiante · 30 000 etiquetas humanas':42s}{acierto_muchas:9.1%}")
print(f"{'Estudiante · 30 000 frases, solo profesor':42s}{acierto_destilado:9.1%}{velocidad(estudiante):10.0f}")
"""),
    ("md", """
## ¿Qué ha pasado?

- El estudiante es **15 veces más pequeño** y decenas de veces **más rápido** que el profesor. Pierde acierto: un
  modelo tan diminuto no puede igualar al grande.
- El estudiante destilado **no ha visto ni una etiqueta humana** y, aun así, queda prácticamente empatado (a un
  punto, arriba o abajo según la ejecución) con el que aprendió de 30 000 etiquetas puestas a mano, y muy por encima
  del que solo tenía 1 000. Las probabilidades del profesor enseñan casi tanto como el trabajo de las personas.
- La consecuencia práctica: con un buen profesor puedes entrenar un modelo pequeño con **cualquier texto sin
  etiquetar**, que es barato y abundante.

Esto es, a escala de juguete, lo que hacen las empresas cuando publican versiones «mini» o «flash» de sus modelos,
o lo que hizo DeepSeek al destilar su modelo de razonamiento R1 en modelos Qwen y Llama más pequeños.

**Para experimentar:** cambia `TEMPERATURA` (1, 4, 8) y vuelve a ejecutar los pasos 3 a 5. ¿Mejora o empeora el
estudiante destilado?
"""),
])
print("Cuadernos generados en", OUT)
