# 13. Aplicaciones e ingeniería de prompts

!!! abstract "En este módulo"
    - Las tres formas de usar un modelo comercial: chat, agente y API.
    - El mapa de aplicaciones de IA generativa a finales de 2026: texto, imagen, vídeo, audio y herramientas especializadas.
    - Ingeniería de prompts: estructuras, ejemplos de antes y después, plantillas y errores frecuentes.

## 1. Tres formas de usar un modelo

Los grandes modelos comerciales (GPT de OpenAI, Gemini de Google, Claude de Anthropic, Grok de xAI…) se pueden usar de tres maneras:

| Modo | Cómo es | Para quién |
|---|---|---|
| **Chat** | Una aplicación web o móvil en la que conversas. Suele tener plan gratuito y suscripciones de unos 20 € al mes (y planes superiores para uso intensivo). | Cualquiera. |
| **Agente** | El modelo no solo responde: **actúa**. Navega por la web, maneja archivos, programa o usa tus aplicaciones conectadas para completar una tarea en varios pasos. | Tareas largas. Lo verás en el [módulo 17](17-agentes.md). |
| **API** | Tus programas envían peticiones al modelo y reciben la respuesta. Se paga por tokens. | Quien quiera integrar la IA en una web, una app o un flujo automático. Ver [módulo 15](15-api.md). |

Casi todas las aplicaciones de chat permiten además **configurar** el modelo: instrucciones personalizadas («respóndeme siempre en tono formal»), memoria, proyectos con documentos propios, elegir entre un modelo rápido y uno de razonamiento, activar la búsqueda web o conectar servicios como Google Drive o el correo ([módulo 16](16-habilidades-mcp.md)).

## 2. El mapa de aplicaciones

La lista cambia cada pocos meses; esta es una foto de **noviembre de 2026**. Más que memorizar nombres, conviene saber qué tipo de herramienta existe para cada tarea.

### Asistentes de texto (LLM)

- **ChatGPT** (OpenAI): el más popular y el que marca el estándar. Integra voz, visión, generación de imágenes, búsqueda, agentes y un ecosistema enorme de aplicaciones conectadas.
- **Gemini** (Google): integrado en Android, Gmail, Docs y el buscador. Destaca por su ventana de contexto muy grande y por entender vídeo.
- **Claude** (Anthropic): muy valorado para escribir, analizar documentos largos y programar, y por su enfoque en la seguridad. Fue el primero en ofrecer conectores MCP y habilidades ([módulo 16](16-habilidades-mcp.md)).
- **Grok** (xAI): integrado en X (Twitter), con acceso a lo que se publica en la red social en tiempo real.
- **Microsoft Copilot**: el asistente de Windows y Office, basado en modelos de OpenAI y de otros proveedores.
- **Le Chat** (Mistral AI): la principal empresa europea, con modelos comerciales y abiertos.
- **Modelos abiertos chinos**: **DeepSeek**, **Qwen** (Alibaba), **Kimi** (Moonshot AI) y **GLM** (Zhipu) compiten con los mejores modelos comerciales y publican sus pesos para que cualquiera los descargue y los use en su propio equipo.
- **Meta**: tras la familia Llama, en 2026 lanzó **Muse Spark**, que primero fue un modelo cerrado y en octubre se publicó con pesos abiertos bajo una licencia propia y restrictiva, y **Muse Glimmer**, un modelo pequeño con licencia Apache 2.0.
- **Agregadores**: **Perplexity** (un buscador que responde con fuentes citadas), **Poe** u **OpenRouter** dan acceso a modelos de varias empresas desde una misma aplicación o cuenta.

!!! note "Abierto no siempre significa libre"
    Un modelo de **pesos abiertos** (*open weights*) permite descargar los parámetros y usarlo en tu equipo, pero no siempre publica los datos ni el código de entrenamiento, y su licencia puede prohibir ciertos usos. Los modelos realmente **de código abierto** (como OLMo, del Allen Institute) publican todo.

### Imagen

- **GPT Image** (dentro de ChatGPT) y **Nano Banana** (el modelo de imagen de Gemini): editan fotos con instrucciones en lenguaje natural («quita a la persona del fondo», «ponle un sombrero») y escriben texto legible dentro de la imagen.
- **Midjourney**: referencia en calidad artística y estética.
- **Flux** (Black Forest Labs) y **Stable Diffusion**: modelos abiertos que pueden ejecutarse en local y personalizarse con estilos propios (LoRA, [módulo 18](18-fine-tuning.md)).
- **Ideogram**, **Seedream**, **Adobe Firefly**: otras opciones populares; Firefly se entrena con imágenes con licencia, lo que importa en usos comerciales.

### Vídeo

- **Sora** (OpenAI), **Veo** (Google), **Runway**, **Kling** y **Seedance**: generan clips de varios segundos a partir de texto o de una imagen, con movimientos de cámara y, en las versiones recientes, sonido y diálogos sincronizados.

### Audio y voz

- **Suno**: canciones completas (letra, música y voz) a partir de una descripción.
- **ElevenLabs**: síntesis y clonación de voz, doblaje a otros idiomas y efectos de sonido. Recuerda el [módulo 11](11-etica.md) antes de clonar una voz.

### Herramientas especializadas

- **Programación:** **GitHub Copilot**, **Cursor**, **Claude Code** o **Codex** (OpenAI). Los dos últimos ya son agentes ([módulo 17](17-agentes.md)).
- **Estudio e investigación:** **NotebookLM** (Google) responde solo a partir de los documentos que le subes y genera resúmenes en audio tipo pódcast; las funciones de **investigación profunda** (*deep research*) de ChatGPT, Gemini, Claude o Perplexity redactan informes con decenas de fuentes.
- **Ciencia:** **AlphaFold 3** (Google DeepMind) predice la estructura de proteínas y de sus interacciones con otras moléculas.
- **Presentaciones:** **Gamma** crea diapositivas a partir de un texto.

## 3. Ingeniería de prompts

Un **prompt** es la instrucción que le das al modelo. La **ingeniería de prompts** es el arte de escribirla para obtener lo que buscas a la primera. Los modelos de 2026 entienden peticiones vagas mucho mejor que los de 2023, pero un buen prompt sigue marcando la diferencia, sobre todo en tareas largas o en las API.

Un buen prompt suele incluir:

1. **Rol:** quién debe «ser» el modelo («Actúa como profesora de física de bachillerato»).
2. **Tarea:** qué quieres exactamente, con un verbo claro.
3. **Contexto:** para quién es, para qué, qué sabes ya. El modelo no lee tu mente.
4. **Datos o ejemplos:** el texto que debe usar, o uno o dos ejemplos del resultado que esperas (*few-shot*).
5. **Formato:** tabla, lista, correo, JSON, número de palabras.
6. **Restricciones:** lo que no debe hacer («no inventes cifras; si no lo sabes, dilo»).

### Estructuras para recordar

Hay muchas «fórmulas» con siglas. Todas dicen lo mismo con otro orden; elige una y úsala como lista de comprobación:

=== "R-T-F (Rol, Tarea, Formato)"

    ```text
    Actúa como [ROL]. Tu tarea es [TAREA] para [PÚBLICO].
    Devuélvelo en formato [FORMATO], con un máximo de [N] palabras.
    ```

=== "C-O-T (Contexto, Objetivo, Tarea)"

    ```text
    Contexto: [quién eres y en qué situación estás].
    Objetivo: [qué quieres conseguir].
    Tarea: [qué debe producir exactamente el modelo].
    ```

=== "P-A-S (Problema, Análisis, Solución)"

    ```text
    Problema: [descríbelo con datos].
    Analiza las causas posibles, propón tres soluciones con su coste e impacto,
    elige la mejor y dame un plan de acción para los próximos 90 días.
    ```

### Antes y después

| Prompt débil | Prompt mejorado |
|---|---|
| «Hazme un resumen.» | «Resume este informe en 5 viñetas con los datos clave y una recomendación final. Es para la dirección, que no es técnica. Máximo 120 palabras.» |
| «Escribe un correo.» | «Escribe un correo de 120-150 palabras a los padres de 2.º de ESO para recordarles la excursión del viernes 12: salida a las 8:30, vuelta a las 17:00, llevar comida. Tono cordial y claro. Incluye asunto.» |
| «Explícame la fotosíntesis.» | «Explícame la fotosíntesis como si tuviera 12 años, con una analogía de cocina. Después hazme 3 preguntas tipo test para comprobar que lo he entendido, sin darme las respuestas hasta que conteste.» |

### Técnicas útiles

- **Itera.** El primer resultado es un borrador: «más corto», «más formal», «añade un ejemplo», «quita la jerga».
- **Divide las tareas grandes.** Primero el índice, luego cada apartado.
- **Pide que razone o que pregunte.** «Antes de responder, hazme las preguntas que necesites para hacerlo bien.»
- **Da ejemplos.** Uno o dos ejemplos del estilo o del formato valen más que un párrafo de explicaciones.
- **Autoingeniería de prompts (*meta-prompting*).** Pide a la IA que escriba el prompt por ti: «Quiero que una IA me ayude a preparar un examen de historia. Escríbeme el mejor prompt posible para conseguirlo y pregúntame lo que te falte». Muchas plataformas tienen un botón de «mejorar prompt» que hace esto.
- **Instrucciones de sistema.** En las API y en LM Studio puedes fijar un *system prompt*: instrucciones que se aplican a toda la conversación (el rol, el tono, lo que no debe hacer). En las apps de chat equivalen a las instrucciones personalizadas o a los proyectos.

### Plantillas listas para usar

- **Resumen ejecutivo:** «Sintetiza en 6 viñetas con cifras. Añade "Riesgos" y "Siguientes pasos".»
- **Lluvia de ideas:** «Genera 15 ideas y clasifícalas en una tabla 2×2 por impacto y esfuerzo.»
- **Tabla comparativa:** «Compara [opciones] por precio, funciones, soporte y riesgos. Devuelve una tabla.»
- **Plan de estudio:** «Plan de 30 días para aprender [tema], 5 horas por semana, con objetivos medibles cada semana.»
- **Simulador de entrevista:** «Hazme una entrevista para [puesto]: 10 preguntas, de una en una, con comentarios a cada respuesta.»
- **Revisión de texto:** «Corrige ortografía y estilo de este texto. Muestra los cambios en una tabla con el original, la corrección y el motivo.»
- **Depuración de código:** «Analiza este error. Dame hipótesis ordenadas por probabilidad, cómo comprobar cada una y la solución.»
- **Traducción con tono:** «Traduce al inglés manteniendo un tono [cercano/formal]. Marca las expresiones que no tengan traducción directa.»
- **Investigación:** «Busca en la web 5 fuentes recientes sobre [tema], resume cada una en dos líneas con su enlace y señala en qué discrepan.»
- **Datos:** «Describe los patrones y valores atípicos de esta tabla y propón 3 gráficos para presentarlos.»

### Errores frecuentes

| Error | Solución |
|---|---|
| Ambigüedad | Define rol, objetivo y formato. |
| Falta de contexto | Aporta datos, ejemplos y restricciones. |
| Pedir demasiado a la vez | Divide la tarea e itera. |
| No verificar | Contrasta las cifras, las citas y los enlaces: los modelos [alucinan](08-ia-generativa.md). |
| Compartir datos sensibles | No pegues contraseñas, datos personales de terceros ni documentos confidenciales en servicios que no controlas ([módulo 11](11-etica.md)). |

!!! example "Actividad"
    Elige una tarea real de tu trabajo o tus estudios. Escribe primero un prompt de una línea y guarda la respuesta. Después reescríbelo con la estructura R-T-F, añade un ejemplo y una restricción, y compara. Por último, pídele a la IA que mejore tu prompt y prueba su versión. ¿Cuál ha funcionado mejor?

## Para ampliar

<div class="recursos" markdown>

**Guías**

- [Guía de ingeniería de prompts](https://www.promptingguide.ai/es) (DAIR.AI, en español): la referencia más completa, de lo básico a lo avanzado.
- [Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) (Anthropic, en inglés) y [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering) (OpenAI, en inglés): las guías oficiales.
- [200 prompts que todo programador debe conocer](https://drive.google.com/file/d/1uWlawLnt9AJnTl7E-_jMMTO_Uy_QgrLe/view) (libro electrónico en PDF, en español).
- [AIPRM](https://www.aiprm.com/): extensión con una biblioteca de prompts para ChatGPT y otros asistentes.

**Para explorar**

- :material-gesture-tap: [LMArena](https://lmarena.ai/): compara a ciegas las respuestas de dos modelos y vota; mantiene una clasificación pública de los mejores.
- :material-gesture-tap: [Artificial Analysis](https://artificialanalysis.ai/): comparativas independientes de calidad, velocidad y precio de los modelos.

</div>
