---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 20. Destila tu propio modelo

**Módulo:** [20. Destilación](../20-destilacion.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** destilar de verdad un modelo de lenguaje, como hizo DeepSeek con R1: un modelo **profesor** grande, en LM Studio, responde a cientos de preguntas, y con esas respuestas se ajusta un modelo **estudiante** mucho más pequeño. Después compararás a los tres (profesor, estudiante antes y estudiante después) en LM Studio.

**Material:** el script [destilar_profesor.py](../descargas/destilar_profesor.py), que se ejecuta con una sola orden (necesitas **uv**, mira las [normas comunes](index.md)).

## Qué modelos usar

| Equipo | Profesor (en LM Studio) | Estudiante (en Unsloth Studio) |
|---|---|---|
| Mac mini M4 16 GB | Qwen3 8B en Q4_K_M | Qwen3-0.6B |
| PC RTX 5060 Ti 16 GB | gpt-oss-20b o Qwen3 14B en Q4_K_M | Qwen3-0.6B o Qwen3-1.7B |

En el Mac, **expulsa el profesor** de LM Studio (*Eject*) antes de entrenar al estudiante, para liberar memoria.

## Tu variante (tema de las preguntas)

| N.º | Tema |
|---|---|
| 1 | El sistema solar y la exploración espacial. |
| 2 | La Edad Media en la península ibérica. |
| 3 | El cuerpo humano: aparatos y sistemas. |
| 4 | Economía doméstica: ahorro, nómina e impuestos. |
| 5 | La Segunda Guerra Mundial. |
| 6 | Química de la cocina. |
| 7 | Ciberseguridad para usuarios. |
| 8 | Arte del Renacimiento. |

## Tareas

1. **Preguntas.** Con LM Studio abierto, el profesor cargado y el servidor en marcha (**Model Server → Status: Running**), genera **150 preguntas** sobre tu tema. En la terminal, dentro de la carpeta donde está el script (cambia el modelo y el tema por los tuyos):

    ```bash
    uv run destilar_profesor.py preguntas --modelo qwen/qwen3-8b --tema "la Edad Media en la península ibérica" --n 150
    ```

    **Revisa** el archivo `preguntas.txt`: elimina las repetidas, las ambiguas o las que no sean del tema, y añade **al menos 20 escritas por ti**.

2. **Prueba aparte.** Aparta **10 preguntas** que no usarás para entrenar: sácalas de `preguntas.txt` y guárdalas en otro archivo.
3. **Respuestas del profesor.** Genera las respuestas:

    ```bash
    uv run destilar_profesor.py respuestas --modelo qwen/qwen3-8b
    ```

    Anota cuánto tarda y a cuántos tokens por segundo trabaja el profesor. Revisa al menos **20 respuestas** de `datos_profesor.jsonl` y corrige las que tengan errores. Si se corta, vuelve a ejecutar la orden: continúa donde lo dejó.

4. **Antes.** Haz las 10 preguntas de prueba al **profesor** y al **estudiante** sin entrenar, en LM Studio, con **Think** desactivado. Guarda las respuestas y su velocidad.
5. **Destilación.** Ajusta el estudiante con **Unsloth Studio** usando tu archivo `datos_profesor.jsonl` (formato Alpaca, 10 % de validación, **Gradient Accumulation 2**). Captura las gráficas de pérdida y guarda la configuración.
6. **Después.** Exporta el estudiante a GGUF, impórtalo en LM Studio (`lms import -c -y --user-repo alumno/practica20 archivo.gguf`) y hazle las 10 preguntas de prueba.
7. **Comparación.** Haz una tabla con los tres modelos: tamaño del archivo, memoria al cargarlo, tokens por segundo y una puntuación de 0 a 2 de cada respuesta (corrección y estilo). ¿Cuánto se acerca el estudiante al profesor? ¿En qué falla?

## Entregables

- `preguntas.txt` y `datos_profesor.jsonl`, con la lista de tus preguntas propias y de las respuestas que corregiste.
- Las respuestas de los tres modelos a las 10 preguntas de prueba.
- Capturas completas de LM Studio (profesor y estudiante cargados) y de las gráficas de Unsloth.
- La configuración guardada.
- La tabla del apartado 7 y tus conclusiones (máximo 250 palabras).

**Defensa posible:** en clase, tus compañeros harán una pregunta nueva de tu tema a tu estudiante y al profesor, en directo.
