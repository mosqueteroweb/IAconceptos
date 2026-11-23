---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 19. Cuantizar y medir

**Módulo:** [19. Cuantización](../19-cuantizacion.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** cuantizar un modelo tú mismo, en tu ordenador y con la terminal, con las mismas herramientas que usan por dentro LM Studio y Ollama, y medir con datos (tamaño, velocidad y perplejidad) qué se gana y qué se pierde.

**Qué vas a usar:** [llama.cpp](https://github.com/ggml-org/llama.cpp) (los programas `llama-quantize`, `llama-bench` y `llama-perplexity`), **uv** (mira las [normas comunes](index.md)) y LM Studio. Unos 5 GB libres de disco.

## Tu variante

| N.º | Modelo que cuantizas | Modelo para LM Studio |
|---|---|---|
| 1 | Qwen/Qwen3-0.6B | Gemma 4 E2B (Q4_K_M y Q8_0) |
| 2 | Qwen/Qwen3-1.7B | Qwen3 4B (Q4_K_M y Q8_0) |
| 3 | Qwen/Qwen3-0.6B | Qwen3 8B (Q3_K_M y Q4_K_M) |
| 4 | Qwen/Qwen3-1.7B | Gemma 4 E4B (Q4_K_M y Q8_0) |
| 5 | Qwen/Qwen3-4B | Qwen3 1.7B (Q4_K_M y Q8_0) |

En las órdenes de abajo aparece `Qwen/Qwen3-0.6B`: cámbialo por el modelo de tu variante.

## Tareas

### 1. Prepara las herramientas

Crea una carpeta `practica19` y abre la terminal **dentro de ella**: en Mac, escribe `cd ` y arrastra la carpeta a la Terminal; en Windows, abre la carpeta en el Explorador, haz clic en la barra de direcciones, escribe `powershell` y pulsa Intro.

=== "Mac"

    1. Instala llama.cpp con [Homebrew](https://brew.sh/):

        ```bash
        brew install llama.cpp
        ```

    2. Comprueba que funciona:

        ```bash
        llama-quantize --help
        ```

=== "PC (Windows)"

    1. Entra en la página de [versiones de llama.cpp](https://github.com/ggml-org/llama.cpp/releases/latest) y, en *Assets*, descarga estos dos archivos:
        - `llama-…-bin-win-cuda-13.5-x64.zip` (los programas, preparados para tarjetas NVIDIA).
        - `cudart-llama-bin-win-cuda-13.5-x64.zip` (las librerías de CUDA que necesitan).
    2. Crea la carpeta `C:\llama` y descomprime **los dos** archivos dentro (que los `.exe` y los `.dll` queden juntos en `C:\llama`).
    3. En la terminal, añade esa carpeta a las órdenes disponibles (hay que repetirlo cada vez que abras una terminal nueva):

        ```powershell
        $env:Path += ";C:\llama"
        ```

    4. Comprueba que funciona:

        ```powershell
        llama-quantize --help
        ```

    Si da error con la tarjeta gráfica, actualiza el controlador de NVIDIA o usa la versión `…-bin-win-vulkan-x64.zip`, que funciona con cualquier tarjeta.

Después, descarga el código de llama.cpp, que incluye el *script* de conversión (es el mismo para Mac y PC; en Windows escribe `curl.exe` en lugar de `curl`):

```bash
curl -L -o llama-src.zip https://github.com/ggml-org/llama.cpp/archive/refs/heads/master.zip
tar -xf llama-src.zip
```

Se crea la carpeta `llama.cpp-master`.

### 2. Descarga el modelo original

Bajamos el modelo tal y como lo publica su autor en Hugging Face, a 16 bits:

```bash
uvx hf download Qwen/Qwen3-0.6B --local-dir modelo-original
```

Anota el tamaño de los archivos `.safetensors` de la carpeta `modelo-original`.

### 3. Convierte a GGUF (sin cuantizar)

GGUF es el formato que entienden LM Studio, Ollama y llama.cpp: un solo archivo con los pesos, el tokenizador y la arquitectura. Primero lo convertimos manteniendo los 16 bits (BF16). La primera vez tarda unos minutos porque uv descarga lo que necesita el *script*:

=== "Mac"

    ```bash
    uv run --python 3.12 --with-requirements llama.cpp-master/requirements/requirements-convert_hf_to_gguf.txt python llama.cpp-master/convert_hf_to_gguf.py modelo-original --outtype bf16 --outfile modelo-bf16.gguf
    ```

=== "PC (Windows)"

    ```powershell
    uv run --python 3.12 --with-requirements llama.cpp-master\requirements\requirements-convert_hf_to_gguf.txt python llama.cpp-master\convert_hf_to_gguf.py modelo-original --outtype bf16 --outfile modelo-bf16.gguf
    ```

### 4. Cuantiza a tres niveles

`llama-quantize` redondea cada peso a menos bits. Ejecuta una orden por cada nivel:

```bash
llama-quantize modelo-bf16.gguf modelo-Q8_0.gguf Q8_0
llama-quantize modelo-bf16.gguf modelo-Q4_K_M.gguf Q4_K_M
llama-quantize modelo-bf16.gguf modelo-Q2_K.gguf Q2_K
```

| Tipo | Bits aproximados | Qué es |
|---|---|---|
| `Q8_0` | 8,5 | Casi sin pérdida. |
| `Q4_K_M` | 4,8 | El equilibrio habitual: el que más verás en LM Studio. |
| `Q2_K` | 2,6 | Compresión extrema. |

Anota el tamaño de los cuatro archivos `.gguf` y el porcentaje respecto al BF16.

### 5. Mide la velocidad

`llama-bench` mide cuántos tokens por segundo procesa tu equipo al **leer** un texto (`pp512`) y al **escribir** (`tg128`). Mide los cuatro archivos de una vez y guarda el resultado en un archivo:

```bash
llama-bench -m modelo-bf16.gguf -m modelo-Q8_0.gguf -m modelo-Q4_K_M.gguf -m modelo-Q2_K.gguf | tee velocidad.txt
```

### 6. Mide la calidad: la perplejidad

La **perplejidad** mide cuánto le «sorprende» al modelo un texto que no ha visto: cuanto **más baja**, mejor predice. Usamos las primeras páginas del *Lazarillo de Tormes*. Descárgalas (en Windows, `curl.exe`):

```bash
curl -L -o lazarillo.txt https://mosqueteroweb.github.io/IAconceptos/descargas/lazarillo-perplejidad.txt
```

Y mide cada versión (tarda uno o dos minutos por archivo). La cifra que buscas aparece al final, en la línea **`Final estimate: PPL =`**:

```bash
llama-perplexity -m modelo-bf16.gguf -f lazarillo.txt -c 512
llama-perplexity -m modelo-Q8_0.gguf -f lazarillo.txt -c 512
llama-perplexity -m modelo-Q4_K_M.gguf -f lazarillo.txt -c 512
llama-perplexity -m modelo-Q2_K.gguf -f lazarillo.txt -c 512
```

### 7. Tabla y gráfica

Haz una tabla con las cuatro versiones (tamaño, velocidad al escribir y perplejidad) y una gráfica del **tamaño frente a la perplejidad**. ¿Dónde está el «codo», el punto a partir del cual comprimir más ya no compensa?

### 8. Tus GGUF en LM Studio

1. Importa tus cuatro archivos en LM Studio (si `lms` no se encuentra, en Mac está en `~/.lmstudio/bin/lms` y en Windows en `C:\Users\tu_usuario\.lmstudio\bin\lms.exe`):

    ```bash
    lms import -c -y --user-repo alumno/practica19 modelo-bf16.gguf
    lms import -c -y --user-repo alumno/practica19 modelo-Q8_0.gguf
    lms import -c -y --user-repo alumno/practica19 modelo-Q4_K_M.gguf
    lms import -c -y --user-repo alumno/practica19 modelo-Q2_K.gguf
    ```

    Aparecerán en **Library** como un solo modelo, `practica19`, con cuatro variantes.

2. Escribe **una pregunta tuya** sobre una asignatura que estudies. Hazla a las cuatro versiones con **temperatura 0** y **Think** desactivado. Compara las cuatro respuestas y la velocidad que indica LM Studio con la de `llama-bench`.

### 9. Los modelos de tu variante

En LM Studio, descarga el modelo de la columna «Modelo para LM Studio» de tu variante en las dos cuantizaciones indicadas. Mide la velocidad (tres preguntas, tres veces cada una) y anota la memoria estimada al cargarlo.

### 10. Cálculo

Con la regla del módulo, calcula cuánto ocuparía un modelo de **14 000 millones de parámetros** en BF16, Q8_0 y Q4_K_M. ¿Cuál cabría en tu equipo? ¿Y en el otro tipo de equipo del aula? Justifícalo con los datos de la pantalla **Hardware** de LM Studio.

## Entregables

- `velocidad.txt` y la salida de las cuatro órdenes de perplejidad (cópiala en un archivo `perplejidad.txt`).
- La tabla y la gráfica del apartado 7.
- Las respuestas del apartado 8 y la captura de **Library** con tus cuatro modelos.
- Las mediciones del apartado 9 con capturas completas.
- Los cálculos del apartado 10.

**Defensa posible:** explicar con tus cifras por qué la versión más comprimida no siempre es la más rápida en tu equipo, o por qué la perplejidad de Q8_0 es casi igual a la del original.
