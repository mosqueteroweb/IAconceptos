# IAconceptos

Curso introductorio de Inteligencia Artificial en español, publicado como web con [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Web:** https://mosqueteroweb.github.io/IAconceptos/

## Contenido

1. ¿Qué es la IA? · 2. Historia · 3. Tipos de IA · 4. Machine Learning · 5. Deep Learning y redes neuronales · 6. Multimodalidad · 7. Herramientas · 8. IA generativa · 9. Hardware (y práctica de montaje) · 10. Software · 11. Ética y responsabilidad · Glosario

Cada módulo incluye diagramas, actividades y enlaces de ampliación verificados.

## Uso en local

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Los diagramas propios se regeneran con `.venv/bin/python tools/diagramas.py`.

## Publicación

Cada push a `main` compila la web y la publica en GitHub Pages (`.github/workflows/deploy.yml`).

## Licencia

Autor: **MosqueteroWeb**. Texto y diagramas propios: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es).
