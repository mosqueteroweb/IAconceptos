# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = [
#   "torch>=2.6",
#   "transformers>=4.50",
#   "matplotlib",
#   "numpy",
#   "sentencepiece",
#   "protobuf",
#   "safetensors",
# ]
#
# # En Windows y Linux, PyTorch con CUDA 12.8 (necesario para las tarjetas RTX 50); en Mac, el normal (usa la GPU del Mac)
# [[tool.uv.index]]
# name = "pytorch-cu128"
# url = "https://download.pytorch.org/whl/cu128"
# explicit = true
#
# [tool.uv.sources]
# torch = [{ index = "pytorch-cu128", marker = "sys_platform == 'win32' or sys_platform == 'linux'" }]
# ///
"""Pre-entrena un nano-modelo de lenguaje con un libro del Proyecto Gutenberg.

Curso «IA de cero a modelo propio» (https://mosqueteroweb.github.io/IAconceptos/) · MosqueteroWeb · CC BY-SA 4.0.
Basado en nanoGPT de Andrej Karpathy.

Primera parte, un Transformer casero que lee carácter a carácter:

    uv run nanomodelo.py caracteres --libro 320
    uv run nanomodelo.py caracteres --libro 320 --capas 2 --comienzo "Pues sepa Vuestra Merced"

Segunda parte, un nano-Llama con un tokenizador profesional que se exporta a GGUF para LM Studio:

    uv run nanomodelo.py llama --libro 320

Cada ejecución crea una carpeta de resultados con la tabla de pérdidas (CSV), la gráfica (PNG), los textos generados
y un resumen. La primera vez tarda más porque descarga PyTorch.
"""
import argparse
import csv
import json
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile
from pathlib import Path


def descargar_libro(libro):
    ruta = "/".join(str(libro)[:-1]) + f"/{libro}/{libro}-0.txt"
    fuentes = [f"https://www.gutenberg.org/cache/epub/{libro}/pg{libro}.txt",
               f"https://gutenberg.pglaf.org/cache/epub/{libro}/pg{libro}.txt",   # copias espejo, por si la principal falla
               f"https://gutenberg.pglaf.org/{ruta}",
               f"https://mirrors.xmission.com/gutenberg/{ruta}"]
    copia = Path(f"libro-{libro}.txt")
    if copia.exists():
        texto = copia.read_text(encoding="utf-8")
    else:
        texto = None
        for url in fuentes:
            try:
                peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                bruto = urllib.request.urlopen(peticion, timeout=60).read().decode("utf-8")
                if "START OF" in bruto:
                    texto = bruto
                    break
            except Exception as error:
                print("No se pudo usar", url, "→", error)
        if texto is None:
            sys.exit("No se ha podido descargar el libro. Comprueba el número y la conexión.")
        copia.write_text(texto, encoding="utf-8")   # la próxima vez no se descarga
    texto = texto.replace("\r\n", "\n")   # algunas copias usan saltos de línea de Windows
    inicio = texto.index("\n", texto.index("START OF")) + 1
    fin = next((texto.index(m) for m in ("*** END OF", "End of the Project Gutenberg", "End of Project Gutenberg")
                if m in texto), len(texto))
    return texto[inicio:fin].strip()


def preparar(args, nombre):
    import torch
    torch.manual_seed(1605)
    if torch.cuda.is_available():
        dispositivo = "cuda"
    elif torch.backends.mps.is_available():
        dispositivo = "mps"
    else:
        dispositivo = "cpu"
    carpeta = Path(f"resultados-{args.libro}-{nombre}")
    carpeta.mkdir(exist_ok=True)
    print(f"Equipo: {platform.system()} {platform.machine()} · entrenando en: {dispositivo}")
    return torch, dispositivo, carpeta


def guardar_perdidas(carpeta, historial, titulo):
    import matplotlib
    matplotlib.use("Agg")   # dibuja en un archivo, sin abrir ventanas
    import matplotlib.pyplot as plt
    with open(carpeta / "perdidas.csv", "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["paso", "perdida_entreno", "perdida_validacion", "segundos"])
        escritor.writerows([(p, f"{e:.4f}", f"{v:.4f}", f"{s:.0f}") for p, e, v, s in historial])
    pasos, entreno, validacion, _ = zip(*historial)
    plt.figure(figsize=(7, 4))
    plt.plot(pasos, entreno, marker="o", label="entrenamiento")
    plt.plot(pasos, validacion, marker="o", label="validación")
    plt.xlabel("pasos de entrenamiento")
    plt.ylabel("pérdida (menos es mejor)")
    plt.title(titulo)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(carpeta / "perdidas.png", dpi=120)


# ---------------------------------------------------------------------------------------------------------------
# Primera parte: un token por carácter y un Transformer escrito a mano
# ---------------------------------------------------------------------------------------------------------------
def caracteres(args):
    texto = descargar_libro(args.libro)
    nombre = f"capas{args.capas}-dim{args.dim}-contexto{args.contexto}-pasos{args.pasos}"
    torch, dispositivo, carpeta = preparar(args, nombre)
    import torch.nn as nn
    from torch.nn import functional as F

    vocabulario = sorted(set(texto))
    a_numero = {c: i for i, c in enumerate(vocabulario)}
    def codificar(cadena):
        return [a_numero[c] for c in cadena if c in a_numero]   # los caracteres que no están en el libro se ignoran
    def decodificar(numeros):
        return "".join(vocabulario[n] for n in numeros)

    datos = torch.tensor(codificar(texto), dtype=torch.long)
    corte = int(0.9 * len(datos))   # 90 % para entrenar, 10 % final para validar
    entreno, validacion = datos[:corte], datos[corte:]
    LOTE, CABEZAS, DROPOUT = 32, 4, 0.2

    def lote(parte):
        fuente = entreno if parte == "entreno" else validacion
        posiciones = torch.randint(len(fuente) - args.contexto, (LOTE,))
        x = torch.stack([fuente[p:p + args.contexto] for p in posiciones])
        y = torch.stack([fuente[p + 1:p + args.contexto + 1] for p in posiciones])   # el texto desplazado un carácter
        return x.to(dispositivo), y.to(dispositivo)

    class Bloque(nn.Module):
        def __init__(self):
            super().__init__()
            self.norma1 = nn.LayerNorm(args.dim)
            self.atencion = nn.MultiheadAttention(args.dim, CABEZAS, dropout=DROPOUT, batch_first=True)
            self.norma2 = nn.LayerNorm(args.dim)
            self.red = nn.Sequential(nn.Linear(args.dim, 4 * args.dim), nn.GELU(),
                                     nn.Linear(4 * args.dim, args.dim), nn.Dropout(DROPOUT))

        def forward(self, x):
            T = x.shape[1]
            mascara = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1)   # no mirar el futuro
            h = self.norma1(x)
            x = x + self.atencion(h, h, h, attn_mask=mascara, need_weights=False)[0]
            return x + self.red(self.norma2(x))

    class NanoModelo(nn.Module):
        def __init__(self):
            super().__init__()
            self.tokens = nn.Embedding(len(vocabulario), args.dim)
            self.posiciones = nn.Embedding(args.contexto, args.dim)
            self.bloques = nn.Sequential(*[Bloque() for _ in range(args.capas)])
            self.norma = nn.LayerNorm(args.dim)
            self.salida = nn.Linear(args.dim, len(vocabulario))

        def forward(self, idx, objetivos=None):
            x = self.tokens(idx) + self.posiciones(torch.arange(idx.shape[1], device=idx.device))
            logits = self.salida(self.norma(self.bloques(x)))
            perdida = None if objetivos is None else F.cross_entropy(logits.view(-1, logits.size(-1)), objetivos.view(-1))
            return logits, perdida

        @torch.no_grad()
        def generar(self, comienzo, nuevos, temperatura):
            idx = torch.tensor([codificar(comienzo)], dtype=torch.long, device=dispositivo)
            for _ in range(nuevos):
                logits, _ = self(idx[:, -args.contexto:])
                probabilidades = F.softmax(logits[:, -1, :] / temperatura, dim=-1)
                idx = torch.cat([idx, torch.multinomial(probabilidades, num_samples=1)], dim=1)
            return decodificar(idx[0].tolist())

    modelo = NanoModelo().to(dispositivo)
    parametros = sum(p.numel() for p in modelo.parameters())
    print(f"Libro {args.libro}: {len(texto):,} caracteres · vocabulario de {len(vocabulario)} caracteres")
    print(f"Parámetros del modelo: {parametros / 1e6:.2f} millones")

    modelo.eval()
    antes = modelo.generar(args.comienzo, 200, 0.8)
    modelo.train()

    @torch.no_grad()
    def evaluar():
        modelo.eval()
        resultado = [torch.stack([modelo(*lote(parte))[1] for _ in range(50)]).mean().item()
                     for parte in ("entreno", "validacion")]
        modelo.train()
        return resultado

    optimizador = torch.optim.AdamW(modelo.parameters(), lr=3e-4)
    historial, comienzo = [], time.time()
    for paso in range(args.pasos + 1):
        if paso % 500 == 0 or paso == args.pasos:
            p_ent, p_val = evaluar()
            historial.append((paso, p_ent, p_val, time.time() - comienzo))
            print(f"Paso {paso:5d} · pérdida entreno {p_ent:.3f} · validación {p_val:.3f} · {time.time() - comienzo:4.0f} s")
        if paso == args.pasos:
            break
        x, y = lote("entreno")
        _, perdida = modelo(x, y)
        optimizador.zero_grad(set_to_none=True)
        perdida.backward()
        optimizador.step()
    duracion = time.time() - comienzo

    modelo.eval()
    textos = [f"ANTES DE ENTRENAR (temperatura 0,8):\n{antes}\n"]
    for temperatura in (0.3, 0.8, 1.3):
        textos.append(f"TEMPERATURA {temperatura}:\n{modelo.generar(args.comienzo, args.caracteres, temperatura)}\n")
    (carpeta / "textos.txt").write_text("\n".join(textos), encoding="utf-8")
    guardar_perdidas(carpeta, historial, f"Libro {args.libro} · {nombre}")
    resumen = (f"Libro: {args.libro}\nCaracteres: {len(texto)}\nVocabulario: {len(vocabulario)}\n"
               f"Capas: {args.capas} · DIM: {args.dim} · Contexto: {args.contexto} · Pasos: {args.pasos}\n"
               f"Parámetros: {parametros}\nTiempo de entrenamiento: {duracion:.0f} s\n"
               f"Pérdida final: entreno {historial[-1][1]:.3f} · validación {historial[-1][2]:.3f}\n"
               f"Equipo: {platform.system()} {platform.machine()} · {dispositivo}\n")
    (carpeta / "resumen.txt").write_text(resumen, encoding="utf-8")
    print("\n" + "\n".join(textos))
    print(resumen)
    print(f"Resultados en la carpeta {carpeta.resolve()}")


# ---------------------------------------------------------------------------------------------------------------
# Segunda parte: arquitectura Llama + tokenizador de SmolLM2, exportable a GGUF
# ---------------------------------------------------------------------------------------------------------------
def llama(args):
    texto = descargar_libro(args.libro)
    torch, dispositivo, carpeta = preparar(args, "llama")
    from transformers import AutoTokenizer, LlamaConfig, LlamaForCausalLM

    tokenizador = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M")
    ids = torch.tensor(tokenizador(texto)["input_ids"])
    print(f"El libro ocupa {len(texto):,} caracteres y {len(ids):,} tokens "
          f"({len(texto) / len(ids):.1f} caracteres por token)")
    print("Así trocea una frase:", tokenizador.tokenize(args.comienzo))
    corte = int(0.9 * len(ids))
    entreno, validacion = ids[:corte], ids[corte:]
    LOTE, CONTEXTO, DIM, CAPAS, CABEZAS = 32, 128, 256, 4, 4

    def lote(parte):
        fuente = entreno if parte == "entreno" else validacion
        posiciones = torch.randint(len(fuente) - CONTEXTO, (LOTE,))
        return torch.stack([fuente[p:p + CONTEXTO] for p in posiciones]).to(dispositivo)

    configuracion = LlamaConfig(vocab_size=len(tokenizador), hidden_size=DIM, intermediate_size=704,
                                num_hidden_layers=CAPAS, num_attention_heads=CABEZAS, num_key_value_heads=CABEZAS,
                                max_position_embeddings=256, tie_word_embeddings=True,
                                bos_token_id=tokenizador.bos_token_id, eos_token_id=tokenizador.eos_token_id)
    modelo = LlamaForCausalLM(configuracion).to(dispositivo)
    parametros = sum(p.numel() for p in modelo.parameters())
    embeddings = modelo.get_input_embeddings().weight.numel()
    print(f"Parámetros: {parametros / 1e6:.1f} millones, de los que {embeddings / 1e6:.1f} son la tabla de embeddings")

    optimizador = torch.optim.AdamW(modelo.parameters(), lr=1e-3)
    historial, comienzo = [], time.time()
    for paso in range(args.pasos + 1):
        if paso % 250 == 0 or paso == args.pasos:
            modelo.eval()
            with torch.no_grad():
                p_ent = torch.stack([modelo(input_ids=(x := lote("entreno")), labels=x).loss for _ in range(20)]).mean().item()
                p_val = torch.stack([modelo(input_ids=(x := lote("validacion")), labels=x).loss for _ in range(20)]).mean().item()
            modelo.train()
            historial.append((paso, p_ent, p_val, time.time() - comienzo))
            print(f"Paso {paso:5d} · pérdida entreno {p_ent:.3f} · validación {p_val:.3f} · {time.time() - comienzo:4.0f} s")
        if paso == args.pasos:
            break
        x = lote("entreno")
        perdida = modelo(input_ids=x, labels=x).loss
        optimizador.zero_grad(set_to_none=True)
        perdida.backward()
        optimizador.step()
    duracion = time.time() - comienzo
    guardar_perdidas(carpeta, historial, f"Libro {args.libro} · nano-Llama")

    modelo.eval()
    inicio = tokenizador(args.comienzo, return_tensors="pt").input_ids.to(dispositivo)
    salida = modelo.generate(inicio, max_new_tokens=80, do_sample=True, temperature=0.8, top_k=50,
                             pad_token_id=tokenizador.eos_token_id)
    muestra = tokenizador.decode(salida[0])
    (carpeta / "textos.txt").write_text(f"TEMPERATURA 0.8:\n{muestra}\n", encoding="utf-8")

    # Guardar en formato Hugging Face, con una plantilla de chat mínima: LM Studio le pasará el texto tal cual
    tokenizador.chat_template = "{% for message in messages %}{{ message['content'] }}{% endfor %}"
    modelo.save_pretrained(carpeta / "nano-hf")
    tokenizador.save_pretrained(carpeta / "nano-hf")

    # Convertir a GGUF con el script de llama.cpp (se descarga su código fuente una sola vez)
    fuente = Path("llama.cpp-master")
    if not fuente.exists():
        print("Descargando el código de llama.cpp para convertir a GGUF…")
        urllib.request.urlretrieve("https://github.com/ggml-org/llama.cpp/archive/refs/heads/master.zip", "llama-src.zip")
        with zipfile.ZipFile("llama-src.zip") as z:
            z.extractall(".")
    archivo = carpeta / f"nano-libro-{args.libro}.gguf"
    r = subprocess.run([sys.executable, str(fuente / "convert_hf_to_gguf.py"), str(carpeta / "nano-hf"),
                        "--outfile", str(archivo), "--outtype", "f16"], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        sys.exit("La conversión a GGUF ha fallado.")
    shutil.rmtree(carpeta / "nano-hf", ignore_errors=True)
    tamano = archivo.stat().st_size / 1e6

    resumen = (f"Libro: {args.libro}\nCaracteres: {len(texto)}\nTokens (SmolLM2): {len(ids)}\n"
               f"Parámetros: {parametros} (embeddings: {embeddings})\nPasos: {args.pasos}\n"
               f"Tiempo de entrenamiento: {duracion:.0f} s\n"
               f"Pérdida final: entreno {historial[-1][1]:.3f} · validación {historial[-1][2]:.3f}\n"
               f"Archivo GGUF: {archivo.name} ({tamano:.0f} MB)\n"
               f"Equipo: {platform.system()} {platform.machine()} · {dispositivo}\n")
    (carpeta / "resumen.txt").write_text(resumen, encoding="utf-8")
    print("\n" + muestra + "\n")
    print(resumen)
    print(f"Para abrirlo en LM Studio:  lms import -c \"{archivo.resolve()}\"")


def main():
    parser = argparse.ArgumentParser(description="Pre-entrena un nano-modelo con un libro de Gutenberg")
    sub = parser.add_subparsers(dest="parte", required=True)

    p1 = sub.add_parser("caracteres", help="primera parte: Transformer casero, un token por carácter")
    p1.add_argument("--libro", type=int, default=2000, help="número del libro en Gutenberg (2000 = Quijote)")
    p1.add_argument("--capas", type=int, default=4, help="bloques Transformer (4 por defecto)")
    p1.add_argument("--dim", type=int, default=256, help="tamaño de los vectores (256 por defecto)")
    p1.add_argument("--contexto", type=int, default=128, help="caracteres que mira hacia atrás (128 por defecto)")
    p1.add_argument("--pasos", type=int, default=5000, help="pasos de entrenamiento (5000 por defecto)")
    p1.add_argument("--comienzo", default="DON QUIJOTE", help="principio del texto que generará al final")
    p1.add_argument("--caracteres", type=int, default=300, help="caracteres que generará")
    p1.set_defaults(funcion=caracteres)

    p2 = sub.add_parser("llama", help="segunda parte: nano-Llama exportable a GGUF para LM Studio")
    p2.add_argument("--libro", type=int, default=2000)
    p2.add_argument("--pasos", type=int, default=2000)
    p2.add_argument("--comienzo", default="En un lugar de la Mancha")
    p2.set_defaults(funcion=llama)

    args = parser.parse_args()
    args.funcion(args)


if __name__ == "__main__":
    main()
