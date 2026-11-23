---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 18. Un modelo con estilo propio

**Módulo:** [18. Fine-tuning](../18-fine-tuning.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** crear tu propio conjunto de datos, ajustar un modelo con QLoRA y comprobar con pruebas si de verdad ha aprendido el estilo, sin memorizar.

## Tu variante (el estilo que aprenderá tu modelo)

| N.º | Estilo |
|---|---|
| 1 | Locutor de radio deportiva que lo narra todo como un partido. |
| 2 | Abuela que responde con un refrán y un consejo. |
| 3 | Presentador de documentales de naturaleza. |
| 4 | Asistente que responde siempre en tres viñetas y una pregunta final. |
| 5 | Caballero medieval que habla en castellano antiguo. |
| 6 | Profesor que nunca da la respuesta y guía con preguntas. |
| 7 | Periodista de sucesos que convierte cualquier tema en titular. |
| 8 | Asistente que explica todo con analogías de cocina. |

## Qué modelo usar

| Equipo | Modelo base | Método en Unsloth Studio |
|---|---|---|
| Mac mini M4 16 GB | Qwen3-1.7B | LoRA (o QLoRA si está disponible) |
| PC RTX 5060 Ti 16 GB | Gemma 4 E2B o Qwen3-4B | QLoRA |
| Google Colab | Gemma 4 E2B | QLoRA, con el [cuaderno de Unsloth Studio](https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb) |

Con tan pocos ejemplos, pon **Gradient Accumulation en 1** (por defecto es 8 y el modelo apenas cambiaría).

## Tareas

1. **Datos.** Crea un archivo JSONL en formato Alpaca con **al menos 60 ejemplos** de tu estilo, sobre temas variados. Puedes ayudarte de una IA para generar borradores, pero **revisa y corrige cada ejemplo** y escribe tú **al menos 20** desde cero (márcalos en una lista).
2. **Prueba aparte.** Escribe **10 preguntas de prueba** que **no** estén en los datos.
3. **Antes.** Haz las 10 preguntas al modelo base y guarda las respuestas.
4. **Entrenamiento.** Ajusta el modelo de tu tipo de equipo con **Unsloth Studio**, con un 10 % de validación. Guarda la configuración (**Save**) y captura las gráficas de pérdida.
5. **Después.** Haz las mismas 10 preguntas al modelo ajustado. Puntúa de 0 a 2 cada respuesta del modelo base y del ajustado: ¿mantiene el estilo?, ¿es correcta?
6. **Experimento.** Entrena una segunda vez cambiando **una sola cosa**: el número de épocas (1 o 6) o el rango de LoRA (4 o 64). Compara la pérdida de validación y las respuestas. ¿Hay sobreajuste? ¿Cómo lo sabes?
7. **Exportación.** Exporta el mejor modelo a GGUF, impórtalo en LM Studio (`lms import -c -y --user-repo alumno/practica18 archivo.gguf`) y conversa con él.

## Entregables

- El archivo JSONL y la lista de los ejemplos escritos por ti.
- La configuración guardada (YAML) de los dos entrenamientos.
- Capturas completas de las gráficas de pérdida.
- La tabla de puntuaciones antes y después.
- La captura de LM Studio con tu modelo cargado.
- Las conclusiones del experimento.

**Defensa posible:** en clase, tus compañeros escribirán tres preguntas nuevas y tu modelo tendrá que responderlas en directo con tu estilo.
