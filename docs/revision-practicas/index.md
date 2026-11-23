---
search:
  exclude: true
hide:
  - navigation
---

# Prácticas de la segunda parte (borrador para revisión)

!!! warning "Página de revisión"
    Estas páginas no están enlazadas desde la web del curso. Contienen los enunciados de las prácticas de los módulos 13 a 22 (salvo la de agentes), pendientes de revisión antes de publicarlos.

## Las prácticas

| Práctica | Módulo | Equipo |
|---|---|---|
| [13. El laboratorio de prompts](practica-13.md) | 13. Aplicaciones e ingeniería de prompts | Navegador |
| [14. Tu laboratorio de IA local](practica-14.md) | 14. LM Studio y Ollama | Mac o PC |
| [15. Tu agente, tus APIs](practica-15.md) | 15. La API | Mac o PC + cuenta gratuita de NVIDIA |
| [16. Habilidades y conectores](practica-16.md) | 16. Habilidades y MCP | Mac o PC + navegador |
| [18. Un modelo con estilo propio](practica-18.md) | 18. Fine-tuning | Mac o PC (o Colab) |
| [19. Cuantizar y medir](practica-19.md) | 19. Cuantización | Mac o PC, con la terminal |
| [20. Destila tu propio modelo](practica-20.md) | 20. Destilación | Mac o PC |
| [21. Tu nano-modelo](practica-21.md) | 21. Pre-entrenamiento | Mac o PC, con la terminal |
| [22. Proyecto final](practica-22.md) | 22. Crea tu propio modelo | Mac o PC (o Colab) |

## Normas comunes a todas las prácticas

**Equipos del aula.** Las prácticas están pensadas para los dos tipos de equipo del aula: **Mac mini M4 con 16 GB** y **PC con tarjeta NVIDIA RTX 5060 Ti de 16 GB**. Indica siempre en tu entrega en qué equipo has trabajado. Cuando las instrucciones cambian según el equipo, verás dos pestañas: **Mac** y **PC (Windows)**.

**Tu variante.** Casi todas las prácticas tienen **variantes**. Te corresponde la que indica tu **número de lista**: si hay 8 variantes y eres el número 11, te toca la 3 (11 − 8 = 3). Si se te acaban, vuelve a empezar. Una entrega con otra variante no se evalúa.

**Evidencias, no solo respuestas.** En estas prácticas se evalúa **lo que has hecho y lo que has medido tú**, no un texto bien escrito. Por eso cada práctica pide:

- **Capturas de pantalla completas**, en las que se vean la hora y la fecha del sistema (en Mac, la barra superior; en Windows, la barra de tareas). No recortes las capturas.
- **Los archivos que generes**: conjuntos de datos, configuraciones, resultados de la terminal, archivos de los modelos…
- **Cifras de tu propio equipo**: velocidades, tamaños y pérdidas que solo existen porque tú has hecho el experimento. Las cifras de otro equipo o inventadas se notan.
- **Claves de clase**: algunas prácticas usan una **palabra clave de la sesión** que se dice en el aula y que no está publicada en ningún sitio.

**Uso de IA.** Puedes usar asistentes de IA para ayudarte (al fin y al cabo, es un curso de IA), pero **decláralo**: en un apartado final, indica qué herramienta has usado, para qué y qué has corregido de lo que te dio. Las preguntas de las prácticas se refieren a **tus resultados**: una IA no puede contestarlas sin ellos.

**Los modelos se prueban en LM Studio.** Todos los modelos que crees o transformes (prácticas 18 a 22) se importan y se prueban en **LM Studio**, en tu equipo. Las capturas de **Library** y del chat con tu modelo forman parte de la entrega.

**La terminal.** Varias prácticas usan la terminal. En **Mac** es la aplicación **Terminal** (Cmd + espacio y escribe «Terminal»). En **Windows** es **PowerShell** (menú Inicio y escribe «PowerShell»). Copia las órdenes con el botón de copiar de cada recuadro y pégalas tal cual. Muchas prácticas usan **uv**, un programa que descarga e instala lo que necesita cada *script* de Python sin que tengas que instalar Python a mano:

=== "Mac"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "PC (Windows)"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

Cierra la terminal y vuelve a abrirla después de instalarlo. Comprueba que funciona con `uv --version`.

**Defensa.** Cualquier práctica puede incluir una **defensa oral de 3 a 5 minutos** en el aula, delante de tu equipo: tendrás que repetir una parte del experimento o explicar una decisión. La nota de la práctica puede depender de esa defensa.

**Formato de entrega.** Un único documento (PDF o enlace a un documento compartido) con los apartados numerados como en el enunciado, más los archivos que se pidan, en una carpeta comprimida con tu nombre y el número de la práctica.
