---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 20. Destila tu propio modelo

**Módulo:** [20. Destilación](../20-destilacion.md) · [Normas comunes de las prácticas](index.md)

!!! danger "Validación obligatoria en clase"
    El profesor tiene que ver en clase vuestro trabajo funcionando **antes** de que lo subas. Un trabajo subido sin haberlo validado antes en clase no se evalúa. Lo que tendréis que enseñar está en el apartado [Validación en clase](#validacion-en-clase).

**Objetivo:** destilar de verdad un modelo de lenguaje, como hizo DeepSeek con R1: un modelo **profesor** grande, en LM Studio, responde a cientos de preguntas, y con esas respuestas se ajusta un modelo **estudiante** mucho más pequeño. Después compararás a los tres (profesor, estudiante antes y estudiante después) en LM Studio.

**Material:** el script [destilar_profesor.py](../descargas/destilar_profesor.py), que se ejecuta con una sola orden (necesitas **uv**, mira las [normas comunes](index.md)).

## Qué modelos usar

| Equipo | Profesor (en LM Studio) | Estudiante (en Unsloth Studio) |
|---|---|---|
| Mac mini M4 16 GB | Qwen3 8B en Q4_K_M | Qwen3-0.6B |
| PC RTX 5060 Ti 16 GB | gpt-oss-20b o Qwen3 14B en Q4_K_M | Qwen3-0.6B o Qwen3-1.7B |

En el Mac, **expulsa el profesor** de LM Studio (*Eject*) antes de entrenar al estudiante, para liberar memoria.

## Ejemplo resuelto

**Tema del ejemplo:** los volcanes. Para que el ejemplo fuera rápido usamos como profesor **Gemma 4 E2B** y 120 preguntas (en vuestra práctica, el profesor es más grande: mirad la tabla de arriba). Equipo: Mac con chip M2 Pro.

**1. Preguntas.** Con Gemma 4 E2B cargado y el servidor en marcha:

```bash
uv run destilar_profesor.py preguntas --modelo google/gemma-4-e2b --tema "los volcanes" --n 30
```

Tardó **35 s** en generar 30 preguntas, en tandas de 15. Algunas:

- «¿Cuál es la diferencia fundamental entre magma y lava?»
- «¿Qué es un punto caliente y cómo se relaciona con los volcanes?»
- «¿Cuál es la principal diferencia entre un volcán escudo y un volcán estratovolcán?»

**Revisión.** Encontramos, entre otros, estos problemas, que hay que corregir a mano en `preguntas.txt`:

- Una **casi repetida**: «¿Qué son las cámaras magmáticas y cómo interactúan con la corteza terrestre?» y, más abajo, «¿Qué son las cámaras de magma y cómo determinan el volumen del volcán?». Borramos la segunda.
- Una **redundante**: «un volcán estratovolcán». La cambiamos por «un estratovolcán».
- Una **falta de concordancia**: «un erupción explosiva». La cambiamos por «una erupción explosiva».

**2. Prueba aparte.** Sacamos 10 preguntas a otro archivo, `prueba.txt`.

**3. Respuestas del profesor.**

```bash
uv run destilar_profesor.py respuestas --modelo google/gemma-4-e2b
```

El script muestra el avance y la velocidad: `[1/4] ¿Qué es un volcán y cuáles son sus componentes principales?… (63 tok/s de media)`. Cada respuesta se guarda en `datos_profesor.jsonl`, por ejemplo:

```json
{"instruction": "¿Cuál es la diferencia fundamental entre magma y lava?", "input": "", "output": "La diferencia fundamental entre magma y lava radica principalmente en su ubicación. El magma es la roca fundida que se encuentra debajo de la superficie terrestre…"}
```

Al revisarlas, una respuesta dice que el magma está compuesto por «silicatos metálicos»: es impreciso (son silicatos, que contienen metales como el hierro o el magnesio). Hay que corregirla a mano en `datos_profesor.jsonl` antes de entrenar.

Con 120 preguntas, las 110 respuestas de entrenamiento tardaron unos 12 minutos (59 tok/s de media).

!!! warning "Si el script se para con «LM Studio ha rechazado la petición»"
    Nos pasó a la mitad: cargamos otro modelo en LM Studio y el profesor se descargó. Volved a cargar el profesor y repetid la misma orden: el script continúa donde lo dejó.

**4-6. Destilación.** Entrenamos el estudiante, **Qwen3-0.6B**, con la orden `unsloth train` (el mismo motor que la interfaz de Unsloth Studio), con formato alpaca, 3 épocas y *Gradient Accumulation* 2:

```bash
unsloth train --model unsloth/Qwen3-0.6B --local-dataset datos_profesor.jsonl --format-type alpaca --num-epochs 3 --learning-rate 2e-4 --batch-size 4 --gradient-accumulation-steps 2 --lora-r 16 --lora-alpha 32 --max-seq-length 1024 --output-dir estudiante
```

**42 pasos en 89 s.** La pérdida bajó de 2,44 (paso 1) a 1,61 (paso 10), 1,37 (paso 20) y en torno a 1,0-1,1 al final. Lo exportamos a GGUF en **Q8_0** (639 MB) y lo importamos en LM Studio.

<figure markdown="span">
  ![Pérdida de la destilación](../img/practicas/p20-perdida.svg){ loading=lazy }
  <figcaption>Pérdida de entrenamiento del estudiante paso a paso.</figcaption>
</figure>


**7. Comparación** con las 10 preguntas de prueba, en LM Studio, temperatura 0 y sin *Think*:

| Modelo | Archivo | Velocidad | Respuestas en un párrafo, sin listas | Longitud media |
|---|---|---|---|---|
| Profesor (Gemma 4 E2B) | 4,41 GB | 60 tok/s | **0 de 10** | más de 350 tokens |
| Estudiante sin entrenar (Qwen3-0.6B) | 805 MB | 134 tok/s | **0 de 10** | 328 tokens |
| Estudiante destilado | 639 MB | 133 tok/s | **6 de 10** | 240 tokens |

- El **formato** se ha destilado: el estudiante responde en párrafos, como el profesor cuando generaba los datos. El profesor, en el chat normal, usa listas y encabezados, porque allí no recibe las instrucciones de estilo del script. El estudiante las ha aprendido sin necesitarlas.
- El **contenido**, no. El estudiante destilado dice que el volcán escudo se forma «cuando una erupción es muy fuerte o explosiva» (es al revés: es el de las erupciones tranquilas), que en las zonas de *rift* las placas «convergen» (divergen) y habla de la «cámara magnética» (magmática). Un modelo de 600 millones de parámetros no puede guardar lo que sabe uno de 4 600 millones.
- En nuestras 10 preguntas de prueba había **tres casi iguales** sobre el volcán escudo, porque no revisamos `prueba.txt`. En vuestra práctica, revisad también las preguntas de prueba.

## Vuestra práctica

Haced lo mismo que en el ejemplo con **el tema y el estilo de vuestro grupo** (en [vuestra tarjeta](#lo-especifico-de-cada-grupo)) y el profesor de vuestro tipo de equipo. En las órdenes, cambiad `qwen/qwen3-8b` por el identificador de vuestro profesor.

1. **Preguntas.** Con LM Studio abierto, el profesor cargado y el servidor en marcha (**Model Server → Status: Running**), generad **150 preguntas** sobre vuestro tema. En la terminal, dentro de la carpeta donde está el script (cambia el modelo y el tema por los tuyos):

    ```bash
    uv run destilar_profesor.py preguntas --modelo qwen/qwen3-8b --tema "la Edad Media en la península ibérica" --n 150
    ```

    **Revisa** el archivo `preguntas.txt`: elimina las repetidas, las ambiguas o las que no sean del tema, y añade **al menos 20 escritas por ti**.

2. **Prueba aparte.** Aparta **10 preguntas** que no usarás para entrenar: sácalas de `preguntas.txt` y guárdalas en otro archivo.
3. **Respuestas del profesor.** Generad las respuestas con **el estilo de vuestra tarjeta** (la opción `--estilo` cambia las instrucciones que recibe el profesor):

    ```bash
    uv run destilar_profesor.py respuestas --modelo qwen/qwen3-8b --estilo "EL ESTILO DE VUESTRA TARJETA"
    ```

    Anota cuánto tarda y a cuántos tokens por segundo trabaja el profesor. Revisa al menos **20 respuestas** de `datos_profesor.jsonl` y corrige las que tengan errores. Si se corta, vuelve a ejecutar la orden: continúa donde lo dejó.

4. **Antes.** Haz las 10 preguntas de prueba al **profesor** y al **estudiante** sin entrenar, en LM Studio, con **Think** desactivado. Guarda las respuestas y su velocidad.
5. **Destilación.** Ajusta el estudiante con **Unsloth Studio** usando tu archivo `datos_profesor.jsonl` (formato Alpaca, 10 % de validación, **Gradient Accumulation 2**). Captura las gráficas de pérdida y guarda la configuración.
6. **Después.** Exporta el estudiante a GGUF, impórtalo en LM Studio (`lms import -c -y --user-repo alumno/practica20 archivo.gguf`) y hazle las 10 preguntas de prueba.
7. **Comparación.** Haz una tabla con los tres modelos: tamaño del archivo, memoria al cargarlo, tokens por segundo y una puntuación de 0 a 2 de cada respuesta (corrección y estilo). ¿Cuánto se acerca el estudiante al profesor? ¿En qué falla?

## Lo específico de cada grupo

??? abstract "Grupo 1"
    - **Tema:** El sistema solar y la exploración espacial.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que incluye siempre un dato numérico. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 2"
    - **Tema:** La Edad Media en la península ibérica.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que incluye siempre una fecha. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 3"
    - **Tema:** El cuerpo humano: aparatos y sistemas.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que incluye siempre una comparación con algo de la vida diaria. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 4"
    - **Tema:** Economía doméstica: ahorro, nómina e impuestos.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que incluye siempre un ejemplo con euros. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 5"
    - **Tema:** La Segunda Guerra Mundial.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de exactamente tres frases, sin adjetivos valorativos. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 6"
    - **Tema:** Química de la cocina.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que termina siempre con un consejo práctico. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 7"
    - **Tema:** Ciberseguridad para usuarios.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que termina siempre con una pregunta de repaso. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 8"
    - **Tema:** Arte del Renacimiento.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que cita siempre una obra y su autor. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

??? abstract "Grupo 9"
    - **Tema:** Historia del cine.
    - **Estilo del profesor** (para `--estilo`):

        ```text
        Eres un profesor experto y paciente. Responde en español, en un párrafo de 3 a 6 frases que menciona siempre una película y su año. No uses listas ni encabezados.
        ```

    - **Para la comparación (tarea 7):** puntuad también de 0 a 2 si cada respuesta cumple vuestro estilo.

## Validación en clase

Tendréis que enseñar al profesor, en vuestro equipo:

- `preguntas.txt` y `datos_profesor.jsonl`, con alguna de las correcciones que hicisteis.
- El estudiante destilado cargado en LM Studio.
- Una pregunta nueva de vuestro tema, hecha en directo al profesor y al estudiante.

## Entregables

- `preguntas.txt` y `datos_profesor.jsonl`, con la lista de tus preguntas propias y de las respuestas que corregiste.
- Las respuestas de los tres modelos a las 10 preguntas de prueba.
- Capturas completas de LM Studio (profesor y estudiante cargados) y de las gráficas de Unsloth.
- La configuración guardada.
- La tabla del apartado 7 y tus conclusiones (máximo 250 palabras).

