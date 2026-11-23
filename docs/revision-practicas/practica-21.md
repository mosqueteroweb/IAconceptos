---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 21. Tu nano-modelo

**Módulo:** [21. Pre-entrenamiento](../21-pre-entrenamiento.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** pre-entrenar un modelo desde cero en tu ordenador con un libro distinto del Quijote, observar cómo aprende, relacionar el tamaño del modelo y de los datos con el resultado, y abrir tu propio modelo en LM Studio.

**Qué vas a usar:** el script [nanomodelo.py](../descargas/nanomodelo.py), que hace lo mismo que el cuaderno del módulo 21 pero desde la terminal, y **uv** (mira las [normas comunes](index.md)). La primera vez, uv descarga PyTorch (unos 1-3 GB), así que tarda un rato. Entrena con la GPU del Mac o con la tarjeta NVIDIA del PC.

## Tu variante

| N.º | Libro (`--libro`) | Cambio en la arquitectura |
|---|---|---|
| 1 | 320 · *Lazarillo de Tormes* | `--capas 2` |
| 2 | 16625 · *Libro de Buen Amor* | `--capas 6` |
| 3 | 29506 · *El sombrero de tres picos* | `--dim 128` |
| 4 | 49836 · *Niebla* | `--dim 384` |
| 5 | 17340 · *Marianela* | `--contexto 64` |
| 6 | 58221 · *La Odisea* | `--contexto 256` |
| 7 | 24536 · *Los cuatro jinetes del Apocalipsis* | `--pasos 10000` |

En las órdenes de abajo aparece el libro 320: cámbialo por el de tu variante. Cambia también la frase de `--comienzo` por **una frase típica de tu libro** (ábrelo en [Gutenberg](https://www.gutenberg.org/) y copia el principio de una frase).

## Tareas

### 1. Prepara la carpeta

Crea una carpeta `practica21`, abre la terminal dentro de ella (como en la [práctica 19](practica-19.md#1-prepara-las-herramientas)) y descarga el script (en Windows, `curl.exe`):

```bash
curl -L -o nanomodelo.py https://mosqueteroweb.github.io/IAconceptos/descargas/nanomodelo.py
```

Puedes abrirlo con un editor de texto: está comentado en español y las piezas son las mismas que las del módulo (tokenizador, datos, bloques Transformer, bucle de entrenamiento).

### 2. Primera ejecución: tu libro con la configuración por defecto

```bash
uv run nanomodelo.py caracteres --libro 320 --comienzo "Pues sepa Vuestra Merced"
```

El script descarga el libro, muestra cuántos **caracteres** tiene, el **tamaño del vocabulario** y los **parámetros** del modelo, y entrena 5 000 pasos mostrando la pérdida cada 500. Al terminar crea una carpeta `resultados-320-…` con:

| Archivo | Qué contiene |
|---|---|
| `resumen.txt` | Caracteres, vocabulario, parámetros, tiempo y pérdidas finales. |
| `perdidas.csv` y `perdidas.png` | La tabla y la gráfica de pérdidas (entrenamiento y validación). |
| `textos.txt` | Texto generado antes de entrenar y después, con temperatura 0,3, 0,8 y 1,3. |

### 3. Segunda ejecución: tu cambio de arquitectura

Repite la orden añadiendo el cambio de tu variante, por ejemplo:

```bash
uv run nanomodelo.py caracteres --libro 320 --capas 2 --comienzo "Pues sepa Vuestra Merced"
```

Cada ejecución guarda sus resultados en una carpeta distinta, así que no se borran los de la primera.

### 4. Compara

1. Haz una tabla con las dos ejecuciones: parámetros, tiempo de entrenamiento, pérdida final de entrenamiento y de validación.
2. Lee los textos de las **tres temperaturas** de tu mejor modelo. ¿Qué cambia?
3. Compara tus pérdidas con las del Quijote del módulo 21 (de 4,66 a 1,32 en 5 000 pasos). ¿Tu libro es más o menos «difícil» de aprender? ¿Influye su tamaño?

### 5. ¿Ha memorizado?

1. Mira la gráfica: ¿se separan las pérdidas de entrenamiento y de validación? ¿A partir de qué paso?
2. Copia **dos trozos** de 4 o 5 palabras seguidas de los textos generados y búscalos en el libro (el script lo guarda como `libro-320.txt` en tu carpeta; ábrelo y usa Cmd + F o Ctrl + F). ¿Aparecen tal cual? ¿Qué significa?

### 6. Segunda parte: un nano-Llama para LM Studio

El modelo de la primera parte tiene una arquitectura casera y un tokenizador inventado, y LM Studio solo carga arquitecturas conocidas. Ahora entrenas un **nano-Llama** (la arquitectura de los modelos Llama, en miniatura) con el tokenizador profesional de **SmolLM2**, y el script lo convierte a GGUF:

```bash
uv run nanomodelo.py llama --libro 320 --comienzo "Pues sepa Vuestra Merced"
```

Tarda unos 10-15 minutos. Anota del `resumen.txt` de la carpeta `resultados-320-llama`:

- Cuántos **tokens** ocupa el libro con este tokenizador, frente a los **caracteres** de la primera parte. ¿Cuántos caracteres hay de media en cada token?
- Cuántos **parámetros** tiene el modelo y cuántos son de la tabla de *embeddings*. ¿Por qué el modelo es ahora unas cinco veces más grande, si tiene las mismas capas?
- Su gráfica de pérdidas: compárala con la de la primera parte. ¿Qué le pasa a la pérdida de validación? Relaciónalo con el número de parámetros y el de tokens del libro.

### 7. Ábrelo en LM Studio

1. Importa el archivo GGUF (el script te muestra la orden exacta al terminar):

    ```bash
    lms import -c -y --user-repo alumno/practica21 resultados-320-llama/nano-libro-320.gguf
    ```

    Si `lms` no se encuentra, en Mac está en `~/.lmstudio/bin/lms` y en Windows en `C:\Users\tu_usuario\.lmstudio\bin\lms.exe`.

2. En LM Studio, carga `practica21`, pon la **temperatura en 0,8** y limita la respuesta a **100 tokens** (*Limit Response Length*).
3. Escríbele el principio de **tres frases típicas de tu libro**. Tu modelo no sabe conversar: continuará lo que escribas. Captura las respuestas y la velocidad (tok/s), y compárala con la de Gemma 4 E2B en tu equipo.

## Entregables

- Las tres carpetas `resultados-…` (sin el archivo GGUF, que pesa mucho: basta con la captura de LM Studio).
- La tabla y las respuestas de los apartados 4 a 6.
- Los dos trozos buscados en el libro, con el resultado.
- Las capturas completas de tu modelo en LM Studio (**Library** y chat).

**Defensa posible:** explicar en clase, con tus gráficas, qué ha cambiado al modificar la arquitectura y por qué.
