"""Convierte las páginas del curso a Markdown simple para importarlas en Google Docs.

Genera PNG/JPEG de todas las imágenes en docs/img/png (Docs no admite SVG ni WebP)
y escribe los .md resultantes en _drive/.
"""
import re
from pathlib import Path
import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PNG = DOCS / "img/png"
OUT = ROOT / "_drive"
WEB = "https://mosqueteroweb.github.io/IAconceptos/"
PAGES = ["01-que-es-la-ia", "02-historia", "03-tipos-de-ia", "04-machine-learning", "05-deep-learning",
         "06-multimodalidad", "07-herramientas", "08-ia-generativa", "09-hardware", "practicas/montaje",
         "10-software", "11-etica"]
TITLES = {"note": "Nota", "info": "Información", "tip": "Consejo", "warning": "Atención", "example": "Actividad",
          "question": "Para reflexionar", "abstract": "En este módulo"}

def to_png(src: Path) -> str:
    PNG.mkdir(parents=True, exist_ok=True)
    if src.suffix == ".svg":
        dst = PNG / (src.stem + ".png")
        cairosvg.svg2png(url=str(src), write_to=str(dst), scale=1.6)
    else:
        dst = PNG / (src.stem + ".jpg")
        Image.open(src).convert("RGB").save(dst, "JPEG", quality=85, optimize=True)
    return WEB + "img/png/" + dst.name

def math(expr: str) -> str:
    e = expr.strip()
    e = re.sub(r"\\text\{([^}]*)\}", r"\1", e)
    e = e.replace(r"\cdot", "·").replace(r"\times", "×").replace(r"\;", " ").replace(r"\,", " ")
    e = re.sub(r"_(\d)", lambda m: "₀₁₂₃₄₅₆₇₈₉"[int(m.group(1))], e)
    return e.replace("\\", "")

def convert(name: str) -> str:
    src = DOCS / f"{name}.md"
    base = src.parent
    s = src.read_text(encoding="utf-8")
    s = re.sub(r"^---\n.*?\n---\n", "", s, flags=re.S)
    # figuras
    def fig(m):
        block = m.group(0)
        img = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", block)
        cap = re.search(r"<figcaption>(.*?)</figcaption>", block, re.S)
        url = to_png((base / img.group(2)).resolve())
        text = re.sub(r"<[^>]+>", "", cap.group(1)) if cap else ""
        return f"![{img.group(1)}]({url})\n" + (f"\n*{text.strip()}*\n" if text else "")
    s = re.sub(r"<figure markdown=\"span\">.*?</figure>", fig, s, flags=re.S)
    # mermaid
    s = re.sub(r"```mermaid\n.*?```", f"*(Diagrama interactivo disponible en la versión web: {WEB}{name}/)*", s, flags=re.S)
    # admoniciones y desplegables
    lines, out, i = s.split("\n"), [], 0
    while i < len(lines):
        m = re.match(r'^(!!!|\?\?\?\+?) (\w+)(?: "([^"]*)")?\s*$', lines[i])
        if m:
            title = m.group(3) or TITLES.get(m.group(2), m.group(2).capitalize())
            body = []; i += 1
            while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
                body.append(lines[i][4:]); i += 1
            while body and not body[-1].strip(): body.pop()
            out.append(f"> **{title}**")
            out.append(">")
            out += [("> " + b) if b.strip() else ">" for b in body]
            out.append("")
            continue
        m = re.match(r'^=== "([^"]+)"\s*$', lines[i])
        if m:
            out.append(f"**{m.group(1)}**"); i += 1
            while i < len(lines) and (lines[i].startswith("    ") or lines[i].strip() == ""):
                out.append(lines[i][4:]); i += 1
            continue
        out.append(lines[i]); i += 1
    s = "\n".join(out)
    s = re.sub(r'</?div[^>]*>', "", s)
    s = re.sub(r"\{ ?[.#]?[^}]*(width|loading|\.diagrama)[^}]*\}", "", s)
    s = re.sub(r":material-youtube:", "▶", s)
    s = re.sub(r":material-[a-z-]+: ?", "", s)
    s = re.sub(r"\\\[(.*?)\\\]", lambda m: f"**{math(m.group(1))}**", s, flags=re.S)
    s = re.sub(r"\\\((.*?)\\\)", lambda m: math(m.group(1)), s)
    s = re.sub(r"(\d)\^(\d+)\^", lambda m: m.group(1) + "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[int(c)] for c in m.group(2)), s)
    # enlaces internos -> web
    def link(m):
        target = m.group(2)
        if target.startswith(("http", "#", "mailto")): return m.group(0)
        path, _, anchor = target.partition("#")
        page = (base / path).resolve().relative_to(DOCS.resolve()).with_suffix("")
        return f"[{m.group(1)}]({WEB}{page.as_posix()}/" + (f"#{anchor}" if anchor else "") + ")"
    s = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s += f"\n\n---\n\n*Versión web de este módulo: {WEB}{name}/*\n"
    return re.sub(r"\n{3,}", "\n\n", s)

OUT.mkdir(exist_ok=True)
for p in PAGES:
    md = convert(p)
    (OUT / (p.replace("/", "-") + ".md")).write_text(md, encoding="utf-8")
    print(p, len(md))
