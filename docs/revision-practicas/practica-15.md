---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 15. Tu agente, tus APIs

**Módulo:** [15. Usar modelos desde tus programas: la API](../15-api.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** conectar un **agente** de verdad a dos APIs distintas, una **local** (LM Studio u Ollama, en tu equipo) y una **externa** (gratuita, en la nube), entender qué datos necesita cada conexión (dirección, modelo y clave), ver qué viaja por la API y comparar los dos modelos con la misma tarea.

**Qué vas a usar:**

- **Un agente**, a elegir: [OpenCode](https://opencode.ai/) (de código abierto, pensado para programar y trabajar con archivos) o [Hermes Agent](https://hermes-agent.nousresearch.com/) (de Nous Research, de código abierto, un asistente personal que aprende de lo que hace). Los dos se usan desde la terminal y los dos saben leer y escribir archivos y ejecutar programas.
- **Una API local**: el servidor de **LM Studio** (como en el módulo 14) o el de **Ollama**.
- **Una API externa gratuita**: la de **NVIDIA** ([build.nvidia.com](https://build.nvidia.com/)), que da acceso gratuito a modelos abiertos grandes con una cuenta de desarrollador.

## Tu variante (el asistente que vas a crear)

| N.º | Asistente |
|---|---|
| 1 | Guía de un museo de ciencias inventado, con nombre y tres salas. |
| 2 | Conserje virtual del instituto: horarios, aulas y normas. |
| 3 | Asistente de una biblioteca municipal: préstamos, horarios y actividades. |
| 4 | Recepcionista de un hotel rural inventado. |
| 5 | Entrenador de un gimnasio inventado que solo habla de ejercicio y alimentación sana. |
| 6 | Asistente de una tienda de bicicletas eléctricas inventada. |
| 7 | Guía turístico de tu localidad. |
| 8 | Asistente de una clínica veterinaria inventada. |

## Antes de empezar: qué modelo cargar

Un agente envía al modelo, en cada petición, unas instrucciones muy largas y la descripción de todas sus herramientas. Por eso necesita un **contexto grande**: **Hermes exige al menos 64 000 tokens** y OpenCode funciona bien a partir de 32 000. Además, el modelo debe saber **usar herramientas** (en LM Studio llevan el icono del martillo).

| Equipo | Modelo recomendado en LM Studio | En Ollama | Contexto |
|---|---|---|---|
| Mac mini M4 16 GB | **Gemma 4 E2B** (unos 4 GB con 64 000 de contexto) o Gemma 4 E4B | `gemma4:e2b` o `gemma4:e4b` | 65 536 |
| PC RTX 5060 Ti 16 GB | **Gemma 4 E4B** o **gpt-oss-20b** | `gemma4:e4b` o `gpt-oss:20b` | 65 536 |

## Tareas

### Parte A. La API local

1. **El servidor.** Elige **una** de las dos opciones y captura la pantalla cuando funcione.

    === "LM Studio"

        1. Descarga el modelo recomendado para tu equipo (**Model Search**).
        2. Cárgalo con **Manually choose model load parameters** activado y pon **Context Length** en **65536**. Fíjate en la memoria estimada.
        3. Ve a **Model Server** y activa el interruptor **Status** hasta que diga *Running*. La dirección de la API es `http://localhost:1234/v1`.

    === "Ollama"

        1. Instala Ollama desde [ollama.com](https://ollama.com/download) y ábrelo.
        2. En los ajustes de la aplicación de Ollama (*Settings*), sube **Context length** a **64k**. Por defecto, con menos de 24 GB de memoria, Ollama usa solo 4 096 tokens y los agentes no funcionan.
        3. Descarga el modelo en la terminal, por ejemplo: `ollama pull gemma4:e2b`
        4. La dirección de la API es `http://localhost:11434/v1`.

2. **Habla con la API sin intermediarios.** Antes de usar el agente, comprueba qué modelos ofrece tu servidor. Copia esta orden en la terminal (con Ollama, cambia `1234` por `11434`):

    === "Mac"

        ```bash
        curl http://localhost:1234/v1/models
        ```

    === "PC (Windows)"

        ```powershell
        curl.exe http://localhost:1234/v1/models
        ```

    La respuesta es un texto en JSON. Busca el **identificador** (`"id"`) de tu modelo y anótalo: es el nombre con el que lo pedirá el agente.

3. **Instala el agente** que hayas elegido:

    === "OpenCode"

        - **Mac:** `brew install opencode` (si no tienes Homebrew, `curl -fsSL https://opencode.ai/install | bash`).
        - **Windows:** con Node.js instalado, `npm install -g @opencode/cli` en PowerShell. También puedes descargar la aplicación de escritorio de [opencode.ai/download](https://opencode.ai/download). Ojo: el paquete antiguo `opencode-ai` instala la versión 1, que funciona de otra forma.
        - Comprueba la instalación con `opencode --version`.

    === "Hermes Agent"

        - **Mac:** `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
        - **Windows (PowerShell):** `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`
        - También hay aplicación de escritorio para Mac (con chip Apple) y Windows en su [web](https://hermes-agent.nousresearch.com/).
        - Comprueba la instalación con `hermes --version`. La primera vez, el instalador te hará unas preguntas de configuración; si te pide un proveedor, elige el de la tarea 4.

4. **Conecta el agente a tu API local.**

    === "OpenCode"

        OpenCode **detecta solo** LM Studio y Ollama si están en marcha. Crea una carpeta `practica15`, entra en ella con la terminal (`cd`) y escribe `opencode`. Dentro, escribe `/models` y elige tu modelo, que aparecerá como `lmstudio/…` u `ollama/…`.

    === "Hermes Agent"

        Escribe `hermes model` en la terminal.

        - **LM Studio:** elige *LM Studio*, pulsa Intro para aceptar `http://localhost:1234/v1` y elige tu modelo.
        - **Ollama:** elige *Custom endpoint*, escribe `http://localhost:11434/v1`, deja la clave en blanco y escribe el nombre del modelo (por ejemplo, `gemma4:e2b`).

        Comprueba la configuración con `hermes config show`. Después, crea una carpeta `practica15`, entra en ella con la terminal y escribe `hermes`.

    Captura la pantalla en la que se vea el agente con tu modelo local elegido.

5. **Dale personalidad.** Los dos agentes leen un archivo llamado **`AGENTS.md`** de la carpeta en la que trabajan: es su *system prompt*. Crea `AGENTS.md` en `practica15` con las instrucciones de **tu asistente**: nombre, tono, **tres datos concretos** (teléfono, horario, precios…) y la **palabra clave de la sesión** que se dirá en clase, que el asistente debe escribir al final de cada respuesta. Vuelve a abrir el agente y pregúntale «¿Quién eres?».
6. **Una tarea con archivos.** Copia en la carpeta el archivo [`reservas.csv`](#material-el-archivo-reservascsv) y pide al agente, con estas mismas palabras:

    > Lee reservas.csv y crea informe.md con: 1) el número de reservas confirmadas y el total de personas de esas reservas; 2) los nombres de las reservas canceladas; 3) el día con más personas confirmadas; 4) los grupos de 10 o más personas que están confirmados.

    Cada vez que el agente quiera leer o escribir un archivo te pedirá **permiso**: captura esas ventanas. Después, **comprueba tú el informe** contando a mano en el CSV. ¿Hay algún error?

7. **Que lo calcule con un programa.** Pide al agente: «Comprueba las cifras del informe escribiendo y ejecutando un pequeño programa en Python que lea reservas.csv, y corrige el informe si hace falta». Captura el programa que escribe y el resultado. ¿Coinciden las cifras ahora? ¿Por qué un modelo de lenguaje se equivoca al sumar, pero acierta si escribe un programa?
8. **Bajo el capó** (con LM Studio; si usas Ollama, carga el mismo modelo en LM Studio para este apartado).
    1. En LM Studio, abre **Developer** (o **Model Server**) y mira los registros (**Logs**) mientras el agente trabaja.
    2. Escribe al agente solo «Hola». Busca en el registro la petición y anota cuántos **tokens de entrada** ha enviado el agente (*prompt tokens*).
    3. Haz la misma pregunta directamente a la API, sin agente:

        === "Mac"

            ```bash
            curl http://localhost:1234/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "google/gemma-4-e2b", "messages": [{"role": "user", "content": "Hola"}]}'
            ```

        === "PC (Windows)"

            ```powershell
            curl.exe http://localhost:1234/v1/chat/completions -H "Content-Type: application/json" -d '{\"model\": \"google/gemma-4-e2b\", \"messages\": [{\"role\": \"user\", \"content\": \"Hola\"}]}'
            ```

        Cambia `google/gemma-4-e2b` por el identificador de tu modelo. En la respuesta, busca `"usage"` y anota `prompt_tokens`.

    4. Sigue la conversación con el agente dos turnos más y anota los tokens de entrada de cada petición.

    ¿Por qué un simple «Hola» le cuesta al agente miles de tokens? ¿Por qué crecen los tokens de entrada en cada turno, si la API **no guarda memoria** de las peticiones anteriores?

### Parte B. Una API externa

9. **Tu clave de NVIDIA.**
    1. Entra en [build.nvidia.com](https://build.nvidia.com/) y crea una cuenta gratuita (programa de desarrolladores de NVIDIA).
    2. En tu perfil, ve a **API Keys** y genera una clave. Empieza por `nvapi-`. **Cópiala en un lugar seguro**: no la verás otra vez.
    3. La API de NVIDIA es compatible con la de OpenAI. Su dirección es `https://integrate.api.nvidia.com/v1`.

    !!! danger "Tu clave es como una contraseña"
        No la pegues en `AGENTS.md`, en el informe, en un chat ni en ninguna captura. Si se te escapa, bórrala en la web de NVIDIA y crea otra. Al terminar el curso, bórrala.

10. **Conecta el agente a NVIDIA.**

    === "OpenCode"

        Dentro de OpenCode, escribe `/connect`, elige **Nvidia** y pega tu clave. Después, `/models` y elige un modelo de NVIDIA, por ejemplo `nvidia/nemotron-3.5-lightning-30b-a3b`.

    === "Hermes Agent"

        Hermes lee las claves del archivo **`.env`** de su carpeta (`~/.hermes/.env` en Mac; `C:\Users\tu_usuario\.hermes\.env` en Windows). Ábrelo con un editor de texto y añade una línea con tu clave:

        ```text
        NVIDIA_API_KEY=nvapi-tu_clave
        ```

        Guarda el archivo, ejecuta `hermes model`, elige **NVIDIA Build** y un modelo, por ejemplo `nvidia/nemotron-3.5-lightning-30b-a3b`. También puedes usarlo solo para una conversación: `hermes chat --provider nvidia -m nvidia/nemotron-3.5-lightning-30b-a3b`.

    Puedes elegir otro modelo de la lista de NVIDIA, pero anota cuál y por qué.

11. **La misma tarea.** Borra `informe.md` y repite las tareas 5, 6 y 7 con el modelo de NVIDIA, con las mismas palabras.
12. **Comparación.** Haz una tabla con los dos modelos: nombre, dónde se ejecuta, tiempo que tardó la tarea 6, número de errores del informe antes y después de la tarea 7, si cumplió la personalidad de `AGENTS.md` y si dijo la palabra clave. Después, responde: ¿qué datos tuyos han salido de tu ordenador en la parte B? ¿Qué límites tiene la API gratuita? ¿Cuándo usarías cada una?

!!! tip "Si no puedes usar NVIDIA"
    Otras APIs con modelos gratuitos y compatibles con OpenAI: [OpenRouter](https://openrouter.ai/) (modelos terminados en `:free`) o la API de [Google Gemini](https://aistudio.google.com/) (nivel gratuito). Los dos agentes las admiten. Indica en la entrega cuál has usado.

**Opcional (+1 punto):** repite la parte A con el **otro** servidor local (LM Studio si usaste Ollama, o al revés) o con el **otro** agente, y compara.

## Material: el archivo `reservas.csv`

Crea un archivo llamado `reservas.csv` en la carpeta `practica15`, copia dentro este texto y guárdalo (en Mac con TextEdit en modo de texto normal; en Windows con el Bloc de notas). Son las reservas de tu negocio inventado.

```text
fecha,nombre,personas,estado
2027-02-03,Lucía Ferrer,4,confirmada
2027-02-03,Grupo IES Las Lomas,26,confirmada
2027-02-04,Andrés Molina,2,cancelada
2027-02-05,Familia Ortega,5,confirmada
2027-02-05,Carmen Vidal,1,pendiente
2027-02-06,Club Senderista Peñarrubia,18,confirmada
2027-02-06,Javier Soler,3,cancelada
2027-02-06,Asociación Vecinal El Prado,12,confirmada
2027-02-07,Marta Casado,2,confirmada
2027-02-07,Colegio San Isidro,31,pendiente
2027-02-08,Rubén Prieto,6,confirmada
2027-02-08,Elena Sanz,2,cancelada
2027-02-09,Familia Gil,4,confirmada
2027-02-09,Óscar Delgado,1,confirmada
```

## Entregables

- Tu `AGENTS.md`.
- Los dos `informe.md` (modelo local y modelo de NVIDIA), antes y después de la corrección, y los programas que escribió el agente.
- Tu recuento a mano del CSV.
- Capturas completas: el servidor local en marcha, la respuesta de `/v1/models`, el agente con cada modelo, las ventanas de permiso y los registros de LM Studio con los tokens.
- La tabla de tokens del apartado 8 con tu explicación.
- La tabla comparativa del apartado 12 y tus respuestas (máximo 250 palabras).
- **Ninguna clave**: si aparece en una captura, tápala.

**Defensa posible:** el profesor te dará un dato nuevo para tu asistente y tendrás que añadirlo a `AGENTS.md` y comprobarlo en directo, o te pedirá que cambies el agente de modelo local a externo delante de él.
