# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Genera datos de destilación con un modelo «profesor» servido por LM Studio.

Curso «IA de cero a modelo propio» (https://mosqueteroweb.github.io/IAconceptos/) · MosqueteroWeb · CC BY-SA 4.0.

Dos pasos, cada uno con una sola orden (con LM Studio abierto y su servidor en marcha):

  1. Que el profesor invente preguntas sobre un tema:
     uv run destilar_profesor.py preguntas --modelo qwen/qwen3-8b --tema "la Edad Media" --n 150

  2. Que el profesor responda a cada pregunta y se guarden en formato Alpaca (JSONL) para Unsloth Studio:
     uv run destilar_profesor.py respuestas --modelo qwen/qwen3-8b

Revisa y corrige preguntas.txt entre los dos pasos. Si el paso 2 se interrumpe, al repetirlo continúa donde lo dejó.
"""
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ESTILO = ("Eres un profesor experto y paciente. Responde en español, de forma clara y correcta, "
          "en un párrafo de 3 a 6 frases. No uses listas ni encabezados.")


def pedir(url, modelo, mensajes, temperatura, max_tokens):
    cuerpo = json.dumps({"model": modelo, "messages": mensajes, "temperature": temperatura,
                         "max_tokens": max_tokens}).encode("utf-8")
    peticion = urllib.request.Request(f"{url}/chat/completions", data=cuerpo,
                                      headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(peticion, timeout=600) as respuesta:
        datos = json.load(respuesta)
    texto = datos["choices"][0]["message"]["content"] or ""
    texto = re.sub(r"<think>.*?</think>", "", texto, flags=re.S).strip()  # quita el razonamiento si viene dentro
    return texto, datos.get("usage", {})


def comprobar_servidor(url, modelo):
    try:
        with urllib.request.urlopen(f"{url}/models", timeout=10) as r:
            modelos = [m["id"] for m in json.load(r)["data"]]
    except Exception as error:
        sys.exit(f"No se puede conectar con LM Studio en {url}. ¿Está el servidor en marcha (Model Server → Status)?\n{error}")
    if modelo not in modelos:
        sys.exit(f"El modelo «{modelo}» no está en LM Studio. Modelos disponibles:\n  " + "\n  ".join(modelos))


def preguntas(args):
    comprobar_servidor(args.url, args.modelo)
    salida = Path(args.salida)
    lista = [l.strip() for l in salida.read_text(encoding="utf-8").splitlines() if l.strip()] if salida.exists() else []
    vistas = {l.lower() for l in lista}
    intentos = 0
    while len(lista) < args.n and intentos < args.n:
        intentos += 1
        orden = (f"Escribe 15 preguntas distintas y variadas sobre {args.tema}, adecuadas para {args.publico}. "
                 "Mezcla preguntas de definición, de causa, de comparación y de ejemplos. "
                 "Escribe solo las preguntas, una por línea, sin numerar." )
        if lista:
            orden += " No repitas ninguna de estas: " + " | ".join(lista[-30:])
        texto, _ = pedir(args.url, args.modelo, [{"role": "user", "content": orden}], 0.9, 1500)
        for linea in texto.splitlines():
            linea = re.sub(r"^[\s\-\*\d\.\)]+", "", linea).strip()
            if linea.endswith("?") and len(linea) > 12 and linea.lower() not in vistas:
                lista.append(linea)
                vistas.add(linea.lower())
        print(f"{len(lista)} preguntas…")
    salida.write_text("\n".join(lista[:args.n]) + "\n", encoding="utf-8")
    print(f"Listo: {min(len(lista), args.n)} preguntas en {salida}. Revísalas antes del paso 2.")


def respuestas(args):
    comprobar_servidor(args.url, args.modelo)
    lista = [l.strip() for l in Path(args.preguntas).read_text(encoding="utf-8").splitlines() if l.strip()]
    salida = Path(args.salida)
    hechas = set()
    if salida.exists():
        for linea in salida.read_text(encoding="utf-8").splitlines():
            if linea.strip():
                hechas.add(json.loads(linea)["instruction"])
    pendientes = [p for p in lista if p not in hechas]
    print(f"{len(lista)} preguntas · {len(hechas)} ya respondidas · {len(pendientes)} pendientes")
    tokens, inicio = 0, time.time()
    with salida.open("a", encoding="utf-8") as f:
        for i, pregunta in enumerate(pendientes, 1):
            contenido = pregunta + (" /no_think" if args.sin_razonar else "")
            texto, uso = pedir(args.url, args.modelo, [{"role": "system", "content": args.estilo},
                                                        {"role": "user", "content": contenido}],
                               args.temperatura, args.max_tokens)
            tokens += uso.get("completion_tokens", 0)
            f.write(json.dumps({"instruction": pregunta, "input": "", "output": texto}, ensure_ascii=False) + "\n")
            f.flush()
            ritmo = tokens / max(time.time() - inicio, 1e-6)
            print(f"[{i}/{len(pendientes)}] {pregunta[:60]}… ({ritmo:.0f} tok/s de media)")
    print(f"Listo: datos del profesor en {salida}.")


def main():
    parser = argparse.ArgumentParser(description="Datos de destilación con un profesor en LM Studio")
    parser.add_argument("--url", default="http://localhost:1234/v1", help="dirección del servidor de LM Studio")
    sub = parser.add_subparsers(dest="paso", required=True)

    p1 = sub.add_parser("preguntas", help="el profesor inventa preguntas sobre un tema")
    p1.add_argument("--modelo", required=True, help="identificador del modelo profesor en LM Studio")
    p1.add_argument("--tema", required=True)
    p1.add_argument("--publico", default="alumnado de secundaria")
    p1.add_argument("--n", type=int, default=150)
    p1.add_argument("--salida", default="preguntas.txt")
    p1.set_defaults(funcion=preguntas)

    p2 = sub.add_parser("respuestas", help="el profesor responde a cada pregunta (formato Alpaca)")
    p2.add_argument("--modelo", required=True, help="identificador del modelo profesor en LM Studio")
    p2.add_argument("--preguntas", default="preguntas.txt")
    p2.add_argument("--salida", default="datos_profesor.jsonl")
    p2.add_argument("--estilo", default=ESTILO, help="instrucciones de sistema para el profesor")
    p2.add_argument("--temperatura", type=float, default=0.3)
    p2.add_argument("--max-tokens", type=int, default=500)
    p2.add_argument("--sin-razonar", action=argparse.BooleanOptionalAction, default=True,
                    help="añade /no_think (útil con Qwen3) para respuestas más rápidas")
    p2.set_defaults(funcion=respuestas)

    args = parser.parse_args()
    args.funcion(args)


if __name__ == "__main__":
    main()
