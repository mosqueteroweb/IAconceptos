---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 21. Tu nano-modelo

**Módulo:** [21. Pre-entrenamiento](../21-pre-entrenamiento.md) · [Normas comunes de las prácticas](index.md)

!!! danger "Validación obligatoria en clase"
    El profesor tiene que ver en clase vuestro trabajo funcionando **antes** de que lo subas. Un trabajo subido sin haberlo validado antes en clase no se evalúa. Lo que tendréis que enseñar está en el apartado [Validación en clase](#validacion-en-clase).

**Objetivo:** pre-entrenar un modelo desde cero en vuestro ordenador con un libro, observar cómo aprende, relacionar el tamaño del modelo y de los datos con el resultado, y abrir vuestro propio modelo en LM Studio.

**Qué vais a usar:** el script [nanomodelo.py](../descargas/nanomodelo.py), que hace lo mismo que el cuaderno del módulo 21 pero desde la terminal, y **uv** (mirad las [normas comunes](index.md)). La primera vez, uv descarga PyTorch (unos 1-3 GB), así que tarda un rato. Entrena con la GPU del Mac o con la tarjeta NVIDIA del PC.

## Ejemplo resuelto

**Libro del ejemplo:** 320 · *Lazarillo de Tormes*. **Cambio del ejemplo:** `--capas 2`. Equipo: Mac con chip M2 Pro.

**1. Preparar la carpeta.** Carpeta `practica21`, terminal dentro de ella y descarga del script:

```bash
curl -L -o nanomodelo.py https://mosqueteroweb.github.io/IAconceptos/descargas/nanomodelo.py
```

**2. Primera ejecución, configuración por defecto:**

```bash
uv run nanomodelo.py caracteres --libro 320 --comienzo "Pues sepa Vuestra Merced"
```

El `resumen.txt` dice: 106 533 caracteres, vocabulario de 80 caracteres, **3 233 360 parámetros**, 210 s de entrenamiento. Las pérdidas (de `perdidas.csv`):

| Paso | 0 | 1 000 | 2 000 | 3 000 | 4 000 | 5 000 |
|---|---|---|---|---|---|---|
| Entrenamiento | 4,53 | 1,64 | 1,24 | 0,91 | 0,61 | **0,37** |
| Validación | 4,53 | 1,73 | **1,57** | 1,63 | 1,84 | **2,11** |

A partir del paso 2 000, la pérdida de entrenamiento sigue bajando y la de validación **sube**: el modelo está **memorizando** el libro, que es muy corto.

**3. Segunda ejecución, con el cambio:**

```bash
uv run nanomodelo.py caracteres --libro 320 --capas 2 --comienzo "Pues sepa Vuestra Merced"
```

**1 653 840 parámetros** (la mitad), 111 s:

| Paso | 0 | 1 000 | 2 000 | 3 000 | 4 000 | 5 000 |
|---|---|---|---|---|---|---|
| Entrenamiento | 4,65 | 1,83 | 1,51 | 1,30 | 1,15 | **1,01** |
| Validación | 4,64 | 1,88 | 1,65 | 1,58 | 1,58 | **1,61** |

Con la mitad de capas memoriza mucho menos: al final, la validación es **1,61**, frente a 2,11. Para un libro tan pequeño, el modelo pequeño generaliza mejor.

**4. Temperaturas** (modelo de 2 capas, de `textos.txt`):

- **0,3:** «Pues sepa Vuestra Merced de la casa y a la puerta a la puerta de la posada, que siempre traía a la posada y al ciego…». Repetitivo y «seguro».
- **0,8:** «…una lugar pecador sobre llegábalmos del primero, si el costado…». Más variado, con palabras inventadas.
- **1,3:** «…reV.M. asúbien preguntáronlas caba alguna gran ingencia…». Casi sin sentido.

**5. ¿Ha memorizado?** Buscamos en `libro-320.txt` (Cmd + F) trozos de los textos generados:

- Modelo de 4 capas: «**de su deuda. Anduvieron toda la casa**» aparece **tal cual** en el libro (7 palabras seguidas). Ha copiado.
- Modelo de 2 capas: ningún trozo de 5 palabras aparece en el libro.

**6. El nano-Llama:**

```bash
uv run nanomodelo.py llama --libro 320 --comienzo "Pues sepa Vuestra Merced"
```

El libro ocupa **42 186 tokens** con el tokenizador de SmolLM2 (106 533 caracteres: unos 2,5 caracteres por token). El modelo tiene **15 796 480 parámetros**, de los que **12 582 912** son la tabla de *embeddings* (49 152 tokens del vocabulario × 256 números cada uno): por eso es cinco veces más grande con las mismas capas. Tardó **13 minutos**. Pérdidas:

| Paso | 0 | 250 | 500 | 1 000 | 2 000 |
|---|---|---|---|---|---|
| Entrenamiento | 10,85 | 3,43 | 0,50 | 0,14 | **0,10** |
| Validación | 10,84 | **4,51** | 5,81 | 6,79 | **7,42** |

Casi 16 millones de parámetros para 42 000 tokens: el modelo **se aprende el libro de memoria** desde el paso 250.

**7. En LM Studio:**

```bash
lms import -c -y --user-repo alumno/practica21 resultados-320-llama/nano-libro-320.gguf
```

Con temperatura 0,8 y un límite de 100 tokens, a unos **700 tok/s** (Gemma 4 E2B, en el mismo Mac, va a 63):

- «Y fue ansí» → «…, que luego otro día salimos por la casa a pedir limosna, y había llovido mucho la noche antes; y porque el día también llovía, y andaba rezando debajo de unos portales…». Es, **casi palabra por palabra**, un párrafo del *Lazarillo* (el original dice «salimos por la villa»).
- «Pues sepa Vuestra Merced» → «…, que continuo la cerrada a toro, y díjele: "A fe, el cual yo no me preguntaronmo si quería decirme…"». Aquí mezcla trozos y no tiene sentido.

## Vuestra práctica

Haced lo mismo que en el ejemplo con **el libro y el cambio de vuestro grupo** (en [vuestra tarjeta](#lo-especifico-de-cada-grupo)):

1. **Preparad la carpeta** y descargad el script (en Windows, `curl.exe`).
2. **Primera ejecución** con la configuración por defecto, vuestro libro y vuestra frase de comienzo.
3. **Segunda ejecución** con vuestro cambio.
4. **Comparad:** tabla de las dos ejecuciones (parámetros, tiempo, pérdidas finales y mínimo de validación), los textos de las tres temperaturas y la comparación con el *Lazarillo* del ejemplo. ¿Vuestro libro es más o menos «difícil» de aprender? ¿Influye su tamaño?
5. **¿Ha memorizado?** ¿Se separan las pérdidas de entrenamiento y validación? ¿Desde qué paso? Buscad **dos trozos** de 4 o 5 palabras de los textos generados en `libro-NNNN.txt`.
6. **El nano-Llama** con vuestro libro. Tokens frente a caracteres, parámetros frente a *embeddings* y la gráfica de pérdidas. ¿Memoriza más o menos que el del ejemplo? ¿Por qué?
7. **En LM Studio**: importad el GGUF (si `lms` no se encuentra, en Mac está en `~/.lmstudio/bin/lms` y en Windows en `C:\Users\tu_usuario\.lmstudio\bin\lms.exe`), cargadlo con temperatura 0,8 y límite de 100 tokens, y escribid el principio de **tres frases típicas de vuestro libro**. Buscad si sus respuestas están copiadas del libro. Comparad su velocidad con la de Gemma 4 E2B en vuestro equipo.

## Lo específico de cada grupo

??? abstract "Grupo 1"
    - **Libro:** 16625 · *Libro de Buen Amor* (`--libro 16625`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--capas 6`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 2"
    - **Libro:** 29506 · *El sombrero de tres picos* (`--libro 29506`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--dim 128`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 3"
    - **Libro:** 49836 · *Niebla* (`--libro 49836`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--dim 384`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 4"
    - **Libro:** 17340 · *Marianela* (`--libro 17340`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--contexto 64`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 5"
    - **Libro:** 58221 · *La Odisea* (`--libro 58221`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--contexto 256`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 6"
    - **Libro:** 24536 · *Los cuatro jinetes del Apocalipsis* (`--libro 24536`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--pasos 10000`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 7"
    - **Libro:** 17223 · *Pepita Jiménez* (`--libro 17223`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--capas 2`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 8"
    - **Libro:** 16961 · *Trafalgar* (`--libro 16961`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--pasos 2000`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

??? abstract "Grupo 9"
    - **Libro:** 23600 · *La gaviota* (`--libro 23600`)
    - **Cambio en la arquitectura o el entrenamiento** (segunda ejecución): `--capas 8`
    - **Frase de comienzo:** elegidla vosotros, copiando el principio de una frase típica del libro.

## Validación en clase

Tendréis que enseñar al profesor, en vuestro equipo:

- Las carpetas `resultados-…` con vuestras gráficas, y la explicación de qué cambió con vuestro cambio.
- Vuestro nano-Llama cargado en LM Studio, respondiendo a una frase que os diga el profesor.
- Uno de los trozos copiados del libro, buscado en directo en `libro-NNNN.txt`.

## Entregables

- Las tres carpetas `resultados-…` (sin el archivo GGUF, que pesa mucho: basta con la captura de LM Studio).
- La tabla y las respuestas de los apartados 4 a 6.
- Los trozos buscados en el libro, con el resultado.
- Las capturas completas de vuestro modelo en LM Studio (**Library** y chat).
