---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 22. Proyecto final: tu propio modelo

**Módulo:** [22. Crea tu propio modelo](../22-crear-llm.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** recorrer el ciclo completo de creación de un modelo especializado, desde la idea hasta una demostración en directo, y justificar cada decisión.

**Tema:** eliges tú el tema, pero debe **aprobarlo el profesor** antes de empezar y no puede repetirse en el grupo. Debe ser una tarea concreta y útil (no un chat general), distinta de la de la práctica 18.

## Fases y entregables

1. **Ficha del proyecto** (antes de empezar). Tarea, público, tono, qué no debe hacer y **cinco criterios de éxito** comprobables.
2. **¿Hace falta fine-tuning?** Antes de entrenar, intenta resolver la tarea **solo con un *system prompt*** (y, si sirve, una habilidad o documentos). Pruébalo con 20 casos y puntúalo. Este será tu **punto de partida**.
3. **Datos.** Un conjunto de **al menos 150 ejemplos** de calidad, con un registro de cómo los has obtenido (escritos por ti, adaptados de fuentes que cites, generados con IA y revisados…) y de las correcciones que has hecho.
4. **Entrenamiento.** Ajuste con Unsloth Studio, con validación, y las gráficas de pérdida.
5. **Evaluación.** Los **mismos 20 casos** del apartado 2 con el modelo ajustado, con la misma puntuación. ¿Ha mejorado respecto al *system prompt*? Si no, explica por qué.
6. **Iteración.** Al menos **un segundo entrenamiento** después de corregir los datos a partir de los fallos. Documenta qué cambiaste y qué mejoró.
7. **Despliegue.** El modelo en GGUF, cargado en LM Studio con un *preset* propio.
8. **Demostración** (5 minutos, en clase). Presentas tu modelo y respondes en directo a **entradas nuevas que te darán tus compañeros**.

## Evaluación

| Parte | Peso |
|---|---|
| Ficha y planteamiento | 15 % |
| Calidad y documentación de los datos | 25 % |
| Entrenamiento y evaluación | 25 % |
| Iteración | 15 % |
| Demostración | 20 % |
