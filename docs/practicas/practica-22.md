# Práctica 22. Proyecto final: vuestro propio modelo

**Módulo:** [22. Crea tu propio modelo](../22-crear-llm.md) · [Normas comunes de las prácticas](segunda-parte.md)

!!! danger "Validación obligatoria en clase"
    El profesor tiene que ver en clase vuestro modelo funcionando **antes** de que subáis el trabajo. Un trabajo subido sin haberlo validado antes en clase no se evalúa. La validación es la demostración de la fase 8.

**Objetivo:** recorrer el ciclo completo de creación de un modelo especializado, desde la idea hasta una demostración en directo, y justificar cada decisión.

**Tema:** lo elegís vosotros, pero debe **aprobarlo el profesor** antes de empezar y no puede repetirse en la clase. Debe ser una tarea concreta y útil (no un chat general), distinta de la de la práctica 18. Además, cada grupo tiene un **requisito obligatorio** (en [vuestra tarjeta](#lo-especifico-de-cada-grupo)).

## Ejemplo resuelto (fases 1 y 2)

El proyecto completo dura varias semanas; el ejemplo muestra cómo empezar bien, que es lo más difícil.

**Fase 1. Ficha del proyecto.**

| Apartado | Ejemplo |
|---|---|
| Tarea | Convertir un párrafo de un libro de texto en 3 preguntas tipo test. |
| Público | Profesorado y alumnado de 3.º de ESO. |
| Tono | Neutro y claro, sin bromas. |
| Qué no debe hacer | Inventar datos que no estén en el texto; dar pistas en el enunciado. |
| Criterios de éxito | 1) Exactamente 3 preguntas con 4 opciones. 2) Una sola opción correcta. 3) Todo sale del texto. 4) Las soluciones **no** siguen un patrón (no siempre la misma letra). 5) Las tres preguntas son distintas entre sí. |

**Fase 2. ¿Hace falta *fine-tuning*?** Antes de entrenar, lo intentamos solo con un *system prompt*, en Gemma 4 E2B:

> Eres un generador de preguntas tipo test para alumnado de 3.º de ESO. Con el texto que te den, escribe exactamente 3 preguntas, cada una con 4 opciones (a, b, c, d) y una sola correcta. Al final, escribe una línea «Soluciones:» con las tres letras. No añadas nada más.

Dos de los veinte casos, con un texto sobre la mitosis y otro sobre el río Ebro:

??? example "Los dos textos del ejemplo"

    **Mitosis:** «La mitosis es un tipo de división celular en la que una célula madre da lugar a dos células hijas con el mismo número de cromosomas. Tiene cuatro fases: profase, metafase, anafase y telofase.»

    **Río Ebro:** «El río Ebro nace en Fontibre (Cantabria) y desemboca en el mar Mediterráneo, formando un delta en Tarragona. Es el río más caudaloso de España.»


| Criterio | Mitosis | Ebro |
|---|---|---|
| 1. Tres preguntas con 4 opciones | Sí | Sí |
| 2. Una sola correcta | Sí | Sí |
| 3. Todo sale del texto | Sí | Sí |
| 4. Soluciones sin patrón | **No**: «Soluciones: b, b, b» | Sí (c, c, b) |
| 5. Preguntas distintas | **No**: la 1.ª y la 3.ª preguntan lo mismo (el número de cromosomas) | Sí |
| **Total** | **3/5** | **5/5** |

Con el *system prompt* ya se cumple casi todo. Los fallos son justo los que un buen conjunto de datos puede corregir: **150 ejemplos con las soluciones repartidas entre a, b, c y d** y con preguntas sobre aspectos distintos del texto. Si los veinte casos hubieran salido perfectos, lo honrado sería decir que no hace falta entrenar, o justificar por qué se entrena igualmente (un modelo más pequeño, un formato más fiable…).

**Fases 3 a 8:** se hacen como en las prácticas 18 y 20, con estos datos.

## Fases y entregables

1. **Ficha del proyecto** (antes de empezar): tarea, público, tono, qué no debe hacer y **cinco criterios de éxito** comprobables, como en el ejemplo.
2. **¿Hace falta fine-tuning?** Intentad resolver la tarea **solo con un *system prompt*** (y, si sirve, una habilidad o documentos). Probadlo con 20 casos y puntuadlo. Este será vuestro **punto de partida**.
3. **Datos.** Un conjunto de **al menos 150 ejemplos** de calidad, en **formato de chat** (como en las prácticas 18 y 20), con un registro de cómo los habéis obtenido (escritos por vosotros, adaptados de fuentes que citéis, generados con IA o con un programa y revisados…) y de las correcciones. Si los generáis, revisad que no enseñen a **inventar**: que cada respuesta use solo datos que estén en la pregunta o en la entrada.
4. **Entrenamiento.** Ajuste con Unsloth Studio (*Format* **auto**), con validación, y las gráficas de pérdida.
5. **Evaluación.** Los **mismos 20 casos** del apartado 2 con el modelo ajustado y la misma puntuación. ¿Ha mejorado respecto al *system prompt*? Si no, explicad por qué.
6. **Iteración.** Al menos **un segundo entrenamiento** después de corregir los datos a partir de los fallos. Documentad qué cambiasteis y qué mejoró.
7. **Despliegue.** El modelo en GGUF, cargado en LM Studio con un *preset* propio.
8. **Demostración y validación** (5 minutos, en clase). Presentáis vuestro modelo y responde en directo a **entradas nuevas que os darán vuestros compañeros**.

## Lo específico de cada grupo

??? abstract "Grupo 1"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** El modelo debe ser el más pequeño posible: Qwen3-0.6B.

??? abstract "Grupo 2"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** Las respuestas no pueden pasar de 60 palabras.

??? abstract "Grupo 3"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** El modelo debe responder siempre con el mismo formato en Markdown (encabezado y lista).

??? abstract "Grupo 4"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** El modelo debe negarse educadamente a todo lo que no sea de su tarea (al menos 15 de los 150 ejemplos deben enseñarle a negarse).

??? abstract "Grupo 5"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** El *preset* final debe usar temperatura 0,2 o menos, y el modelo tiene que funcionar bien con ella.

??? abstract "Grupo 6"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** Al menos 30 de los ejemplos deben estar escritos por vosotros desde cero, sin ayuda de una IA.

??? abstract "Grupo 7"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** El modelo debe responder siempre en un registro formal (de usted).

??? abstract "Grupo 8"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** Los 20 casos de evaluación los escribe otro grupo (el profesor os dirá cuál) y no los veis hasta la fase 5.

??? abstract "Grupo 9"
    - **Tema:** lo elegís vosotros y lo aprueba el profesor (no puede repetirse en la clase).
    - **Requisito obligatorio de vuestro grupo:** El modelo debe funcionar en el Mac y en el PC: comparad la velocidad en los dos tipos de equipo.

## Evaluación

| Parte | Peso |
|---|---|
| Ficha y planteamiento | 15 % |
| Calidad y documentación de los datos | 25 % |
| Entrenamiento y evaluación | 25 % |
| Iteración | 15 % |
| Demostración | 20 % |
