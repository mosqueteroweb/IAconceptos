# Prácticas de la segunda parte

Estas son las prácticas evaluables de los módulos 13 a 22. Antes de empezar cualquiera, lee las [normas comunes](#normas-comunes-a-todas-las-practicas): son las mismas para todas.

## Las prácticas

| Práctica | Módulo | Equipo |
|---|---|---|
| [13. El laboratorio de prompts](practica-13.md) | 13. Aplicaciones e ingeniería de prompts | Navegador |
| [14. Tu laboratorio de IA local](practica-14.md) | 14. LM Studio y Ollama | Mac o PC |
| [16. Habilidades y conectores](practica-16.md) | 16. Habilidades y MCP | Mac o PC + navegador |
| [17. Tu agente, tus APIs](practica-17.md) | 15. La API y 17. Agentes | Mac o PC + cuenta gratuita de NVIDIA |
| [18. Un modelo con estilo propio](practica-18.md) | 18. Fine-tuning | Mac o PC (o Colab) |
| [19. Cuantizar y medir](practica-19.md) | 19. Cuantización | Mac o PC, con la terminal |
| [20. Destila tu propio modelo](practica-20.md) | 20. Destilación | Mac o PC |
| [21. Tu nano-modelo](practica-21.md) | 21. Pre-entrenamiento | Mac o PC, con la terminal |
| [22. Proyecto final](practica-22.md) | 22. Crea tu propio modelo | Mac o PC (o Colab) |

## Normas comunes a todas las prácticas

!!! danger "Validación obligatoria en clase"
    **El profesor tiene que ver en clase que tu práctica funciona** antes de que la subas. Primero la enseñas funcionando en el aula; después subes tu entrega. **Un trabajo subido sin haberlo validado antes en clase no se evalúa.** Cada práctica indica qué tendrás que enseñar en la validación.

**Grupos y entregas.** Las prácticas se hacen **en grupo**, en el equipo del grupo. Hay **9 grupos** en cada clase y cada práctica tiene un apartado con lo que le toca a cada uno: pulsa en tu grupo para verlo. Aunque el trabajo sea en grupo, **cada alumno entrega su propia documentación**, escrita por él, aunque los datos y las capturas sean los mismos que los de sus compañeros. En la validación, el profesor puede preguntar a **cualquier** miembro del grupo.

**Cómo están hechas las prácticas.** Cada práctica empieza con un **ejemplo resuelto** paso a paso, con resultados reales. Después vienen las tareas: haces lo mismo que en el ejemplo, pero con **los datos de tu grupo** y con alguna tarea que el ejemplo no tiene. Copiar los resultados del ejemplo no sirve: no son los de tu grupo ni los de tu equipo.

**Equipos del aula.** Las prácticas están pensadas para los dos tipos de equipo del aula: **Mac mini M4 con 16 GB** y **PC con tarjeta NVIDIA RTX 5060 Ti de 16 GB**. Indica siempre en tu entrega en qué equipo has trabajado. Cuando las instrucciones cambian según el equipo, verás dos pestañas: **Mac** y **PC (Windows)**. Los ejemplos resueltos se hicieron en un Mac con chip M2 Pro: las cifras de tu equipo serán distintas.

**Evidencias, no solo respuestas.** Se evalúa **lo que habéis hecho y medido**, no un texto bien escrito. Por eso cada práctica pide:

- **Capturas de pantalla completas**, en las que se vean la hora y la fecha del sistema (en Mac, la barra superior; en Windows, la barra de tareas). No recortes las capturas.
- **Los archivos que generéis**: conjuntos de datos, configuraciones, resultados de la terminal…
- **Cifras de vuestro equipo**: velocidades, tamaños y pérdidas que solo existen porque habéis hecho el experimento.

**Uso de IA.** Puedes usar asistentes de IA para ayudarte (al fin y al cabo, es un curso de IA), pero **decláralo**: en un apartado final, indica qué herramienta has usado, para qué y qué has corregido de lo que te dio. Las preguntas de las prácticas se refieren a **vuestros resultados**: una IA no puede contestarlas sin ellos.

**Los modelos se prueban en LM Studio.** Todos los modelos que creéis o transforméis (prácticas 18 a 22) se importan y se prueban en **LM Studio**. Las capturas de **Library** y del chat con vuestro modelo forman parte de la entrega.

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

## Cómo se entrega

Cada alumno sube a EducaMadrid **un solo archivo ZIP**, **después** de la validación en clase. Se llama con el número de la práctica y tu nombre, por ejemplo `P18-Garcia-Lopez-Ana.zip`, y contiene:

1. **Un PDF** con el mismo nombre (`P18-Garcia-Lopez-Ana.pdf`) y solo dos cosas:
    - una **portada** con tu **nombre y apellidos**, el **título de la práctica**, el **nombre del módulo** y tu **grupo** (del 1 al 9);
    - el **enlace** a la página de esa práctica en **tu web de GitHub Pages**.
2. **Los archivos** que pide la práctica en su apartado *Entregables*, en «En el ZIP»: conjuntos de datos, configuraciones, resultados de la terminal…

**En tu web va toda la documentación:** los apartados numerados como en el enunciado, las tablas, las capturas, las respuestas, las conclusiones y el apartado de uso de IA. Una página por práctica, en un repositorio **público** de GitHub.

!!! warning "Tus datos, solo en la portada del PDF"
    La web es pública: no escribas en ella tu nombre ni tus apellidos, ni los de tus compañeros. Revisa también las capturas antes de publicarlas: que no se vea ninguna **clave** ni el nombre de usuario del equipo.

!!! info "No cambies la página después de entregar"
    El profesor comprueba en el historial del repositorio la fecha del último cambio de cada página. Si una página se ha modificado después de la entrega, se evalúa la versión entregada o no se evalúa. Si tienes que corregir algo, pregunta antes al profesor.
