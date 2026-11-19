---
search:
  exclude: true
hide:
  - navigation
---

# Prácticas de la segunda parte (borrador para revisión)

!!! warning "Página de revisión"
    Esta página no está enlazada desde la web del curso. Contiene los enunciados de las prácticas de los módulos 13 a 22 (salvo la de agentes), pendientes de revisión antes de publicarlos.

## Normas comunes a todas las prácticas

**Equipos del aula.** Las prácticas están pensadas para los dos tipos de equipo del aula: **Mac mini M4 con 16 GB** y **PC con tarjeta NVIDIA RTX 5060 Ti de 16 GB**. Indica siempre en tu entrega en qué equipo has trabajado. Si una tarea no cabe en tu equipo, puedes usar **Google Colab**.

**Tu variante.** Casi todas las prácticas tienen **variantes**. Te corresponde la que indica tu **número de lista**: si hay 8 variantes y eres el número 11, te toca la 3 (11 − 8 = 3). Si se te acaban, vuelve a empezar. Una entrega con otra variante no se evalúa.

**Evidencias, no solo respuestas.** En estas prácticas se evalúa **lo que has hecho y lo que has medido tú**, no un texto bien escrito. Por eso cada práctica pide:

- **Capturas de pantalla completas**, en las que se vean la hora y la fecha del sistema (en Mac, la barra superior; en Windows, la barra de tareas). No recortes las capturas.
- **Los archivos que generes**: conjuntos de datos, configuraciones, cuadernos ejecutados con sus resultados, colecciones de Postman…
- **Cifras de tu propio equipo**: velocidades, tamaños y pérdidas que solo existen porque tú has hecho el experimento. Las cifras de otro equipo o inventadas se notan.
- **Materiales y claves de clase**: algunas prácticas usan un documento, una carpeta o una **palabra clave de la sesión** que se entrega en el aula y que no está publicada en ningún sitio.

**Uso de IA.** Puedes usar asistentes de IA para ayudarte (al fin y al cabo, es un curso de IA), pero **decláralo**: en un apartado final, indica qué herramienta has usado, para qué y qué has corregido de lo que te dio. Las preguntas de las prácticas se refieren a **tus resultados**: una IA no puede contestarlas sin ellos.

**Los modelos se prueban en LM Studio.** Todos los modelos que crees o transformes (prácticas 18 a 22) se importan y se prueban en **LM Studio**, en tu equipo. Las capturas de **Library** y del chat con tu modelo forman parte de la entrega.

**Defensa.** Cualquier práctica puede incluir una **defensa oral de 3 a 5 minutos** en el aula, delante de tu equipo: tendrás que repetir una parte del experimento o explicar una decisión. La nota de la práctica puede depender de esa defensa.

**Formato de entrega.** Un único documento (PDF o enlace a un documento compartido) con los apartados numerados como en el enunciado, más los archivos que se pidan, en una carpeta comprimida con tu nombre y el número de la práctica.

---

## Práctica 13. El laboratorio de prompts

**Módulo:** [13. Aplicaciones e ingeniería de prompts](../13-apps-prompts.md)

**Objetivo:** demostrar con tus propias pruebas cómo mejora una respuesta al mejorar el prompt, y aprender a verificar lo que dice una IA.

**Tu variante (escenario):**

| N.º | Escenario |
|---|---|
| 1 | Preparar un examen de Historia de 2.º de Bachillerato sobre un tema que elijas. |
| 2 | Plan de entrenamiento de 8 semanas para correr 10 km, para alguien que nunca ha corrido. |
| 3 | Menú semanal para una familia de cuatro con una persona celíaca y presupuesto ajustado. |
| 4 | Guion de un vídeo de 60 segundos para promocionar las jornadas de puertas abiertas del centro. |
| 5 | Comparativa de tres móviles de menos de 300 € para una persona mayor. |
| 6 | Carta de reclamación por un vuelo cancelado. |
| 7 | Plan de estudio para preparar el B2 de inglés en tres meses. |
| 8 | Organizar una excursión de un día para un grupo de 25 alumnos. |

**Tareas:**

1. **Prompt débil.** Escribe un prompt de una sola línea para tu escenario. Ejecútalo en un asistente (ChatGPT, Gemini, Claude o Copilot) y guarda la respuesta.
2. **Prompt estructurado.** Reescríbelo con una de las estructuras del módulo (R-T-F, C-O-T o P-A-S). Debe incluir **contexto real tuyo** (tu centro, tu ciudad, tus restricciones de verdad), un **formato** concreto y al menos **una restricción**. Ejecútalo en el mismo asistente.
3. **Meta-prompt.** Pide al asistente que te haga las preguntas que necesite y que después escriba él el mejor prompt para tu escenario. Contesta a sus preguntas y ejecuta el prompt que te proponga.
4. **Dos asistentes.** Ejecuta tu mejor prompt en **otro asistente distinto** (uno de ellos puede ser un modelo local de LM Studio).
5. **Tu rúbrica.** Define **cuatro criterios** para juzgar las respuestas de tu escenario (por ejemplo, «adaptado a mi presupuesto», «cifras verificables»…) y puntúa de 1 a 5 las cinco respuestas obtenidas en una tabla.
6. **Verificación.** Elige **tres afirmaciones concretas** de las respuestas (un dato, una cifra, un nombre, una norma) y compruébalas en una fuente fiable. Indica la fuente y si la IA acertó.

**Entregables:** los cinco prompts; las cinco respuestas como **enlace compartido** de la conversación o **captura completa**; la tabla de puntuaciones con tus criterios; la verificación con sus fuentes; una conclusión (máximo 150 palabras) sobre qué parte del prompt mejoró más el resultado, apoyada en **tu** tabla.

**Defensa posible:** el profesor ejecutará en clase uno de tus prompts en un asistente que tú no hayas usado y te pedirá que expliques para qué sirve cada parte del prompt.

---

## Práctica 14. Tu laboratorio de IA local

**Módulo:** [14. IA en tu ordenador: LM Studio y Ollama](../14-ia-local.md)

**Objetivo:** instalar y configurar LM Studio, medir el rendimiento real de tu equipo y comprobar cómo influyen los ajustes de carga, los de muestreo y el uso de documentos.

**Tu variante (pareja de modelos que vas a comparar):**

| N.º | Modelo A | Modelo B |
|---|---|---|
| 1 | Gemma 4 E2B en Q4_K_M | Gemma 4 E2B en Q8_0 |
| 2 | Qwen3 4B en Q4_K_M | Qwen3 4B en Q8_0 |
| 3 | Gemma 4 E2B en Q4_K_M | Gemma 4 E4B en Q4_K_M |
| 4 | Qwen3 1.7B en Q4_K_M | Qwen3 4B en Q4_K_M |
| 5 | Gemma 4 E4B en Q4_K_M | Qwen3 4B en Q4_K_M |
| 6 | Qwen3 4B en Q4_K_M | Qwen3 8B en Q4_K_M |

**Tareas:**

1. **Tu equipo.** Captura la pantalla **Ajustes → Hardware** de LM Studio y anota la memoria total y la utilizable como VRAM.
2. **Carga.** Descarga los dos modelos de tu variante. Para cada uno, abre los ajustes de carga manuales y anota la **memoria estimada** con un contexto de 4 096 tokens y con uno de 32 768. ¿Cuánto crece? ¿Por qué?
3. **Benchmark.** Con temperatura 0, haz a cada modelo las **cinco preguntas** que se repartirán en clase, **tres veces cada una**. Anota en una hoja de cálculo el tiempo hasta el primer token y los tokens por segundo de cada ejecución, y calcula las medias. Haz una gráfica con las medias.
4. **Muestreo.** Con el modelo que prefieras, pide «el principio de un cuento sobre [el objeto que te diga el profesor]» con temperatura 0,2, 1 y 1,6, y después con temperatura 1 y Top K 1. Copia las cuatro respuestas y describe las diferencias.
5. **Documentos.** Adjunta al chat el **documento que se entregará en clase** y responde con el modelo a las cinco preguntas que lo acompañan. Haz además **una pregunta cuya respuesta no esté en el documento**. ¿Qué hace el modelo? ¿Se lo inventa?
6. **Preset.** Crea un *preset* con un *System Prompt* para un uso tuyo real (tutor de una asignatura, corrector de tus redacciones…) y guárdalo.

**Entregables:** capturas completas de los apartados 1, 2, 5 y 6; la hoja de cálculo con las mediciones y la gráfica; las respuestas del apartado 4; un análisis (máximo 250 palabras) que responda, **con tus cifras**: ¿qué modelo elegirías para tu equipo y para qué tarea? ¿Compensa la diferencia de calidad la diferencia de velocidad?

**Defensa posible:** el profesor te pedirá que cargues uno de tus modelos con un contexto concreto y expliques en directo por qué cambia la memoria estimada, o que compares tus cifras con las de un compañero que haya usado el otro tipo de equipo del aula.

---

## Práctica 15. Tu propia API

**Módulo:** [15. Usar modelos desde tus programas: la API](../15-api.md)

**Objetivo:** usar un modelo desde un cliente HTTP, entender la estructura de las peticiones y comprobar por ti mismo que la API no tiene memoria.

**Tu variante (el asistente que vas a crear):**

| N.º | Asistente |
|---|---|
| 1 | Guía de un museo de ciencias inventado, con nombre y tres salas. |
| 2 | Conserje virtual del instituto: horarios, aulas y normas. |
| 3 | Asistente de una biblioteca municipal: préstamos, horarios y actividades. |
| 4 | Recepcionista de un hotel rural inventado. |
| 5 | Entrenador personal que solo habla de ejercicio y alimentación sana. |
| 6 | Asistente de una tienda de bicicletas eléctricas inventada. |
| 7 | Guía turístico de tu localidad. |
| 8 | Asistente de una clínica veterinaria inventada. |

**Tareas** (con el servidor local de LM Studio y Postman):

1. **Modelos.** Lista los modelos disponibles con una petición `GET`.
2. **Instrucciones de sistema.** Envía un mensaje con un *system prompt* que defina tu asistente: nombre, tono, tres datos concretos (teléfono, horario, precios…) y la **palabra clave de la sesión** que se dará en clase, que el asistente debe decir al despedirse.
3. **Historial.** Mantén una conversación de **tres turnos** construyendo tú el historial en el cuerpo de la petición. En el tercer turno, pregunta algo que solo se pueda responder con lo dicho en el primero.
4. **Sin memoria.** Repite la tercera pregunta **sin el historial**. Explica qué ocurre y por qué.
5. **Reproducibilidad.** Haz la misma petición dos veces con temperatura 0 y dos veces con temperatura 1,5. ¿Coinciden las respuestas?
6. **Salida estructurada.** Pide a tu asistente que devuelva una **ficha en JSON** con los campos que se indicarán en clase, usando `response_format` con un esquema JSON. Comprueba que la respuesta cumple el esquema.
7. **Terminal.** Repite la petición del apartado 2 con **curl** desde la terminal.

**Entregables:** la **colección de Postman exportada** (archivo `.json`) con todas las peticiones; capturas completas de Postman con cada respuesta; una captura de **Server Logs** de LM Studio en la que se vean tus peticiones; la orden de curl y su respuesta; las explicaciones de los apartados 4 y 5. Añade una tabla con los tokens de entrada y salida (`usage`) de tres peticiones y explica por qué crecen los de entrada a lo largo de la conversación.

**Opcional (+1 punto):** repite los apartados 2 y 3 con el nivel gratuito de la API de Gemini usando su endpoint compatible con OpenAI. **Nunca** incluyas tu clave en la entrega: tápala en las capturas.

**Defensa posible:** el profesor te dará un dato nuevo para tu asistente y tendrás que añadirlo y comprobarlo en directo.

---

## Práctica 16. Habilidades y conectores

**Módulo:** [16. Habilidades y conectores (MCP)](../16-habilidades-mcp.md)

**Objetivo:** escribir una habilidad que cambie de verdad el comportamiento de un modelo, y dar herramientas a un modelo local con MCP, controlando qué puede y qué no puede hacer.

**Tu variante (el documento que la habilidad debe redactar):**

| N.º | Documento |
|---|---|
| 1 | Convocatoria de una reunión de departamento. |
| 2 | Nota informativa a las familias. |
| 3 | Texto para el cartel de un evento del centro. |
| 4 | Acta breve de una reunión. |
| 5 | Correo de bienvenida a alumnado nuevo. |
| 6 | Noticia para la web del centro. |

**Parte A. Una habilidad**

1. En clase recibirás la **guía de estilo** (inventada) del centro. Escribe un `SKILL.md` que enseñe a un modelo a redactar el documento de tu variante **siguiendo esa guía**: nombre, descripción, instrucciones, un ejemplo y una lista de comprobación final.
2. Pruébala en un asistente que admita habilidades. Si no tienes acceso, pega el contenido de la habilidad como *System Prompt* en LM Studio.
3. Pide el mismo documento **con y sin** la habilidad, con los mismos datos. Comprueba punto por punto qué reglas de la guía cumple cada versión.
4. Mejora la habilidad al menos **una vez** a partir de los fallos que encuentres, y repite la prueba.

**Parte B. Un modelo con herramientas**

5. En LM Studio, añade en `mcp.json` dos servidores MCP: el de **hora** (`mcp-server-time`) y el de **archivos** (`server-filesystem`), este último **limitado a la carpeta de prácticas** que se te entregará en clase.
6. Con un modelo que sepa usar herramientas, haz tres preguntas que necesiten las herramientas, al menos una que combine las dos (por ejemplo, sobre los archivos de la carpeta y la fecha de hoy).
7. Pide al modelo que **lea un archivo que esté fuera** de la carpeta permitida. ¿Qué ocurre?
8. Busca **un error** del modelo: una herramienta mal elegida, un dato mal leído o una respuesta inventada.

**Entregables:** la carpeta de la habilidad comprimida (versión inicial y mejorada); la tabla de comprobación de la guía de estilo (con y sin habilidad); tu `mcp.json`; capturas completas de cada llamada a herramienta, **incluida la ventana de permiso**; una reflexión (máximo 200 palabras) sobre qué riesgos tendría dar acceso a tu carpeta personal entera o a tu correo.

**Defensa posible:** el profesor añadirá una regla nueva a la guía de estilo y tendrás que incorporarla a tu habilidad y probarla en directo.

---

## Práctica 18. Un modelo con estilo propio

**Módulo:** [18. Fine-tuning](../18-fine-tuning.md)

**Objetivo:** crear tu propio conjunto de datos, ajustar un modelo con QLoRA y comprobar con pruebas si de verdad ha aprendido el estilo, sin memorizar.

**Tu variante (el estilo que aprenderá tu modelo):**

| N.º | Estilo |
|---|---|
| 1 | Locutor de radio deportiva que lo narra todo como un partido. |
| 2 | Abuela que responde con un refrán y un consejo. |
| 3 | Presentador de documentales de naturaleza. |
| 4 | Asistente que responde siempre en tres viñetas y una pregunta final. |
| 5 | Caballero medieval que habla en castellano antiguo. |
| 6 | Profesor que nunca da la respuesta y guía con preguntas. |
| 7 | Periodista de sucesos que convierte cualquier tema en titular. |
| 8 | Asistente que explica todo con analogías de cocina. |

**Tareas:**

1. **Datos.** Crea un archivo JSONL en formato Alpaca con **al menos 60 ejemplos** de tu estilo, sobre temas variados. Puedes ayudarte de una IA para generar borradores, pero **revisa y corrige cada ejemplo** y escribe tú **al menos 20** desde cero (márcalos en una lista).
2. **Prueba aparte.** Escribe **10 preguntas de prueba** que **no** estén en los datos.
3. **Antes.** Haz las 10 preguntas al modelo base y guarda las respuestas.
4. **Entrenamiento.** Ajusta el modelo indicado en clase para tu tipo de equipo con **Unsloth Studio** (en tu equipo o en Colab), con QLoRA y un 10 % de validación. Guarda la configuración (**Save**) y captura las gráficas de pérdida.
5. **Después.** Haz las mismas 10 preguntas al modelo ajustado. Puntúa de 0 a 2 cada respuesta del modelo base y del ajustado: ¿mantiene el estilo?, ¿es correcta?
6. **Experimento.** Entrena una segunda vez cambiando **una sola cosa**: el número de épocas (1 o 6) o el rango de LoRA (4 o 64). Compara la pérdida de validación y las respuestas. ¿Hay sobreajuste? ¿Cómo lo sabes?
7. **Exportación.** Exporta el mejor modelo a GGUF, impórtalo en LM Studio y conversa con él.

**Entregables:** el archivo JSONL; la lista de los ejemplos escritos por ti; la configuración guardada (YAML) de los dos entrenamientos; capturas completas de las gráficas de pérdida; la tabla de puntuaciones antes y después; la captura de LM Studio con tu modelo cargado; las conclusiones del experimento.

**Defensa posible:** en clase, tus compañeros escribirán tres preguntas nuevas y tu modelo tendrá que responderlas en directo con tu estilo.

---

## Práctica 19. Cuantizar y medir

**Módulo:** [19. Cuantización](../19-cuantizacion.md)

**Objetivo:** cuantizar un modelo tú mismo y medir con datos (tamaño, velocidad y perplejidad) qué se gana y qué se pierde.

**Tu variante:**

| N.º | Modelo para el cuaderno | Modelo para LM Studio |
|---|---|---|
| 1 | Qwen3-0.6B | Gemma 4 E2B (Q4_K_M y Q8_0) |
| 2 | Qwen3-1.7B | Qwen3 4B (Q4_K_M y Q8_0) |
| 3 | Qwen3-0.6B | Qwen3 8B (Q3_K_M y Q4_K_M) |
| 4 | Qwen3-1.7B | Gemma 4 E4B (Q4_K_M y Q8_0) |
| 5 | Qwen3-4B | Qwen3 1.7B (Q4_K_M y Q8_0) |

**Tareas:**

1. **Cuaderno.** Ejecuta el [cuaderno de cuantización](https://colab.research.google.com/github/mosqueteroweb/IAconceptos/blob/main/notebooks/cuantizacion.ipynb) con el modelo de tu variante (cambia la variable `MODELO`). Anota el tamaño, la velocidad y la **perplejidad** de cada versión.
2. **Pregunta propia.** Cambia la `PREGUNTA` por una de tu elección sobre una asignatura que estudies y compara las cuatro respuestas.
3. **Gráfica.** Representa en una gráfica el tamaño frente a la perplejidad. ¿Dónde está el «codo», el punto a partir del cual comprimir más ya no compensa?
4. **Tu equipo.** En LM Studio, descarga el modelo de tu variante en las dos cuantizaciones indicadas, mide la velocidad (tres preguntas, tres veces cada una) y anota la memoria estimada de carga.
5. **Tus GGUF en LM Studio.** Descarga del cuaderno tus archivos `Q4_K_M` y `Q2_K`, impórtalos en LM Studio (`lms import -c archivo.gguf`) y hazles las mismas tres preguntas del apartado 4. Mide su velocidad **en tu equipo** y compárala con la del cuaderno.
6. **Cálculo.** Con la regla del módulo, calcula cuánto ocuparía un modelo de **14 000 millones de parámetros** en BF16, Q8_0 y Q4_K_M. ¿Cuál cabría en tu equipo? ¿Y en el otro tipo de equipo del aula? Justifícalo con los datos de la pantalla **Hardware** de LM Studio.

**Entregables:** el **cuaderno ejecutado** descargado con sus resultados (`.ipynb`); la tabla y la gráfica del apartado 3; las respuestas del apartado 2; las mediciones de LM Studio con capturas completas (incluida la pantalla **Library** con tus modelos importados); los cálculos del apartado 6.

**Defensa posible:** explicar con tus cifras por qué la versión más comprimida no siempre es la más rápida en tu equipo, o por qué la perplejidad de Q8_0 es casi igual a la del original.

---

## Práctica 20. Destila tu propio modelo

**Módulo:** [20. Destilación](../20-destilacion.md)

**Objetivo:** destilar de verdad un modelo de lenguaje, como hizo DeepSeek con R1: un modelo **profesor** grande, en LM Studio, responde a cientos de preguntas, y con esas respuestas se ajusta un modelo **estudiante** mucho más pequeño. Después compararás a los tres (profesor, estudiante antes y estudiante después) en LM Studio.

**Material:** el script [destilar_profesor.py](../descargas/destilar_profesor.py), que se ejecuta con una sola orden (necesitas **uv**, el mismo de la práctica 16), y el modelo profesor y el estudiante que se indicarán en clase para tu tipo de equipo.

**Tu variante (tema de las preguntas):**

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

**Tareas:**

1. **Preguntas.** Con LM Studio abierto, el modelo profesor cargado y el servidor en marcha, genera **150 preguntas** sobre tu tema con la orden `preguntas` del script. **Revísalas**: elimina las repetidas, las ambiguas o las que no sean del tema, y añade **al menos 20 escritas por ti**.
2. **Prueba aparte.** Aparta **10 preguntas** que no usarás para entrenar.
3. **Respuestas del profesor.** Genera las respuestas con la orden `respuestas`. Anota cuánto tarda y a cuántos tokens por segundo trabaja el profesor. Revisa al menos **20 respuestas** y corrige las que tengan errores.
4. **Antes.** Haz las 10 preguntas de prueba al **profesor** y al **estudiante** sin entrenar, en LM Studio. Guarda las respuestas y su velocidad.
5. **Destilación.** Ajusta el estudiante con **Unsloth Studio** usando tu archivo `datos_profesor.jsonl` (formato Alpaca, 10 % de validación). Captura las gráficas de pérdida y guarda la configuración.
6. **Después.** Exporta el estudiante a GGUF, impórtalo en LM Studio y hazle las 10 preguntas de prueba.
7. **Comparación.** Haz una tabla con los tres modelos: tamaño del archivo, memoria al cargarlo, tokens por segundo y una puntuación de 0 a 2 de cada respuesta (corrección y estilo). ¿Cuánto se acerca el estudiante al profesor? ¿En qué falla?

**Entregables:** `preguntas.txt` y `datos_profesor.jsonl` (con la lista de tus preguntas propias y de las respuestas que corregiste); las respuestas de los tres modelos a las 10 preguntas de prueba; capturas completas de LM Studio (profesor y estudiante cargados) y de las gráficas de Unsloth; la configuración guardada; la tabla del apartado 7 y tus conclusiones (máximo 250 palabras).

**Defensa posible:** en clase, tus compañeros harán una pregunta nueva de tu tema a tu estudiante y al profesor, en directo.

---

## Práctica 21. Tu nano-modelo

**Módulo:** [21. Pre-entrenamiento](../21-pre-entrenamiento.md)

**Objetivo:** pre-entrenar un modelo desde cero con un libro distinto del Quijote, observar cómo aprende, relacionar el tamaño del modelo y de los datos con el resultado, y abrir tu propio modelo en LM Studio.

**Tu variante:**

| N.º | Libro (`LIBRO`) | Cambio en la arquitectura |
|---|---|---|
| 1 | 320 · *Lazarillo de Tormes* | `CAPAS = 2` |
| 2 | 16625 · *Libro de Buen Amor* | `CAPAS = 6` |
| 3 | 29506 · *El sombrero de tres picos* | `DIM = 128` |
| 4 | 49836 · *Niebla* | `DIM = 384` |
| 5 | 17340 · *Marianela* | `CONTEXTO = 64` |
| 6 | 58221 · *La Odisea* | `CONTEXTO = 256` |
| 7 | 24536 · *Los cuatro jinetes del Apocalipsis* | `PASOS = 10000` |

**Tareas:**

1. Ejecuta el [cuaderno del nano-modelo](https://colab.research.google.com/github/mosqueteroweb/IAconceptos/blob/main/notebooks/nanomodelo-quijote.ipynb) cambiando solo `LIBRO`. Anota el número de caracteres del libro, el **tamaño del vocabulario**, los **parámetros** del modelo, la tabla de pérdidas y el texto generado.
2. Ejecútalo otra vez con el **cambio de arquitectura** de tu variante. Anota lo mismo y el tiempo de entrenamiento.
3. Genera texto con **temperatura 0,3, 0,8 y 1,3** con tu mejor modelo y empezando por una frase **típica de tu libro**.
4. Compara tus pérdidas con las del Quijote publicadas en el módulo 21. ¿Tu libro es más o menos «difícil» de aprender? ¿Influye su tamaño?
5. Busca señales de **sobreajuste**: ¿se separan las pérdidas de entrenamiento y validación? ¿Copia el modelo frases literales del libro? Busca dos frases generadas en el texto original y di si aparecen.
6. **Segunda parte: a LM Studio.** Ejecuta la segunda parte del cuaderno (el nano-Llama con el tokenizador de SmolLM2) con tu libro. Anota cuántos **tokens** ocupa el libro con este tokenizador frente a los caracteres de la primera parte, y por qué el modelo tiene ahora unos 16 millones de parámetros.
7. Descarga tu archivo GGUF, impórtalo en LM Studio (`lms import -c nano-libro-XXXX.gguf`) y escríbele el principio de tres frases típicas de tu libro. Captura las respuestas y la velocidad. Compárala con la de Gemma 4 E2B en tu equipo.

**Entregables:** el **cuaderno ejecutado** de las dos ejecuciones (`.ipynb`); una tabla comparativa de las dos ejecuciones; las gráficas de pérdida; los textos generados; las respuestas a los apartados 4 a 6; las capturas completas de tu modelo en LM Studio (Library y chat).

**Defensa posible:** explicar en clase, con tus gráficas, qué ha cambiado al modificar la arquitectura y por qué.

---

## Práctica 22. Proyecto final: tu propio modelo

**Módulo:** [22. Crea tu propio modelo](../22-crear-llm.md)

**Objetivo:** recorrer el ciclo completo de creación de un modelo especializado, desde la idea hasta una demostración en directo, y justificar cada decisión.

**Tema:** eliges tú el tema, pero debe **aprobarlo el profesor** antes de empezar y no puede repetirse en el grupo. Debe ser una tarea concreta y útil (no un chat general), distinta de la de la práctica 18.

**Fases y entregables:**

1. **Ficha del proyecto** (antes de empezar). Tarea, público, tono, qué no debe hacer y **cinco criterios de éxito** comprobables.
2. **¿Hace falta fine-tuning?** Antes de entrenar, intenta resolver la tarea **solo con un *system prompt*** (y, si sirve, una habilidad o documentos). Pruébalo con 20 casos y puntúalo. Este será tu **punto de partida**.
3. **Datos.** Un conjunto de **al menos 150 ejemplos** de calidad, con un registro de cómo los has obtenido (escritos por ti, adaptados de fuentes que cites, generados con IA y revisados…) y de las correcciones que has hecho.
4. **Entrenamiento.** Ajuste con Unsloth Studio, con validación, y las gráficas de pérdida.
5. **Evaluación.** Los **mismos 20 casos** del apartado 2 con el modelo ajustado, con la misma puntuación. ¿Ha mejorado respecto al *system prompt*? Si no, explica por qué.
6. **Iteración.** Al menos **un segundo entrenamiento** después de corregir los datos a partir de los fallos. Documenta qué cambiaste y qué mejoró.
7. **Despliegue.** El modelo en GGUF, cargado en LM Studio con un *preset* propio.
8. **Demostración** (5 minutos, en clase). Presentas tu modelo y respondes en directo a **entradas nuevas que te darán tus compañeros**.

**Evaluación:** ficha y planteamiento (15 %), calidad y documentación de los datos (25 %), entrenamiento y evaluación (25 %), iteración (15 %), demostración (20 %).
