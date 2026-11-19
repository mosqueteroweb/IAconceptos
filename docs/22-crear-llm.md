# 22. Crea tu propio modelo

!!! abstract "En este módulo"
    - Qué significa, en la práctica, «crear tu propio LLM».
    - Las cuatro fases de un proyecto: objetivo, componentes, creación e iteración.
    - Proyecto final: **Chef-bot**, un asistente de cocina que funciona en tu ordenador.
    - Recursos para quien quiera construir un LLM desde cero, línea a línea.

## 1. ¿Qué significa «crear» un LLM?

Como viste en el [módulo 21](21-pre-entrenamiento.md), pre-entrenar un modelo como los de ChatGPT o Gemini está al alcance de muy pocas empresas. En la práctica, **crear tu propio LLM** significa tomar un **modelo abierto** ya pre-entrenado y transformarlo en una herramienta única para tu necesidad.

Es como montar un coche de carreras: no fabricas el motor (el pre-entrenamiento), sino que eliges el mejor motor del mercado (el modelo base) y lo ajustas, lo afinas y le añades piezas a medida ([fine-tuning](18-fine-tuning.md), [cuantización](19-cuantizacion.md), instrucciones y herramientas).

## 2. Las cuatro fases

### Fase 1. El objetivo :material-target:

Es la fase más importante, y no necesita ordenador. Responde por escrito:

- **¿Qué tarea concreta?** «Un asistente que genera recetas sencillas con los ingredientes que tengo», «Un corrector que adapta textos a lectura fácil», «Un clasificador de incidencias del servicio técnico». Cuanto más concreta, mejor.
- **¿Qué personalidad y qué tono?** Formal o cercano, breve o detallado.
- **¿Qué no debe hacer?** Temas que debe rechazar, información que no debe inventar.
- **¿Cómo sabré si funciona?** Criterios comprobables: «Con 20 listas de ingredientes que no estén en los datos, propone una receta viable en al menos 17».

Y una pregunta previa: **¿hace falta *fine-tuning*?** Muchas veces basta un buen prompt de sistema, una [habilidad](16-habilidades-mcp.md) o RAG con tus documentos ([módulo 18](18-fine-tuning.md#fine-tuning-prompt-o-rag)). Prueba primero lo sencillo.

### Fase 2. Los componentes :material-cog:

- **Modelo base.** El más grande que funcione con soltura en el equipo donde se usará (no en el que entrenas). Para un portátil, uno de 2 000 a 8 000 millones de parámetros, como Gemma 4 E2B/E4B o Qwen3 4B/8B. Comprueba su **licencia**.
- **Datos.** El corazón del proyecto: cientos de ejemplos de alta calidad que reflejen exactamente el objetivo de la fase 1. **Calidad antes que cantidad:** 500 ejemplos excelentes valen más que 50 000 mediocres.
- **Herramientas.** Para entrenar, **Unsloth Studio** (o Axolotl, si programas). Para probar y usar, **LM Studio** u **Ollama**.

### Fase 3. La creación :material-hammer-wrench:

1. **Fine-tuning** con LoRA o QLoRA: el modelo aprende su nueva especialidad.
2. **Evaluación** con los criterios de la fase 1, usando ejemplos que **no** estaban en los datos de entrenamiento.
3. **Fusión y cuantización** a GGUF (por ejemplo, Q4_K_M) para que funcione en un ordenador normal.
4. **Despliegue:** cargarlo en LM Studio u Ollama, con un prompt de sistema que lo complete.

### Fase 4. Iteración :material-refresh:

Un modelo propio nunca está «terminado». Al usarlo aparecerán fallos: cada uno es un **ejemplo nuevo** para los datos. El ciclo es:

**Uso → fallos → mejores datos → nuevo entrenamiento → uso.**

Es exactamente como mejoran los grandes modelos comerciales, a otra escala.

## 3. Proyecto final: Chef-bot

**Objetivo:** un asistente llamado **Chef-bot** que, con la lista de ingredientes que tienes en la nevera, propone **una receta sencilla en español**, con nombre, pasos breves y tiempo de preparación. No es un chat general: es un especialista.

**Componentes:**

- **Modelo base:** Gemma 4 E2B Instruct (Google, licencia Apache 2.0) o Qwen3 4B Instruct.
- **Datos:** [recetas.jsonl](descargas/recetas.jsonl): 59 ejemplos de ingredientes y recetas de cocina española y mediterránea, preparados para este curso. Ábrelo y añade tus propias recetas: cuantas más y mejores, mejor Chef-bot.
- **Herramientas:** Unsloth Studio (local o [en Colab](18-fine-tuning.md#practica)) y LM Studio.

### Paso 1. Prueba el modelo base

Antes de entrenar, carga el modelo base en LM Studio y escribe: `Tengo aguacates, cebolla morada, tomate y lima.` Guarda la respuesta. Será tu punto de comparación. ¿Es una receta? ¿Es breve? ¿Sigue siempre el mismo formato?

### Paso 2. Entrena

En Unsloth Studio, igual que en la [práctica del módulo 18](18-fine-tuning.md#practica):

1. *Model Type* **Text**, *Training Method* **QLoRA** y el modelo base elegido.
2. Sube `recetas.jsonl`, formato **alpaca**, *Eval split* del 10 %.
3. *Epochs*: **3**. Deja el resto por defecto y pulsa **Start Training**.
4. Vigila las dos pérdidas. Si la de validación empieza a subir, el modelo está memorizando recetas: para y entrena con menos épocas.

### Paso 3. Evalúa

En el chat de Studio, con el modelo ajustado, prueba **ingredientes que no estén en los datos**:

- `Tengo aguacates, cebolla morada, tomate y lima.`
- `Hay pasta, nata y bacon.`
- `Ingredientes: lentejas, arroz y cebolla.`
- `Solo me quedan huevos.`
- `¿Quién ganó el Mundial de 2010?` (fuera de su especialidad: ¿qué hace?)

Puntúa cada respuesta: ¿es una receta viable?, ¿sigue el formato?, ¿inventa ingredientes que no tienes? Compara con el paso 1.

### Paso 4. Crea el modelo final

En **Export**, elige el último *checkpoint*, **GGUF / llama.cpp** y descárgalo. El archivo es tu Chef-bot.

### Paso 5. ¡A cocinar!

1. Importa el GGUF en LM Studio (arrástralo a **My Models**, o en la terminal `lms import chef-bot.gguf`).
2. Cárgalo y añade un **prompt de sistema** que refuerce el papel: `Eres Chef-bot. Solo propones recetas sencillas con los ingredientes que te dan. Si te preguntan otra cosa, explica amablemente que solo sabes de cocina.`
3. Guárdalo como **preset** «Chef-bot».

El resultado esperado: ante `Tengo aguacates, cebolla morada, tomate y lima.`, algo como «Prepara un **guacamole**. Machaca los aguacates, añade la cebolla y el tomate picados, el zumo de la lima y sal. Tiempo: 10 minutos», con el mismo formato que los ejemplos.

!!! tip "Chef-bot en Ollama"
    Si prefieres Ollama, crea un archivo llamado `Modelfile` junto al GGUF:

    ```text
    FROM ./chef-bot.gguf
    SYSTEM "Eres Chef-bot. Solo propones recetas sencillas con los ingredientes que te dan."
    PARAMETER temperature 0.7
    ```

    y ejecuta `ollama create chef-bot -f Modelfile` y luego `ollama run chef-bot`.

### Paso 6. Itera

Apunta cada fallo (una receta que no tiene sentido, un ingrediente inventado, una respuesta demasiado larga), escribe el ejemplo correcto, añádelo a `recetas.jsonl` y vuelve a entrenar. Con unos 300 ejemplos buenos, Chef-bot será notablemente más fiable.

!!! example "Proyecto libre"
    Repite el proceso con una idea tuya. Algunas propuestas para el aula: un asistente que adapta textos a **lectura fácil**, un generador de **preguntas tipo test** sobre un tema, un corrector que explica las faltas de ortografía con las reglas de la RAE o un asistente que responde con el **tono de un personaje histórico**. Empieza por la fase 1, por escrito.

## 4. ¿Y desde cero de verdad?

Si te pica la curiosidad y sabes (o quieres aprender) programar, hay recursos excelentes para construir un LLM **línea a línea**, entendiendo cada pieza:

- **El curso de Karpathy** *Neural Networks: Zero to Hero*: de una neurona a un GPT completo en vídeos de dos horas. La práctica del módulo 21 está basada en él.
- **El libro de Sebastian Raschka** *Build a Large Language Model (From Scratch)* y su repositorio, que incluye implementaciones completas de modelos reales como OLMo 3, Qwen3 o Gemma 3, en un solo cuaderno.
- **RustGPT**: un LLM escrito en Rust **sin ninguna librería** de IA, ni siquiera PyTorch. Ideal para ver que no hay magia: solo multiplicaciones de matrices.
- **tiny_llm**: otro LLM mínimo y didáctico para estudiar su código.

## Para ampliar

<div class="recursos" markdown>

**Para construir desde cero**

- :material-youtube: [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) (Andrej Karpathy, en inglés con subtítulos).
- [LLMs from scratch](https://github.com/rasbt/LLMs-from-scratch) (Sebastian Raschka): el código del libro, y su [implementación de OLMo 3](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/13_olmo3/standalone-olmo3.ipynb) en un solo cuaderno.
- [RustGPT](https://github.com/tekaratzas/RustGPT): un LLM en Rust puro, sin librerías.
- [tiny_llm](https://github.com/Geddydukes/tiny_llm): un LLM pequeño y didáctico.
- [nanoGPT](https://github.com/karpathy/nanoGPT) y [nanochat](https://github.com/karpathy/nanochat) (Karpathy): el segundo entrena por unos cientos de dólares un pequeño ChatGPT completo, con pre-entrenamiento, ajuste e interfaz web.

**Para crear con modelos abiertos**

- [Documentación de Unsloth Studio](https://unsloth.ai/docs/new/studio) (en inglés).
- [Importar modelos en Ollama](https://docs.ollama.com/import) (en inglés).
- [Modelos abiertos en Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending): los más populares de cada semana.

</div>
