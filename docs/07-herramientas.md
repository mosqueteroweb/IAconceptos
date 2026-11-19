# 7. Las herramientas del oficio

!!! abstract "En este módulo"
    - Por qué Python es el lenguaje de la IA.
    - Las librerías clave, explicadas sin código.
    - Dónde se entrena todo esto: la nube y los cuadernos (Colab y alternativas).
    - Herramientas sin código y para usar IA en tu propio ordenador.

## 1. El lenguaje: ¿por qué Python es el rey de la IA?

En IA y ciencia de datos, un lenguaje se ha coronado como el rey indiscutible: **Python**. Existen alternativas (R para estadística, C++ y CUDA para las partes que exigen máxima velocidad, Julia…), pero la inmensa mayoría de la investigación, la enseñanza y el desarrollo en IA se hace en Python. ¿Por qué?

1. **Sencillez y legibilidad.** Su sintaxis es limpia y se parece mucho al inglés, lo que facilita aprender y permite a investigadores centrarse en el problema (el modelo) en lugar de pelearse con el lenguaje.
2. **Un ecosistema gigantesco de librerías.** NumPy, Pandas, Scikit-learn, PyTorch… ofrecen bloques ya hechos para casi cualquier tarea. Nadie tiene que reinventar la rueda.
3. **Una comunidad enorme.** Infinidad de documentación, tutoriales, foros y cursos. Si te atascas, casi seguro que alguien ya resolvió el mismo problema.
4. **Versatilidad.** Python sirve también para webs, automatización o análisis de datos, lo que facilita integrar los modelos en aplicaciones reales.

!!! info "¿Python es lento?"
    Python por sí mismo es relativamente lento. El truco es que las librerías de IA están escritas por dentro en **C, C++ y CUDA** (muy rápidos) y Python actúa como un «mando a distancia» cómodo. Lo pesado lo hace la GPU.

!!! tip "¿Hay que saber programar para usar IA?"
    Para **usar** IA, no: chatbots, generadores de imágenes y herramientas como Teachable Machine no requieren código. Además, los asistentes de IA actuales ayudan mucho a escribir y entender programas. Para **crear o adaptar** modelos sí conviene saber algo de Python, y es un lenguaje muy amable para empezar.

## 2. Librerías clave (explicadas sin código)

Una **librería** es un conjunto de código ya escrito que se puede reutilizar. No necesitas saber usarlas, pero sí qué problema resuelve cada una:

| Librería | Para qué sirve | Analogía |
|---|---|---|
| **NumPy** | Cálculo numérico con tablas de números (matrices) a gran velocidad. Es la base de casi todas las demás. | La calculadora científica |
| **Pandas** | Cargar, limpiar, transformar y explorar datos en tablas (los *DataFrames*). | Una hoja de cálculo con superpoderes |
| **Matplotlib / Seaborn** | Gráficos y visualizaciones. | El papel milimetrado |
| **Scikit-learn** | Machine Learning clásico: clasificación, regresión, clustering, evaluación de modelos. | La caja de herramientas |
| **PyTorch** | Deep Learning: construir y entrenar redes neuronales. | El taller de motores |
| **TensorFlow / Keras** | Deep Learning, con buenas herramientas para llevar modelos a producción y a móviles. | Otro taller de motores |
| **Hugging Face Transformers** | Descargar y usar miles de modelos ya entrenados (texto, imagen, audio). | Una biblioteca de modelos listos para usar |

**Pandas** es la «refinería» de los datos: antes de entrenar, los datos deben cargarse, limpiarse (quitar duplicados, rellenar huecos), transformarse y explorarse. Se dice que hasta el 80 % del trabajo de un científico de datos es preparar datos.

**Scikit-learn** es la referencia para el **Machine Learning tradicional** del [módulo 4](04-machine-learning.md). Su gran virtud es la coherencia: todos los modelos se usan igual, así que probar diez algoritmos distintos cuesta muy poco.

**PyTorch y TensorFlow** son las dos grandes librerías de **Deep Learning**:

- **PyTorch**, creada por Meta (Facebook) en 2016 y gestionada hoy por la PyTorch Foundation (Linux Foundation), es flexible e intuitiva. Domina la investigación y el entrenamiento de grandes modelos de lenguaje.
- **TensorFlow**, de Google (2015), destaca por sus herramientas para poner modelos en producción, en móviles y en navegadores, y por **Keras**, una interfaz muy sencilla. Su uso en investigación ha bajado frente a PyTorch. Google utiliza también **JAX** para sus modelos más grandes (como Gemini).

## 3. Plataformas en la nube: ¿dónde se entrena todo esto?

Entrenar un modelo de Deep Learning requiere muchísimo cálculo y hardware específico (GPUs, [módulo 9](09-hardware.md)), algo que pocas personas tienen en casa. La solución es **la nube**: Google Cloud, Amazon Web Services (AWS) y Microsoft Azure, entre otros, alquilan **por horas** servidores con las GPUs más potentes o con chips específicos de IA (como las **TPU** de Google). Esto democratiza el acceso: no hace falta comprar equipos carísimos.

### Google Colab

Para empezar existe una herramienta gratuita perfecta: **Google Colaboratory (Colab)**. Ofrece **cuadernos** (*notebooks*) que funcionan en el navegador y dan **acceso gratuito, con límites, a GPUs y TPUs**. Sin instalar nada ni pagar, se puede ejecutar Python y entrenar modelos relativamente complejos.

Un cuaderno mezcla **celdas de texto** (explicaciones, como en este curso) y **celdas de código** que se ejecutan de una en una, mostrando el resultado debajo. Es ideal para experimentar, enseñar y compartir: muchísimos tutoriales y proyectos de IA se publican como cuadernos de Colab que cualquiera puede abrir y ejecutar con un clic.

!!! warning "Limitaciones de la versión gratuita"
    Las sesiones se cierran tras un tiempo de inactividad (y como máximo unas horas) y los archivos se **borran al terminar** (conviene guardar en Google Drive). La GPU disponible y el tiempo de uso varían según la demanda. Existen planes de pago (Colab Pro) con más recursos.

### Alternativas a Google Colab

- **Kaggle Notebooks** (Google). Kaggle es famosa por sus **competiciones** de ciencia de datos y sus miles de **conjuntos de datos** públicos, que se usan desde el cuaderno sin descargarlos. Ofrece GPU y TPU gratuitas con una cuota semanal (unas 30 horas de GPU) y permite aprender viendo los cuadernos públicos de otros participantes. *Ideal para:* practicar con datos reales y competiciones.
- **Amazon SageMaker Studio Lab** (AWS). Gratuito y **sin tarjeta de crédito**, con **15 GB de almacenamiento persistente** (tu trabajo se conserva entre sesiones) y entorno JupyterLab completo con terminal. Las sesiones con GPU están limitadas a unas pocas horas al día. *Ideal para:* proyectos que necesitan guardar archivos.
- **Deepnote.** Cuadernos enfocados a la **colaboración en tiempo real** («un Google Docs para ciencia de datos»), con integraciones con bases de datos y fácil publicación de resultados para personas no técnicas. *Ideal para:* trabajo en equipo.
- **Databricks Free Edition.** Desde 2025 sustituye a la antigua *Community Edition*. Plataforma profesional de Big Data basada en **Apache Spark**. *Ideal para:* orientarse a la ingeniería de datos.

| | Google Colab | Kaggle Notebooks | SageMaker Studio Lab | Deepnote |
|---|---|---|---|---|
| **Punto fuerte** | Sencillez, integración con Drive | Datos y comunidad | Almacenamiento persistente | Colaboración |
| **GPU gratuita** | Sí, con límites variables | Sí, cuota semanal | Sí, sesiones cortas | Limitada |
| **Almacenamiento** | Temporal (usar Drive) | Temporal + datasets | Persistente (15 GB) | Persistente |
| **Ideal para** | Aprender y prototipar | Competiciones | Proyectos largos | Equipos |

!!! note "Los límites cambian"
    Las cuotas gratuitas de estas plataformas se modifican a menudo. Consulta siempre la web oficial antes de planificar una práctica.

## 4. Sin código y en tu propio ordenador

No todo es programar en la nube. Algunas herramientas útiles para clase:

- **Sin código:** [Teachable Machine](https://teachablemachine.withgoogle.com/) (entrenar clasificadores de imagen, sonido o postura), [TensorFlow Playground](https://playground.tensorflow.org/) (redes neuronales), [Hugging Face Spaces](https://huggingface.co/spaces) (miles de demos de modelos para probar en el navegador).
- **IA en local:** [Ollama](https://ollama.com/) y [LM Studio](https://lmstudio.ai/) permiten **descargar y ejecutar modelos de lenguaje abiertos** (Llama, Mistral, Qwen, Gemma…) en tu propio ordenador, sin conexión y sin enviar tus datos a nadie. Un portátil moderno con 16 GB de memoria ya mueve modelos pequeños. Enlaza con los módulos de [hardware](09-hardware.md) y [software](10-software.md).

## Para ampliar

<div class="recursos" markdown>

**Artículos y documentación**

- [¿Qué es Python?](https://aws.amazon.com/es/what-is/python/) (AWS).
- [El tutorial de Python](https://docs.python.org/es/3/tutorial/) (documentación oficial en español).
- Webs oficiales: [NumPy](https://numpy.org/es/), [Pandas](https://pandas.pydata.org/), [Scikit-learn](https://scikit-learn.org/stable/), [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/?hl=es-419).
- Plataformas: [Google Colab](https://colab.research.google.com/), [Kaggle](https://www.kaggle.com/code), [SageMaker Studio Lab](https://studiolab.sagemaker.aws/), [Deepnote](https://deepnote.com/), [Databricks Free Edition](https://www.databricks.com/learn/free-edition).

**Vídeos**

- :material-youtube: [Python en 8 minutos](https://www.youtube.com/watch?v=PtBHnMMRI0E) (MoureDev, 10 min).
- :material-youtube: [Introducción a Google Colab para principiantes](https://www.youtube.com/watch?v=9g61bnipcSs) (EvoAcademy, 19 min).
- :material-youtube: [Introducción a Google Colab, una completa guía](https://www.youtube.com/watch?v=8VFYs3Ot_aA) (DATACLOUDER, 16 min).

**Cursos y libros para seguir aprendiendo**

- [Aprende a programar en Python desde cero](https://www.freecodecamp.org/espanol/news/aprende-a-programar-en-python-desde-cero-curso-completo-gratis/) (freeCodeCamp en español, curso completo gratuito).
- [Curso intensivo de Machine Learning](https://developers.google.com/machine-learning/crash-course?hl=es-419) (Google, gratuito).
- [Curso de LLM de Hugging Face](https://huggingface.co/learn/llm-course/es/chapter1/1) (en español, gratuito).
- [Especialización en Deep Learning](https://www.coursera.org/specializations/deep-learning) (Andrew Ng, DeepLearning.AI en Coursera; se puede auditar gratis).
- [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) (Andrej Karpathy, en inglés): construye desde cero una red neuronal y un pequeño GPT. Para quien ya programa.
- Libro: *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow* (Aurélien Géron, O'Reilly). Sus cuadernos de ejemplo son gratuitos en [GitHub](https://github.com/ageron/handson-ml3).

</div>
