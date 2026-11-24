"""Genera la chuleta con casillas y las presentaciones de repaso del profesor.

Lee tools/repaso_datos.py y escribe en docs/profesor/:
- index.html: portada con los enlaces;
- chuleta.html: los 22 módulos con sus puntos clave y una casilla en cada uno;
- presentacion-parte-1.html y presentacion-parte-2.html: una diapositiva por módulo.

Uso: python3 tools/repaso.py
"""
import html
import json
from pathlib import Path

from repaso_datos import MODULOS

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "profesor"
WEB = "https://mosqueteroweb.github.io/IAconceptos/"
PARTES = {1: "Primera parte: entender la IA", 2: "Segunda parte: usar y crear modelos"}

e = html.escape

ESTILO_BASE = """
:root {
  --fondo: #f7f7f5; --papel: #ffffff; --texto: #1c1d21; --suave: #5f6370; --linea: #e3e3df;
  --p1: #2f6fdf; --p1-claro: #e8f0fd; --p2: #7a4fd6; --p2-claro: #f0eafc; --ok: #1f9d55; --ok-claro: #e5f6ec;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --fondo: #15161a; --papel: #1e2026; --texto: #ececef; --suave: #a3a7b3; --linea: #30333b;
    --p1: #7aa7ff; --p1-claro: #1c2a45; --p2: #b494ff; --p2-claro: #2a2142; --ok: #4cc785; --ok-claro: #17301f;
    color-scheme: dark;
  }
}
* { box-sizing: border-box; }
html, body { margin: 0; }
body { background: var(--fondo); color: var(--texto);
  font: 16px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; -webkit-text-size-adjust: 100%; }
a { color: inherit; }
"""


def color(parte):
    return ("var(--p1)", "var(--p1-claro)") if parte == 1 else ("var(--p2)", "var(--p2-claro)")


# ---------------------------------------------------------------------------- Portada
def portada():
    tarjetas = []
    for parte in (1, 2):
        ms = [m for m in MODULOS if m["parte"] == parte]
        tarjetas.append(f"""
      <a class="tarjeta" href="presentacion-parte-{parte}.html" style="--c:{color(parte)[0]};--cc:{color(parte)[1]}">
        <span class="etq">Presentación</span>
        <strong>{e(PARTES[parte])}</strong>
        <span>Módulos {ms[0]['n']} a {ms[-1]['n']} · una diapositiva por módulo</span>
      </a>""")
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Repaso del profesor</title>
<meta name="robots" content="noindex">
<style>{ESTILO_BASE}
main {{ max-width: 760px; margin: 0 auto; padding: 32px 16px 48px; }}
h1 {{ font-size: 1.6rem; margin: 0 0 4px; }}
p.sub {{ color: var(--suave); margin: 0 0 24px; }}
.tarjeta {{ display: block; text-decoration: none; background: var(--papel); border: 1px solid var(--linea);
  border-left: 6px solid var(--c); border-radius: 14px; padding: 16px 18px; margin-bottom: 12px; }}
.tarjeta:hover {{ background: var(--cc); }}
.tarjeta strong {{ display: block; font-size: 1.15rem; margin: 2px 0; }}
.tarjeta span {{ color: var(--suave); font-size: .92rem; }}
.tarjeta .etq {{ color: var(--c); font-weight: 600; font-size: .8rem; text-transform: uppercase; letter-spacing: .04em; }}
footer {{ color: var(--suave); font-size: .85rem; margin-top: 24px; }}
</style>
</head>
<body>
<main>
  <h1>Repaso del profesor</h1>
  <p class="sub">Los puntos clave de cada módulo del curso «IA de cero a modelo propio», para comprobar que no se queda nada importante sin explicar.</p>
  <a class="tarjeta" href="chuleta.html" style="--c:var(--ok);--cc:var(--ok-claro)">
    <span class="etq">Chuleta con casillas</span>
    <strong>Los 22 módulos, punto a punto</strong>
    <span>Marca cada punto al explicarlo. Las marcas se guardan en este navegador; bórralas al cambiar de grupo.</span>
  </a>
  {''.join(tarjetas)}
  <footer>Volver al <a href="../">curso</a>.</footer>
</main>
</body>
</html>
"""


# ---------------------------------------------------------------------------- Chuleta
def chuleta():
    chips, bloques = [], []
    for parte in (1, 2):
        ms = [m for m in MODULOS if m["parte"] == parte]
        chips.append(f'<div class="fila"><span class="parte" style="color:{color(parte)[0]}">Parte {parte}</span>'
                     + "".join(f'<a class="chip" href="#m{m["n"]}" data-m="{m["n"]}" style="--c:{color(parte)[0]}">'
                               f'{m["n"]}<small></small></a>' for m in ms) + "</div>")
        bloques.append(f'<h2 class="titulo-parte" style="color:{color(parte)[0]}">{e(PARTES[parte])}</h2>')
        for m in ms:
            puntos = "".join(
                f'<li><label><input type="checkbox" data-id="m{m["n"]}p{i}">'
                f'<span class="ico" aria-hidden="true">{ico}</span>'
                f'<span class="txt"><b>{e(t)}</b><span class="det">{e(d)}</span></span></label></li>'
                for i, (ico, t, d) in enumerate(m["puntos"]))
            practica = (f' · <a href="{WEB}practicas/practica-{m["practica"]}/">práctica evaluable {m["practica"]}</a>'
                        if m.get("practica") else "")
            actividad = f'<p class="act"><span aria-hidden="true">🧪</span> <b>Actividad:</b> {e(m["actividad"])}</p>' if m.get("actividad") else ""
            bloques.append(f"""
<section class="modulo" id="m{m['n']}" style="--c:{color(parte)[0]};--cc:{color(parte)[1]}">
  <header>
    <span class="num">{m['n']}</span>
    <div>
      <h3>{e(m['titulo'])}</h3>
      <p class="idea">{e(m['idea'])}</p>
    </div>
  </header>
  <ul>{puntos}</ul>
  {actividad}
  <div class="pie">
    <span class="prog" data-prog="m{m['n']}"></span>
    <a href="{WEB}{m['pagina']}/">módulo en la web</a>{practica} ·
    <a href="presentacion-parte-{parte}.html#m{m['n']}">diapositiva</a>
    <button type="button" class="borrar" data-borrar="m{m['n']}">Borrar marcas</button>
  </div>
</section>""")
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chuleta de repaso</title>
<meta name="robots" content="noindex">
<style>{ESTILO_BASE}
.barra {{ position: sticky; top: 0; z-index: 5; background: var(--fondo); border-bottom: 1px solid var(--linea);
  padding: 8px 16px; }}
.barra .cab {{ display: flex; align-items: center; gap: 12px; max-width: 860px; margin: 0 auto 6px; }}
.barra .cab a {{ font-weight: 700; text-decoration: none; }}
.barra .cab span {{ color: var(--suave); font-size: .85rem; margin-left: auto; }}
.fila {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; max-width: 860px; margin: 0 auto 4px; }}
.parte {{ font-size: .75rem; font-weight: 700; width: 52px; }}
.chip {{ min-width: 36px; height: 32px; padding: 0 6px; border-radius: 9px; border: 1px solid var(--linea);
  background: var(--papel); text-decoration: none; display: inline-flex; align-items: center; justify-content: center;
  gap: 3px; font-weight: 600; font-size: .9rem; }}
.chip small {{ font-weight: 500; color: var(--suave); font-size: .7rem; }}
.chip.algo {{ border-color: var(--c); }}
.chip.hecho {{ background: var(--ok); border-color: var(--ok); color: #fff; }}
.chip.hecho small {{ color: #fff; }}
main {{ max-width: 860px; margin: 0 auto; padding: 8px 16px 64px; }}
.titulo-parte {{ font-size: 1.05rem; margin: 28px 0 10px; text-transform: uppercase; letter-spacing: .03em; }}
.modulo {{ background: var(--papel); border: 1px solid var(--linea); border-top: 5px solid var(--c);
  border-radius: 14px; padding: 14px 16px 10px; margin-bottom: 18px; scroll-margin-top: 110px; }}
.modulo header {{ display: flex; gap: 12px; align-items: flex-start; }}
.num {{ flex: none; width: 40px; height: 40px; border-radius: 10px; background: var(--cc); color: var(--c);
  font-weight: 800; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; }}
h3 {{ margin: 0; font-size: 1.12rem; line-height: 1.25; }}
.idea {{ margin: 4px 0 0; color: var(--suave); font-style: italic; }}
ul {{ list-style: none; padding: 0; margin: 12px 0 4px; }}
li label {{ display: flex; gap: 10px; align-items: flex-start; padding: 8px 6px; border-radius: 10px; cursor: pointer; }}
li label:hover {{ background: var(--fondo); }}
li input {{ width: 22px; height: 22px; margin: 2px 0 0; flex: none; accent-color: var(--ok); cursor: pointer; }}
.ico {{ flex: none; width: 26px; text-align: center; font-size: 1.15rem; }}
.txt b {{ display: block; font-weight: 600; }}
.det {{ display: block; color: var(--suave); font-size: .88rem; }}
li input:checked ~ .txt b {{ text-decoration: line-through; text-decoration-color: var(--ok); text-decoration-thickness: 2px; }}
li input:checked ~ .txt, li input:checked ~ .ico {{ opacity: .55; }}
.act {{ margin: 6px 0 8px; padding: 8px 10px; background: var(--cc); border-radius: 10px; font-size: .9rem; }}
.pie {{ display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: .85rem; color: var(--suave);
  border-top: 1px solid var(--linea); padding-top: 8px; margin-top: 6px; }}
.pie .prog {{ font-weight: 700; color: var(--c); margin-right: 4px; }}
.pie .prog.hecho {{ color: var(--ok); }}
.borrar {{ margin-left: auto; font: inherit; color: var(--suave); background: none; border: 1px solid var(--linea);
  border-radius: 8px; padding: 4px 10px; cursor: pointer; }}
.borrar:hover {{ color: var(--texto); border-color: var(--suave); }}
@media (max-width: 620px) {{
  .det {{ font-size: .84rem; }} .modulo {{ padding: 12px 12px 8px; scroll-margin-top: 104px; }}
  .barra {{ padding: 6px 10px; }}
  .barra .cab {{ margin-bottom: 4px; }} .barra .cab span {{ display: none; }}
  .fila {{ flex-wrap: nowrap; overflow-x: auto; scrollbar-width: none; margin-bottom: 3px; }}
  .fila::-webkit-scrollbar {{ display: none; }}
  .parte {{ width: auto; flex: none; margin-right: 2px; }}
  .chip {{ flex: none; min-width: 32px; height: 28px; font-size: .85rem; }}
}}
</style>
</head>
<body>
<div class="barra">
  <div class="cab"><a href="index.html">Repaso del profesor</a><span>Marca cada punto al explicarlo</span></div>
  {''.join(chips)}
</div>
<main>
{''.join(bloques)}
</main>
<script>
(function () {{
  var CLAVE = "iaconceptos-chuleta";
  var marcas = {{}};
  try {{ marcas = JSON.parse(localStorage.getItem(CLAVE)) || {{}}; }} catch (err) {{ marcas = {{}}; }}
  function guardar() {{ try {{ localStorage.setItem(CLAVE, JSON.stringify(marcas)); }} catch (err) {{}} }}
  var casillas = document.querySelectorAll("input[data-id]");
  function pintar() {{
    var cuenta = {{}};
    casillas.forEach(function (c) {{
      var m = c.dataset.id.split("p")[0];
      cuenta[m] = cuenta[m] || [0, 0];
      cuenta[m][1]++;
      if (c.checked) cuenta[m][0]++;
    }});
    Object.keys(cuenta).forEach(function (m) {{
      var hechos = cuenta[m][0], total = cuenta[m][1];
      var prog = document.querySelector('[data-prog="' + m + '"]');
      prog.textContent = hechos + " de " + total;
      prog.classList.toggle("hecho", hechos === total);
      var chip = document.querySelector('.chip[data-m="' + m.slice(1) + '"]');
      chip.querySelector("small").textContent = hechos ? hechos + "/" + total : "";
      chip.classList.toggle("algo", hechos > 0 && hechos < total);
      chip.classList.toggle("hecho", hechos === total);
    }});
  }}
  casillas.forEach(function (c) {{
    c.checked = !!marcas[c.dataset.id];
    c.addEventListener("change", function () {{
      if (c.checked) marcas[c.dataset.id] = 1; else delete marcas[c.dataset.id];
      guardar(); pintar();
    }});
  }});
  document.querySelectorAll("[data-borrar]").forEach(function (b) {{
    b.addEventListener("click", function () {{
      var m = b.dataset.borrar;
      if (!confirm("¿Borrar las marcas del módulo " + m.slice(1) + "?")) return;
      casillas.forEach(function (c) {{
        if (c.dataset.id.split("p")[0] === m) {{ c.checked = false; delete marcas[c.dataset.id]; }}
      }});
      guardar(); pintar();
    }});
  }});
  pintar();
}})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------- Presentaciones
def presentacion(parte):
    c, cc = color(parte)
    ms = [m for m in MODULOS if m["parte"] == parte]
    diapos = [f"""
<section class="diapo portada" id="inicio">
  <div class="lienzo">
    <p class="etq">IA de cero a modelo propio · repaso del profesor</p>
    <h1>{e(PARTES[parte])}</h1>
    <ol class="indice">{''.join(f'<li><a href="#m{m["n"]}"><b>{m["n"]}</b> {e(m["titulo"])}</a></li>' for m in ms)}</ol>
  </div>
</section>"""]
    for m in ms:
        n = len(m["puntos"])
        cols = "dos" if n > 4 else "una"
        puntos = "".join(f'<li><span class="ico" aria-hidden="true">{ico}</span><span>{e(t)}</span></li>'
                         for ico, t, _ in m["puntos"])
        actividad = f'<p class="act"><span aria-hidden="true">🧪</span> {e(m["actividad"])}</p>' if m.get("actividad") else ""
        practica = f'<span class="pract">Práctica evaluable {m["practica"]}</span>' if m.get("practica") else ""
        diapos.append(f"""
<section class="diapo" id="m{m['n']}">
  <div class="lienzo">
    <header><span class="num">{m['n']}</span><h2>{e(m['titulo'])}</h2>{practica}</header>
    <p class="idea">{e(m['idea'])}</p>
    <ul class="{cols}">{puntos}</ul>
    {actividad}
  </div>
</section>""")
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Repaso: parte {parte}</title>
<meta name="robots" content="noindex">
<style>{ESTILO_BASE}
:root {{ --c: {c}; --cc: {cc}; }}
html, body {{ height: 100%; overflow: hidden; }}
.pase {{ height: 100%; display: flex; align-items: center; justify-content: center; padding: 12px; }}
.diapo {{ display: none; width: min(100%, calc((100vh - 70px) * 16 / 9)); aspect-ratio: 16 / 9;
  background: var(--papel); border: 1px solid var(--linea); border-radius: 18px; container-type: inline-size;
  box-shadow: 0 6px 30px rgba(0,0,0,.08); overflow: hidden; }}
.diapo.activa {{ display: block; }}
.lienzo {{ height: 100%; padding: 4.5cqw 5cqw; display: flex; flex-direction: column; border-top: 1.1cqw solid var(--c); }}
.etq {{ color: var(--c); font-weight: 700; font-size: 1.5cqw; text-transform: uppercase; letter-spacing: .08em; margin: 0; }}
h1 {{ font-size: 4.4cqw; margin: 1cqw 0 2.5cqw; line-height: 1.1; }}
.indice {{ columns: 2; column-gap: 4cqw; margin: 0; padding: 0; list-style: none; font-size: 1.9cqw; }}
.indice li {{ break-inside: avoid; margin-bottom: 1cqw; }}
.indice a {{ text-decoration: none; }}
.indice b {{ display: inline-block; min-width: 3.2cqw; color: var(--c); }}
header {{ display: flex; align-items: center; gap: 1.8cqw; }}
.num {{ flex: none; width: 6cqw; height: 6cqw; border-radius: 1.4cqw; background: var(--c); color: #fff;
  font-weight: 800; font-size: 3.2cqw; display: flex; align-items: center; justify-content: center; }}
h2 {{ font-size: 3.2cqw; margin: 0; line-height: 1.1; }}
.pract {{ margin-left: auto; flex: none; font-size: 1.4cqw; font-weight: 600; color: var(--c); background: var(--cc);
  padding: .6cqw 1.2cqw; border-radius: 99px; }}
.idea {{ font-size: 2.05cqw; color: var(--suave); font-style: italic; margin: 1.6cqw 0 2.2cqw; padding-left: 1.4cqw;
  border-left: .5cqw solid var(--c); }}
ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 1.3cqw 3cqw; align-content: start; flex: 1; }}
ul.dos {{ grid-template-columns: 1fr 1fr; }}
ul li {{ display: flex; align-items: center; gap: 1.4cqw; font-size: 2.05cqw; font-weight: 600; line-height: 1.2;
  background: var(--cc); border-radius: 1.2cqw; padding: 1.1cqw 1.4cqw; }}
ul.una li {{ font-size: 2.4cqw; }}
ul .ico {{ font-size: 2.6cqw; flex: none; }}
.act {{ margin: 1.6cqw 0 0; font-size: 1.6cqw; color: var(--suave); }}
.mando {{ position: fixed; bottom: 10px; left: 0; right: 0; display: flex; justify-content: center; align-items: center;
  gap: 10px; font-size: .9rem; color: var(--suave); }}
.mando button, .mando a {{ font: inherit; background: var(--papel); color: var(--texto); border: 1px solid var(--linea);
  border-radius: 9px; padding: 5px 12px; cursor: pointer; text-decoration: none; }}
@media print {{
  html, body {{ height: auto; overflow: visible; }}
  .pase {{ display: block; padding: 0; }}
  .diapo {{ display: block; width: 100%; page-break-after: always; box-shadow: none; margin: 0 0 8px; }}
  .mando {{ display: none; }}
}}
</style>
</head>
<body>
<div class="pase">
{''.join(diapos)}
</div>
<nav class="mando">
  <button type="button" id="ant" aria-label="Anterior">←</button>
  <span id="cuenta"></span>
  <button type="button" id="sig" aria-label="Siguiente">→</button>
  <a href="chuleta.html" id="achuleta">Chuleta</a>
  <a href="index.html">Inicio</a>
</nav>
<script>
(function () {{
  var d = Array.prototype.slice.call(document.querySelectorAll(".diapo"));
  var i = 0;
  function ir(k, sinHash) {{
    i = Math.max(0, Math.min(d.length - 1, k));
    d.forEach(function (x, j) {{ x.classList.toggle("activa", j === i); }});
    document.getElementById("cuenta").textContent = (i + 1) + " / " + d.length;
    document.getElementById("achuleta").href = "chuleta.html" + (d[i].id.charAt(0) === "m" ? "#" + d[i].id : "");
    if (!sinHash) history.replaceState(null, "", "#" + d[i].id);
  }}
  function desdeHash() {{
    var h = location.hash.slice(1);
    var k = d.findIndex(function (x) {{ return x.id === h; }});
    ir(k < 0 ? 0 : k, true);
  }}
  document.getElementById("ant").onclick = function () {{ ir(i - 1); }};
  document.getElementById("sig").onclick = function () {{ ir(i + 1); }};
  document.addEventListener("keydown", function (ev) {{
    if (["ArrowRight", "PageDown", " "].indexOf(ev.key) >= 0) {{ ev.preventDefault(); ir(i + 1); }}
    if (["ArrowLeft", "PageUp"].indexOf(ev.key) >= 0) {{ ev.preventDefault(); ir(i - 1); }}
    if (ev.key === "Home") ir(0);
    if (ev.key === "End") ir(d.length - 1);
  }});
  var x0 = null;
  document.addEventListener("touchstart", function (ev) {{ x0 = ev.touches[0].clientX; }}, {{ passive: true }});
  document.addEventListener("touchend", function (ev) {{
    if (x0 === null) return;
    var dx = ev.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) ir(i + (dx < 0 ? 1 : -1));
    x0 = null;
  }});
  window.addEventListener("hashchange", desdeHash);
  desdeHash();
}})();
</script>
</body>
</html>
"""


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "index.html").write_text(portada(), encoding="utf-8")
    (SALIDA / "chuleta.html").write_text(chuleta(), encoding="utf-8")
    for parte in (1, 2):
        (SALIDA / f"presentacion-parte-{parte}.html").write_text(presentacion(parte), encoding="utf-8")
    print("Generado en", SALIDA, "·", len(MODULOS), "módulos,", sum(len(m["puntos"]) for m in MODULOS), "puntos")


if __name__ == "__main__":
    main()
