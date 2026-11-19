# IA de cero a modelo propio

Curso de Inteligencia Artificial en español, en dos partes, publicado como web con [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Web:** https://mosqueteroweb.github.io/IAconceptos/

## Contenido

**Primera parte, entender la IA:** 1. ¿Qué es la IA? · 2. Historia · 3. Tipos de IA · 4. Machine Learning · 5. Deep Learning y redes neuronales · 6. Multimodalidad · 7. Herramientas · 8. IA generativa · 9. Hardware (y práctica de montaje) · 10. Software · 11. Ética y responsabilidad

**Segunda parte, usar y crear modelos:** 12. Inferencia · 13. Aplicaciones e ingeniería de prompts · 14. IA en local (LM Studio y Ollama) · 15. La API · 16. Habilidades y MCP · 17. Agentes · 18. Fine-tuning · 19. Cuantización · 20. Destilación · 21. Pre-entrenamiento · 22. Crea tu propio modelo

Y un glosario. Cada módulo incluye diagramas, actividades y enlaces de ampliación verificados.

## Cuadernos de Colab

Las prácticas de cuantización, destilación y pre-entrenamiento están en [`notebooks/`](notebooks) y se abren directamente en Google Colab. Se generan con `tools/cuadernos.py`. Los conjuntos de datos de las prácticas de fine-tuning están en [`docs/descargas/`](docs/descargas) y se generan con `tools/datasets.py`.

## Uso en local

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Los diagramas propios se regeneran con `.venv/bin/python tools/diagramas.py` (primera parte) y `tools/diagramas2.py` (segunda parte). `tools/export_drive.py` prepara las versiones para Google Docs.

## Publicación

Cada push a `main` compila la web y la publica en GitHub Pages (`.github/workflows/deploy.yml`).

## Licencia

Autor: **MosqueteroWeb**. Texto y diagramas propios: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es).
