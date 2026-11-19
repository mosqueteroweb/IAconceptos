# Glosario

Términos clave del curso, en orden alfabético.

Agente
:   Sistema de IA que encadena acciones de forma autónoma (buscar, usar herramientas, escribir y probar código…) para completar una tarea.

AGI (Inteligencia Artificial General)
:   IA hipotética con una inteligencia tan flexible como la humana, capaz de aprender cualquier tarea intelectual. No existe todavía. Ver [módulo 3](03-tipos-de-ia.md).

Alucinación
:   Respuesta de un modelo generativo que suena convincente pero es falsa o inventada.

ANI (IA estrecha o débil)
:   IA especializada en una tarea concreta. Es la mayoría de la IA que existe.

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

Cuantización
:   Guardar los parámetros de un modelo con menos bits (8 o 4) para que ocupe menos memoria y funcione más rápido.

CUDA
:   Plataforma de NVIDIA para programar sus GPUs. Es la base de casi todo el software de IA.

Deep Learning (aprendizaje profundo)
:   Machine Learning con redes neuronales de muchas capas.

Deepfake (ultrafalso)
:   Vídeo, imagen o audio manipulado con IA para que parezca auténtico.

Descenso del gradiente
:   Algoritmo de optimización que ajusta los pesos de un modelo poco a poco en la dirección que reduce el error.

Embedding
:   Representación de una palabra, imagen u otro dato como un vector de números, de modo que los elementos con significado parecido quedan cerca.

Fine-tuning (ajuste fino)
:   Seguir entrenando un modelo ya entrenado con datos específicos para especializarlo. LoRA y QLoRA son técnicas eficientes para hacerlo.

Función de activación
:   Función que transforma la suma ponderada de una neurona (ReLU, sigmoide…) y permite a la red aprender relaciones no lineales.

Función de pérdida (loss)
:   Medida de cuánto se equivoca el modelo. El entrenamiento intenta minimizarla.

GPU
:   Unidad de procesamiento gráfico. Hace miles de operaciones en paralelo y es el hardware principal para entrenar y ejecutar modelos.

IA generativa
:   IA que crea contenido nuevo: texto, imágenes, audio, vídeo o código.

Inferencia
:   Usar un modelo ya entrenado para obtener respuestas o predicciones.

LLM (modelo de lenguaje grande)
:   Red neuronal de tipo Transformer entrenada con enormes cantidades de texto para predecir el siguiente token. Es el motor de ChatGPT, Gemini o Claude.

Machine Learning (aprendizaje automático)
:   Rama de la IA en la que los sistemas aprenden patrones a partir de datos en lugar de seguir reglas escritas a mano.

Modelo
:   Resultado del entrenamiento: un conjunto de parámetros que codifica lo aprendido y permite hacer predicciones.

Modelo de difusión
:   Modelo generativo que aprende a eliminar ruido de una imagen y, partiendo de ruido puro, genera imágenes nuevas.

Multimodal
:   Que trabaja con varios tipos de datos a la vez (texto, imagen, audio, vídeo).

Parámetros (pesos y sesgos)
:   Los números internos de un modelo que se ajustan durante el entrenamiento. Los grandes modelos tienen miles de millones.

Prompt
:   Instrucción o texto que se le da a un modelo generativo.

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

Token
:   Fragmento de texto (una palabra, parte de una palabra o un signo) con el que trabaja un modelo de lenguaje.

TPU
:   Chip de Google diseñado específicamente para cálculos de IA.

Transformer
:   Arquitectura de red neuronal presentada en 2017, basada en el mecanismo de atención. Es la base de los LLM y de muchos modelos de imagen.

VRAM
:   Memoria de la tarjeta gráfica. Determina qué tamaño de modelo cabe en ella.
