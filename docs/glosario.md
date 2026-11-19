# Glosario

Términos clave del curso, en orden alfabético.

Agente
:   Sistema de IA que encadena acciones de forma autónoma (buscar, usar herramientas, escribir y probar código…) para completar una tarea. Ver [módulo 17](17-agentes.md).

AGI (Inteligencia Artificial General)
:   IA hipotética con una inteligencia tan flexible como la humana, capaz de aprender cualquier tarea intelectual. No existe todavía. Ver [módulo 3](03-tipos-de-ia.md).

Alucinación
:   Respuesta de un modelo generativo que suena convincente pero es falsa o inventada.

ANI (IA estrecha o débil)
:   IA especializada en una tarea concreta. Es la mayoría de la IA que existe.

API
:   Interfaz que permite a un programa usar un modelo enviando peticiones y recibiendo respuestas (normalmente en JSON). Se paga por tokens. Ver [módulo 15](15-api.md).

Aprendizaje autosupervisado
:   Entrenamiento en el que las etiquetas salen de los propios datos (por ejemplo, adivinar la palabra siguiente). Es como se preentrenan los LLM.

Aprendizaje no supervisado
:   El modelo busca estructura en datos sin etiquetas, por ejemplo, agrupándolos (*clustering*).

Aprendizaje por refuerzo
:   El agente aprende por ensayo y error a partir de recompensas y castigos.

Aprendizaje supervisado
:   El modelo aprende a partir de ejemplos etiquetados con la respuesta correcta. Incluye la clasificación y la regresión.

Atención (mecanismo de)
:   Parte del Transformer que permite a cada token «fijarse» en los otros tokens relevantes del texto.

Caché KV
:   Memoria donde el modelo guarda los cálculos de los tokens ya procesados para no repetirlos al generar cada token nuevo. Crece con la longitud de la conversación. Ver [módulo 12](12-inferencia.md).

Conector
:   Integración que permite a un modelo acceder a una aplicación o servicio (correo, Drive, calendario…) con los permisos de tu cuenta. Hoy se construyen casi siempre con MCP. Ver [módulo 16](16-habilidades-mcp.md).

Cuantización
:   Guardar los parámetros de un modelo con menos bits (8 o 4) para que ocupe menos memoria y funcione más rápido. Ver [módulo 19](19-cuantizacion.md).

CUDA
:   Plataforma de NVIDIA para programar sus GPUs. Es la base de casi todo el software de IA.

Deep Learning (aprendizaje profundo)
:   Machine Learning con redes neuronales de muchas capas.

Deepfake (ultrafalso)
:   Vídeo, imagen o audio manipulado con IA para que parezca auténtico.

Descenso del gradiente
:   Algoritmo de optimización que ajusta los pesos de un modelo poco a poco en la dirección que reduce el error.

Destilación
:   Técnica en la que un modelo grande (profesor) enseña a uno pequeño (estudiante) a imitar sus probabilidades. Ver [módulo 20](20-destilacion.md).

Embedding
:   Representación de una palabra, imagen u otro dato como un vector de números, de modo que los elementos con significado parecido quedan cerca.

Fine-tuning (ajuste fino)
:   Seguir entrenando un modelo ya entrenado con datos específicos para especializarlo. LoRA y QLoRA son técnicas eficientes para hacerlo. Ver [módulo 18](18-fine-tuning.md).

Función de activación
:   Función que transforma la suma ponderada de una neurona (ReLU, sigmoide…) y permite a la red aprender relaciones no lineales.

Función de pérdida (loss)
:   Medida de cuánto se equivoca el modelo. El entrenamiento intenta minimizarla.

GGUF
:   Formato de archivo de llama.cpp, LM Studio y Ollama que guarda en un solo fichero un modelo cuantizado, su tokenizador y su descripción. Ver [módulo 19](19-cuantizacion.md).

GPU
:   Unidad de procesamiento gráfico. Hace miles de operaciones en paralelo y es el hardware principal para entrenar y ejecutar modelos.

Habilidad (skill)
:   Carpeta con un archivo `SKILL.md` que enseña a un modelo o agente cómo hacer una tarea concreta. Estándar abierto desde 2025. Ver [módulo 16](16-habilidades-mcp.md).

IA generativa
:   IA que crea contenido nuevo: texto, imágenes, audio, vídeo o código.

Inferencia
:   Usar un modelo ya entrenado para obtener respuestas o predicciones. Durante la inferencia el modelo no aprende. Ver [módulo 12](12-inferencia.md).

Llamada a herramientas (tool calling)
:   Capacidad de un modelo para pedir, en formato estructurado, que la aplicación ejecute una función externa (buscar, consultar la hora, enviar un correo) y usar el resultado.

LLM (modelo de lenguaje grande)
:   Red neuronal de tipo Transformer entrenada con enormes cantidades de texto para predecir el siguiente token. Es el motor de ChatGPT, Gemini o Claude.

LoRA y QLoRA
:   Técnicas de fine-tuning eficiente: congelan el modelo y entrenan dos matrices pequeñas que se suman a sus pesos. QLoRA lo hace sobre el modelo cuantizado a 4 bits. Ver [módulo 18](18-fine-tuning.md).

Machine Learning (aprendizaje automático)
:   Rama de la IA en la que los sistemas aprenden patrones a partir de datos en lugar de seguir reglas escritas a mano.

MCP (Model Context Protocol)
:   Estándar abierto, creado por Anthropic en 2024, para conectar modelos y agentes con herramientas y fuentes de datos externas. Ver [módulo 16](16-habilidades-mcp.md).

Mezcla de expertos (MoE)
:   Arquitectura en la que cada token solo activa una parte de los parámetros del modelo (los «expertos» elegidos). Permite modelos grandes y rápidos a la vez.

Modelo
:   Resultado del entrenamiento: un conjunto de parámetros que codifica lo aprendido y permite hacer predicciones.

Modelo base
:   Modelo recién pre-entrenado: sabe mucho, pero solo continúa textos. Tras el post-entrenamiento se convierte en un modelo *instruct* o de chat. Ver [módulo 21](21-pre-entrenamiento.md).

Modelo de difusión
:   Modelo generativo que aprende a eliminar ruido de una imagen y, partiendo de ruido puro, genera imágenes nuevas.

Modelo de pesos abiertos (open weights)
:   Modelo cuyos parámetros se pueden descargar y ejecutar en tu equipo. No siempre publica sus datos ni su código de entrenamiento, y su licencia puede limitar usos.

Muestreo (sampling)
:   Forma de elegir cada token entre los posibles según sus probabilidades, controlada por la temperatura, top-k, top-p y otros ajustes. Ver [módulo 12](12-inferencia.md).

Multimodal
:   Que trabaja con varios tipos de datos a la vez (texto, imagen, audio, vídeo).

Orquestador
:   Sistema que divide un objetivo en tareas, las reparte entre varios agentes y junta sus resultados. Ver [módulo 17](17-agentes.md).

Parámetros (pesos y sesgos)
:   Los números internos de un modelo que se ajustan durante el entrenamiento. Los grandes modelos tienen miles de millones.

Pre-entrenamiento
:   Primera fase del entrenamiento de un LLM: predecir el siguiente token en billones de textos. Es la más larga y cara. Ver [módulo 21](21-pre-entrenamiento.md).

Prompt
:   Instrucción o texto que se le da a un modelo generativo.

Prompt de sistema
:   Instrucciones generales (rol, tono, reglas) que se aplican a toda una conversación. En las aplicaciones de chat equivalen a las instrucciones personalizadas.

RAG (generación aumentada por recuperación)
:   Técnica que busca en tus documentos los fragmentos relacionados con la pregunta y se los pasa al modelo para que responda con ellos. Ver [módulo 14](14-ia-local.md).

Red neuronal artificial
:   Modelo formado por neuronas artificiales conectadas en capas.

Red neuronal convolucional (CNN)
:   Tipo de red especializada en imágenes que usa filtros para detectar rasgos locales.

Retropropagación (backpropagation)
:   Algoritmo que calcula cuánto contribuye cada peso al error, recorriendo la red de la salida a la entrada.

RLHF
:   Aprendizaje por refuerzo con retroalimentación humana: se ajusta un modelo para que dé las respuestas que las personas prefieren.

Sesgo algorítmico
:   Resultado injusto o discriminatorio de un sistema de IA, normalmente heredado de los datos de entrenamiento.

Sobreajuste (overfitting)
:   Cuando un modelo memoriza los datos de entrenamiento y falla con datos nuevos.

Temperatura
:   Ajuste del muestreo: baja hace las respuestas más predecibles; alta, más variadas y arriesgadas.

Token
:   Fragmento de texto (una palabra, parte de una palabra o un signo) con el que trabaja un modelo de lenguaje.

Tokenizador
:   Componente que trocea el texto en tokens y los convierte en números (y viceversa). Cada modelo tiene el suyo. Ver [módulo 21](21-pre-entrenamiento.md).

Top-p (nucleus sampling)
:   Ajuste del muestreo que solo sortea entre las opciones más probables cuya probabilidad suma *p* (por ejemplo, el 90 %).

TPU
:   Chip de Google diseñado específicamente para cálculos de IA.

Transformer
:   Arquitectura de red neuronal presentada en 2017, basada en el mecanismo de atención. Es la base de los LLM y de muchos modelos de imagen.

TTFT y tokens por segundo
:   Las dos medidas de velocidad de un modelo: el tiempo hasta el primer token (cuánto tarda en empezar a responder) y los tokens generados por segundo. Ver [módulo 12](12-inferencia.md).

Ventana de contexto
:   Número máximo de tokens que un modelo puede tener en cuenta a la vez: instrucciones, historial, documentos y su propia respuesta.

VRAM
:   Memoria de la tarjeta gráfica. Determina qué tamaño de modelo cabe en ella.

