---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 15. Tu agente, tus APIs

**Módulo:** [15. Usar modelos desde tus programas: la API](../15-api.md) · [Normas comunes de las prácticas](index.md)

!!! danger "Validación obligatoria en clase"
    El profesor tiene que ver en clase vuestro trabajo funcionando **antes** de que lo subas. Un trabajo subido sin haberlo validado antes en clase no se evalúa. Lo que tendréis que enseñar está en el apartado [Validación en clase](#validacion-en-clase).

**Objetivo:** conectar un **agente** de verdad a dos APIs distintas, una **local** (LM Studio u Ollama, en tu equipo) y una **externa** (gratuita, en la nube), entender qué datos necesita cada conexión (dirección, modelo y clave), ver qué viaja por la API y comparar los dos modelos con la misma tarea.

**Qué vas a usar:**

- **Un agente**, a elegir: [OpenCode](https://opencode.ai/) (de código abierto, pensado para programar y trabajar con archivos) o [Hermes Agent](https://hermes-agent.nousresearch.com/) (de Nous Research, de código abierto, un asistente personal que aprende de lo que hace). Los dos se usan desde la terminal y los dos saben leer y escribir archivos y ejecutar programas.
- **Una API local**: el servidor de **LM Studio** (como en el módulo 14) o el de **Ollama**.
- **Una API externa gratuita**: la de **NVIDIA** ([build.nvidia.com](https://build.nvidia.com/)), que da acceso gratuito a modelos abiertos grandes con una cuenta de desarrollador.

## Ejemplo resuelto

**Asistente del ejemplo:** Ondina, la asistente de una piscina municipal. **Agente:** OpenCode 2.3. **API local:** LM Studio con Gemma 4 E2B (contexto 65 536). **API externa:** NVIDIA con `nvidia/nemotron-3.5-lightning-30b-a3b`. Equipo: Mac con chip M2 Pro.

**1-2. Servidor y modelos.** Cargamos Gemma 4 E2B con 65 536 de contexto (LM Studio estimó 4,1 GB), pusimos el servidor en *Running* y `curl http://localhost:1234/v1/models` devolvió, entre otros, `"id": "google/gemma-4-e2b"`.

**3-4. Agente conectado.** Con `brew install opencode`, y dentro de la carpeta `practica15`, `opencode` → `/models`: el modelo aparecía como `lmstudio/google/gemma-4-e2b`, sin configurar nada.

**5. Personalidad.** Este fue nuestro `AGENTS.md`:

```markdown
# Instrucciones
Eres Ondina, la asistente de la Piscina Municipal Cubierta de Valdemora del Río.
Hablas en español, de tú, de forma breve y amable.
Datos que debes conocer:
- Teléfono de recepción: 912 555 310.
- Horario: de lunes a viernes, de 7.00 a 22.00 h; sábados, de 9.00 a 20.00 h; domingos, de 9.00 a 14.00 h.
- Baño libre: 4,20 €; bono de 10 baños: 35 €.
Termina SIEMPRE cada respuesta con esta frase: «Para cualquier duda, llama a recepción: 912 555 310».
```

A «¿Quién eres y a qué hora abrís el sábado?» respondió: «Abrimos los sábados de 9:00 a 20:00 h. Para cualquier duda, llama a recepción: 912 555 310». Cumplió el horario y la frase final, pero **no se presentó** y escribió «9:00» en lugar de «9.00». Lo repetimos y pasó lo mismo.

**6. Tarea con archivos.** Con [el `reservas.csv` del ejemplo](#el-reservascsv-del-ejemplo) y la petición exacta de la tarea 6, el agente pidió permiso para leer el CSV y para crear `informe.md`. Lo comprobamos a mano: 9 reservas confirmadas, **78 personas**, tres canceladas (Andrés Molina, Javier Soler y Elena Sanz), **empate** entre el 3 y el 6 de febrero con 30 personas, y tres grupos de 10 o más confirmados. Esta vez Gemma acertó todo. En otra prueba anterior, con la misma petición, había sumado **72** personas: el mismo modelo no siempre da el mismo resultado.

**7. Que lo calcule con un programa.** Aquí se vio la diferencia entre los dos modelos:

- **Gemma 4 E2B** contestó «He corregido el archivo» sin ejecutar **ningún** programa (no apareció ninguna ventana de permiso para la terminal) y **estropeó** el informe: cambió 78 por 72 y añadió el Colegio San Isidro, que está *pendiente*. Moraleja: si el agente dice que ha comprobado algo, mira si de verdad ha usado la herramienta.
- **Nemotron (NVIDIA)** primero intentó ejecutar el código con una herramienta equivocada (dio error), y después ejecutó en la terminal un programa de Python con `python3 -c`. Salida: `Reservas confirmadas: 9`, `Total personas: 78` y el desglose por días. Concluyó: «Los números del informe son correctos».

**8. Bajo el capó.** Con OpenCode y Gemma, el mensaje «Di hola en una palabra» envió a LM Studio **5 723 tokens de entrada** y el modelo generó 156. Son las instrucciones del agente y la descripción de todas sus herramientas, que viajan en **cada** petición. La misma pregunta con `curl`, sin agente, son unos pocos tokens.

**9-12. API externa.** Con la clave de NVIDIA conectada (`/connect` → Nvidia), el mismo `AGENTS.md` y la misma tarea:

| | Gemma 4 E2B (local) | Nemotron 3.5 Lightning (NVIDIA) |
|---|---|---|
| Dónde se ejecuta | En el Mac | En los servidores de NVIDIA |
| Tiempo de la tarea 6 | unos 35 s | unos 10 s |
| Errores en el informe (tarea 6) | 0 (en otra prueba, 1) | 0 |
| Comprobación con programa (tarea 7) | No ejecutó nada y lo estropeó | Ejecutó Python y confirmó |
| Datos que salen del ordenador | Ninguno | El CSV y las instrucciones |

## El `reservas.csv` del ejemplo

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

## Vuestra práctica

Haced lo mismo que en el ejemplo con **el asistente, el agente, el modelo de NVIDIA y el `reservas.csv` de vuestro grupo** (están en [vuestra tarjeta](#lo-especifico-de-cada-grupo)).

### Antes de empezar: qué modelo cargar

Un agente envía al modelo, en cada petición, unas instrucciones muy largas y la descripción de todas sus herramientas. Por eso necesita un **contexto grande**: **Hermes exige al menos 64 000 tokens** y OpenCode funciona bien a partir de 32 000. Además, el modelo debe saber **usar herramientas** (en LM Studio llevan el icono del martillo).

| Equipo | Modelo recomendado en LM Studio | En Ollama | Contexto |
|---|---|---|---|
| Mac mini M4 16 GB | **Gemma 4 E2B** (unos 4 GB con 64 000 de contexto) o Gemma 4 E4B | `gemma4:e2b` o `gemma4:e4b` | 65 536 |
| PC RTX 5060 Ti 16 GB | **Gemma 4 E4B** o **gpt-oss-20b** | `gemma4:e4b` o `gpt-oss:20b` | 65 536 |

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

3. **Instala el agente** de vuestro grupo:

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

5. **Dale personalidad.** Los dos agentes leen un archivo llamado **`AGENTS.md`** de la carpeta en la que trabajan: es su *system prompt*. Crea `AGENTS.md` en `practica15` con las instrucciones del **asistente de vuestro grupo**: nombre, tono, **tres datos concretos** (teléfono, horario, precios…) y **una frase fija** con la que el asistente debe terminar cada respuesta (por ejemplo, un consejo o el teléfono). Vuelve a abrir el agente y pregúntale «¿Quién eres?».
6. **Una tarea con archivos.** Copia en la carpeta **el `reservas.csv` de vuestra tarjeta** y pide al agente, con estas mismas palabras:

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

10. **Conecta el agente a NVIDIA** y elige **el modelo de vuestra tarjeta**. Si da error con las herramientas, usa `nvidia/nemotron-3.5-lightning-30b-a3b` y explica el error en la entrega.

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
12. **Comparación.** Haz una tabla con los dos modelos: nombre, dónde se ejecuta, tiempo que tardó la tarea 6, número de errores del informe antes y después de la tarea 7, si cumplió la personalidad de `AGENTS.md` y si terminó con la frase fija. Después, responde: ¿qué datos tuyos han salido de tu ordenador en la parte B? ¿Qué límites tiene la API gratuita? ¿Cuándo usarías cada una?

!!! tip "Si no puedes usar NVIDIA"
    Otras APIs con modelos gratuitos y compatibles con OpenAI: [OpenRouter](https://openrouter.ai/) (modelos terminados en `:free`) o la API de [Google Gemini](https://aistudio.google.com/) (nivel gratuito). Los dos agentes las admiten. Indica en la entrega cuál has usado.

**Opcional (+1 punto):** repite la parte A con el **otro** servidor local (LM Studio si usaste Ollama, o al revés) o con el **otro** agente, y compara.

## Lo específico de cada grupo

??? abstract "Grupo 1"
    - **Asistente:** Guía de un museo de ciencias inventado, con nombre y tres salas.
    - **Agente:** OpenCode.
    - **Modelo de NVIDIA:** `nvidia/nemotron-3.5-lightning-30b-a3b`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-03-14,AMPA Río Claro,32,confirmada
        2027-03-14,Academia de Baile Compás,25,confirmada
        2027-03-14,Andrés Molina,2,confirmada
        2027-03-14,Familia Rubio,6,cancelada
        2027-03-14,Hugo Navarro,5,confirmada
        2027-03-14,Paula Romero,5,confirmada
        2027-03-15,Claudia Ramos,5,confirmada
        2027-03-15,Lucía Ferrer,1,cancelada
        2027-03-15,Sara Crespo,2,pendiente
        2027-03-16,Pablo Vega,6,confirmada
        2027-03-18,Familia Iglesias,6,confirmada
        2027-03-18,Rubén Prieto,5,pendiente
        2027-03-20,Asociación Vecinal El Prado,32,pendiente
        2027-03-20,Club Senderista Peñarrubia,32,cancelada
        ```

??? abstract "Grupo 2"
    - **Asistente:** Conserje virtual del instituto: horarios, aulas y normas.
    - **Agente:** Hermes Agent.
    - **Modelo de NVIDIA:** `moonshotai/kimi-k3.1-pro`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-03-03,Andrés Molina,3,confirmada
        2027-03-03,Club de Ajedrez Alfil,14,confirmada
        2027-03-03,Rubén Prieto,6,confirmada
        2027-03-03,Sara Crespo,5,confirmada
        2027-03-04,Daniel Cano,6,confirmada
        2027-03-04,Familia Rubio,2,confirmada
        2027-03-04,Lucía Ferrer,6,confirmada
        2027-03-06,Pablo Vega,4,confirmada
        2027-03-06,Víctor Herrero,3,pendiente
        2027-03-07,Claudia Ramos,5,pendiente
        2027-03-08,Coro Municipal,27,confirmada
        2027-03-09,Asociación Vecinal El Prado,28,confirmada
        2027-03-09,Club de Lectura Atenea,31,confirmada
        2027-03-09,Elena Sanz,1,confirmada
        2027-03-09,Familia Iglesias,6,confirmada
        2027-03-09,Familia Ortega,4,confirmada
        2027-03-09,Paula Romero,5,confirmada
        ```

??? abstract "Grupo 3"
    - **Asistente:** Asistente de una biblioteca municipal: préstamos, horarios y actividades.
    - **Agente:** OpenCode.
    - **Modelo de NVIDIA:** `mistralai/mistral-large-4-1t-a52b`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-05-06,Paula Romero,6,confirmada
        2027-05-07,Academia de Baile Compás,32,confirmada
        2027-05-08,Colegio San Isidro,26,confirmada
        2027-05-08,Scouts Valdemora 1,31,confirmada
        2027-05-09,Familia Ortega,5,confirmada
        2027-05-09,Lucía Ferrer,2,confirmada
        2027-05-09,Víctor Herrero,2,pendiente
        2027-05-10,Alba Méndez,6,confirmada
        2027-05-11,Daniel Cano,1,confirmada
        2027-05-11,Familia Moreno,3,confirmada
        2027-05-11,Sergio Pastor,1,pendiente
        2027-05-11,Óscar Delgado,1,confirmada
        2027-05-12,Club de Lectura Atenea,32,confirmada
        2027-05-12,Irene Calvo,6,confirmada
        2027-05-12,Javier Soler,5,cancelada
        2027-05-12,Marta Casado,5,confirmada
        2027-05-12,Nerea Lozano,5,cancelada
        ```

??? abstract "Grupo 4"
    - **Asistente:** Recepcionista de un hotel rural inventado.
    - **Agente:** Hermes Agent.
    - **Modelo de NVIDIA:** `nvidia/nemotron-3-ultra-550b-a55b`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-03-12,Sergio Pastor,5,pendiente
        2027-03-13,Elena Sanz,4,pendiente
        2027-03-13,Familia Ortega,4,confirmada
        2027-03-14,Andrés Molina,3,pendiente
        2027-03-14,Scouts Valdemora 1,14,confirmada
        2027-03-15,Academia de Baile Compás,14,confirmada
        2027-03-15,Familia Rubio,6,cancelada
        2027-03-15,Hugo Navarro,1,confirmada
        2027-03-15,Javier Soler,1,confirmada
        2027-03-15,Lucía Ferrer,1,confirmada
        2027-03-15,Rubén Prieto,5,cancelada
        2027-03-16,Irene Calvo,3,confirmada
        2027-03-17,Alba Méndez,3,pendiente
        2027-03-17,Residencia Los Olmos,10,confirmada
        2027-03-17,Sara Crespo,4,confirmada
        2027-03-18,Colegio San Isidro,12,confirmada
        2027-03-18,Daniel Cano,1,confirmada
        ```

??? abstract "Grupo 5"
    - **Asistente:** Entrenador de un gimnasio inventado que solo habla de ejercicio y alimentación sana.
    - **Agente:** OpenCode.
    - **Modelo de NVIDIA:** `nvidia/nemotron-3.5-super-vl-120b-a12b`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-04-09,AMPA Río Claro,28,confirmada
        2027-04-09,Sergio Pastor,4,confirmada
        2027-04-10,Alba Méndez,3,confirmada
        2027-04-10,Lucía Ferrer,2,confirmada
        2027-04-10,Paula Romero,4,pendiente
        2027-04-11,Hugo Navarro,6,confirmada
        2027-04-11,Rubén Prieto,1,confirmada
        2027-04-12,Carmen Vidal,2,confirmada
        2027-04-12,Irene Calvo,3,cancelada
        2027-04-12,Pablo Vega,4,confirmada
        2027-04-12,Residencia Los Olmos,11,cancelada
        2027-04-13,Coro Municipal,19,confirmada
        2027-04-13,Marta Casado,1,confirmada
        2027-04-15,Familia Moreno,5,cancelada
        2027-04-15,Familia Rubio,1,confirmada
        2027-04-15,Nerea Lozano,3,confirmada
        2027-04-15,Peña Ciclista La Cuesta,11,cancelada
        ```

??? abstract "Grupo 6"
    - **Asistente:** Asistente de una tienda de bicicletas eléctricas inventada.
    - **Agente:** Hermes Agent.
    - **Modelo de NVIDIA:** `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-03-04,Claudia Ramos,4,confirmada
        2027-03-04,Familia Ortega,1,confirmada
        2027-03-04,Javier Soler,4,confirmada
        2027-03-04,Pablo Vega,3,confirmada
        2027-03-04,Peña Ciclista La Cuesta,11,cancelada
        2027-03-05,Club de Lectura Atenea,11,confirmada
        2027-03-05,Óscar Delgado,5,cancelada
        2027-03-06,Colegio San Isidro,10,confirmada
        2027-03-06,Sergio Pastor,3,confirmada
        2027-03-07,Grupo IES Las Lomas,19,confirmada
        2027-03-07,Rubén Prieto,1,cancelada
        2027-03-08,Familia Rubio,4,confirmada
        2027-03-08,Nerea Lozano,3,confirmada
        2027-03-10,Daniel Cano,1,confirmada
        2027-03-10,Lucía Ferrer,3,pendiente
        2027-03-10,Paula Romero,4,confirmada
        ```

??? abstract "Grupo 7"
    - **Asistente:** Guía turístico de vuestra localidad.
    - **Agente:** OpenCode.
    - **Modelo de NVIDIA:** `nvidia/nemotron-3.5-bolt-e4b`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-05-03,Andrés Molina,1,confirmada
        2027-05-03,Sara Crespo,6,confirmada
        2027-05-04,Sergio Pastor,6,confirmada
        2027-05-04,Víctor Herrero,4,confirmada
        2027-05-05,Academia de Baile Compás,12,cancelada
        2027-05-05,Coro Municipal,16,confirmada
        2027-05-06,Alba Méndez,1,confirmada
        2027-05-06,Colegio San Isidro,32,confirmada
        2027-05-06,Familia Moreno,3,confirmada
        2027-05-06,Rubén Prieto,6,confirmada
        2027-05-07,Óscar Delgado,6,confirmada
        2027-05-09,Asociación Vecinal El Prado,17,pendiente
        2027-05-09,Daniel Cano,3,pendiente
        2027-05-09,Pablo Vega,3,pendiente
        ```

??? abstract "Grupo 8"
    - **Asistente:** Asistente de una clínica veterinaria inventada.
    - **Agente:** Hermes Agent.
    - **Modelo de NVIDIA:** `moonshotai/kimi-k3.1-pro`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-04-02,Carmen Vidal,3,pendiente
        2027-04-02,Club de Ajedrez Alfil,11,confirmada
        2027-04-02,Elena Sanz,1,confirmada
        2027-04-03,Asociación Vecinal El Prado,13,confirmada
        2027-04-03,Claudia Ramos,1,confirmada
        2027-04-03,Grupo IES Las Lomas,14,confirmada
        2027-04-03,Hugo Navarro,1,confirmada
        2027-04-04,Club Senderista Peñarrubia,16,confirmada
        2027-04-04,Nerea Lozano,6,confirmada
        2027-04-05,Familia Moreno,2,confirmada
        2027-04-05,Familia Ortega,4,confirmada
        2027-04-05,Pablo Vega,2,cancelada
        2027-04-06,Irene Calvo,3,cancelada
        2027-04-06,Lucía Ferrer,2,confirmada
        2027-04-07,Alba Méndez,2,confirmada
        2027-04-07,Familia Gil,2,confirmada
        2027-04-07,Familia Rubio,4,pendiente
        ```

??? abstract "Grupo 9"
    - **Asistente:** Asistente de una escuela de música inventada.
    - **Agente:** OpenCode.
    - **Modelo de NVIDIA:** `mistralai/mistral-large-4-1t-a52b`.
    - **Vuestro `reservas.csv`** (cópialo tal cual en la carpeta `practica15`):

        ```text
        fecha,nombre,personas,estado
        2027-03-09,Daniel Cano,3,cancelada
        2027-03-09,Elena Sanz,4,confirmada
        2027-03-09,Rubén Prieto,1,pendiente
        2027-03-09,Víctor Herrero,2,confirmada
        2027-03-10,Academia de Baile Compás,26,confirmada
        2027-03-10,Alba Méndez,6,cancelada
        2027-03-10,Claudia Ramos,6,pendiente
        2027-03-10,Pablo Vega,3,confirmada
        2027-03-11,Asociación Vecinal El Prado,28,cancelada
        2027-03-12,Andrés Molina,5,confirmada
        2027-03-12,Familia Ortega,2,confirmada
        2027-03-13,Club de Lectura Atenea,13,confirmada
        2027-03-13,Familia Gil,5,pendiente
        2027-03-14,Club Senderista Peñarrubia,15,pendiente
        2027-03-14,Irene Calvo,2,cancelada
        ```

## Validación en clase

Tendréis que enseñar al profesor, en vuestro equipo:

- El servidor local en marcha y el agente conectado a vuestro modelo.
- El agente respondiendo con la personalidad de `AGENTS.md`, incluida la frase final.
- La tarea de vuestro `reservas.csv` repetida en directo, con las ventanas de permiso, y vuestro recuento a mano.
- El agente conectado a NVIDIA (sin enseñar la clave).

## Entregables

- Tu `AGENTS.md`.
- Los dos `informe.md` (modelo local y modelo de NVIDIA), antes y después de la corrección, y los programas que escribió el agente.
- Tu recuento a mano del CSV.
- Capturas completas: el servidor local en marcha, la respuesta de `/v1/models`, el agente con cada modelo, las ventanas de permiso y los registros de LM Studio con los tokens.
- La tabla de tokens del apartado 8 con tu explicación.
- La tabla comparativa del apartado 12 y tus respuestas (máximo 250 palabras).
- **Ninguna clave**: si aparece en una captura, tápala.

