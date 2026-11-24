# Práctica 13. El laboratorio de prompts

**Módulo:** [13. Aplicaciones e ingeniería de prompts](../13-apps-prompts.md) · [Normas comunes de las prácticas](segunda-parte.md)

!!! danger "Validación obligatoria en clase"
    El profesor tiene que ver en clase vuestro trabajo funcionando **antes** de que lo subas. Un trabajo subido sin haberlo validado antes en clase no se evalúa. Lo que tendréis que enseñar está en el apartado [Validación en clase](#validacion-en-clase).

**Objetivo:** demostrar con vuestras pruebas cómo mejora una respuesta al mejorar el prompt, y aprender a comprobar lo que dice una IA.

## Ejemplo resuelto

**Escenario del ejemplo:** organizar la fiesta de fin de curso de 4.º de ESO. Lo resolvimos con dos asistentes: **Gemma 4 E2B** en LM Studio (local) y **Nemotron 3.5 Lightning** en la API de NVIDIA (en la nube). Los textos de las respuestas son reales; aquí solo se muestran trozos.

!!! note "Vosotros podéis usar cualquier asistente"
    En el ejemplo, el segundo asistente es Nemotron, al que accedimos a través de la API de NVIDIA, que veréis en la [práctica 17](practica-17.md). Para esta práctica no hace falta: usad los asistentes web que prefiráis (ChatGPT, Gemini, Claude, Copilot) o un modelo de LM Studio. Lo importante es comparar **dos asistentes distintos**.

**1. Prompt débil.**

> Organiza una fiesta de fin de curso.

La respuesta fue una guía genérica de 3 400 caracteres: «Fase 1: Planificación Inicial», ideas de temas («noche de gala, fiesta retro…»)… Nada que sirva para **nuestro** instituto: no sabe cuántos somos, ni cuándo, ni con qué dinero.

**2. Prompt estructurado (R-T-F con restricciones).**

> **Rol:** actúa como coordinador de actividades de un instituto público.
> **Tarea:** organiza la fiesta de fin de curso de 4.º de ESO del IES Valdemora del Río (60 alumnos, 4 tutores) para el viernes 18 de junio de 2027, de 17.00 a 20.00 h, en el patio del centro.
> **Formato:** una tabla con el horario minuto a minuto, otra con el presupuesto por partidas y una lista de tareas con responsable (alumnado, tutores o AMPA).
> **Restricciones:** presupuesto máximo de 300 €; nada de alcohol; la música debe acabar a las 19.45 h por las normas del ayuntamiento; tiene que haber una alternativa si llueve.

Ahora la respuesta tenía las tres partes pedidas: un horario de 17.00 a 20.00 h con «Música y cierre musical» hasta las 19.45 h, un presupuesto de cinco partidas que suma exactamente 300 € y un plan para la lluvia («se trasladará al Salón de Actividades»).

**3. Meta-prompt.** Le pedimos: «Quiero que me ayudes a organizar la fiesta de fin de curso de mi instituto. Antes de nada, hazme todas las preguntas que necesites (como máximo 8). Después, cuando te conteste, escribe tú el mejor prompt posible para conseguirlo». Hizo 8 preguntas (presupuesto, asistentes, ambiente, fecha…). Al contestarlas, escribió un prompt de cuatro secciones que **añadía algo que se nos había olvidado**: la entrega de diplomas.

??? example "Nuestras respuestas a sus 8 preguntas y el prompt que escribió"

    **Nuestras respuestas:**

    > 1) 4.º de ESO, 60 alumnos y 4 tutores. 2) Viernes 18 de junio de 2027, de 17.00 a 20.00 h. 3) En el patio del IES Valdemora del Río; si llueve, el gimnasio. 4) Presupuesto máximo 300 €, lo pone la AMPA. 5) Sin alcohol; música hasta las 19.45 h. 6) Queremos una entrega de diplomas, música y comida. 7) Formato: tablas de horario y presupuesto y lista de tareas. 8) Lo organiza el alumnado con ayuda de los tutores.

    **El prompt que escribió** (es el que ejecutamos después en Gemma y en Nemotron):

    ```text
        Actúa como un organizador de eventos experto en gestión de presupuestos escolares y planificación de fiestas temáticas. Basándote en la siguiente información, genera un plan de acción completo, detallado y organizado, incluyendo tablas claras de presupuesto, horarios y una lista de tareas (checklist) para organizar la Fiesta de Fin de Curso del 4.º de ESO.

        Datos Clave:
        1. Asistentes: 60 alumnos y 4 tutores (Total: 64 personas).
        2. Fecha y Hora: Viernes, 18 de junio de 2027, de 17:00 a 20:00 h.
        3. Lugar Propuesto: Patio del IES Valdemora del Río (con plan B en el gimnasio si llueve).
        4. Presupuesto Máximo: 300 € (A cargo de la AMPA).
        5. Restricciones Importantes: No se permitirá el alcohol. La música debe finalizar a las 19:45 h.
        6. Elementos Requeridos: Entrega de diplomas, música y comida.
        7. Organización: El alumnado organizará la fiesta con la ayuda de los tutores.

        Output Solicitado (Formato Estricto):

        Genera el plan estructurado en las siguientes secciones:

        Sección 1: Distribución del Presupuesto Estimado (Máximo 300 €)
        *   Crea una tabla desglosando los posibles gastos principales (Alquiler/Permisos, Comida, Decoración, Música, Diplomas). Asigna un coste estimado a cada rubro.

        Sección 2: Tabla de Horario Detallado (Cronograma)
        *   Crea un horario minuto a minuto desde las 17:00 h hasta las 20:00 h, especificando cuándo deben ocurrir las actividades clave (llegada, comida, entrega de diplomas, música).

        Sección 3: Lista de Tareas y Responsabilidades (Checklist)
        *   Crea una lista exhaustiva de tareas divididas por responsabilidades (Alumnado, Tutores/AMPA), incluyendo plazos sugeridos (ej. 4 semanas antes) para asegurar la organización fluida.

        Sección 4: Sugerencias Creativas (Ambientación y Menú)
        *   Ofrece ideas específicas y económicas para la decoración, el menú (enfocado en ser festivo y sin alcohol), y opciones de música adecuadas para el ambiente escolar.
    ```

!!! warning "Un fallo nuestro"
    La primera vez pegamos **toda** su respuesta, con el «¡Muchas gracias por la información!» incluido, y el modelo contestó «¡Me parece un prompt excelente! Por favor, procede a ejecutarlo». Hay que copiar **solo el prompt**.

**4. Otro asistente.** El mismo meta-prompt en Nemotron (NVIDIA) dio un plan más detallado: precio por persona de la comida (1,85 €), horario de 17.00 a 17.10 para la recepción, etc.

**5. Rúbrica.** Nuestros cuatro criterios, puntuados de 1 a 5:

| Respuesta | Adaptada a nuestros datos | Cumple las restricciones | Formato pedido | Cifras coherentes | Total |
|---|---|---|---|---|---|
| Prompt débil (Gemma) | 1 | 1 | 1 | — (no hay cifras) | 3 |
| Estructurado (Gemma) | 4 | 5 | 5 | 5 | 19 |
| Meta-prompt (Gemma) | 5 | 5 | 5 | 5 | 20 |
| Meta-prompt (Nemotron) | 5 | 5 | 5 | 3 | 18 |

**6. Verificación.** Comprobamos tres datos de las respuestas:

1. **El presupuesto de Gemma (meta-prompt):** 30 + 120 + 50 + 40 + 35 + 25 = 300 €. **Correcto.**
2. **El presupuesto de Nemotron:** 0 + 118 + 45 + 35 + 75 + 22 = 295 €, y 64 × 1,85 € = 118,40 €. **Correcto.**
3. **Los diplomas de Nemotron:** «64 diplomas entregados en bloque (~30 seg cada uno)», en un hueco de 15 minutos. **Mal dos veces:** los diplomas son para los 60 alumnos, no para los tutores, y 64 × 30 s son 32 minutos, no 15.

**Conclusión del ejemplo:** lo que más mejoró el resultado fueron los **datos concretos y las restricciones** (de 3 a 19 puntos). El meta-prompt añadió algo que habíamos olvidado. El modelo más grande escribió más, pero no se equivocó menos en las cuentas: siempre hay que comprobarlas.

## Vuestra práctica

Haced lo mismo que en el ejemplo con el **escenario de vuestro grupo**:

1. **Prompt débil.** Un prompt de una sola línea. Ejecutadlo en un asistente (ChatGPT, Gemini, Claude, Copilot o un modelo de LM Studio) y guardad la respuesta.
2. **Prompt estructurado.** Reescribidlo con R-T-F, C-O-T o P-A-S, con **datos reales vuestros**, un formato concreto y al menos **dos restricciones**, una de ellas la que indica vuestra tarjeta.
3. **Meta-prompt.** Pedid al asistente que os haga preguntas y escriba él el mejor prompt. Contestad y ejecutad **solo el prompt** que os proponga.
4. **Otro asistente.** Ejecutad vuestro mejor prompt en un asistente distinto.
5. **Rúbrica.** Cuatro criterios vuestros y la tabla de puntuaciones de las **cuatro respuestas** (prompt débil, prompt estructurado, prompt del meta-prompt y ese mismo prompt en el otro asistente), como en el ejemplo.
6. **Verificación.** Tres afirmaciones concretas comprobadas, **al menos dos en una fuente externa fiable** (indicad el enlace).
7. **La comprobación de vuestro grupo.** Haced la comprobación especial que indica vuestra tarjeta.

## Lo específico de cada grupo

??? abstract "Grupo 1"
    - **Escenario:** preparar un examen de Historia de 2.º de Bachillerato sobre un tema que elijáis.
    - **Restricción obligatoria:** el examen debe durar 90 minutos y tener exactamente tres partes.
    - **Comprobación del grupo:** verificad **cinco fechas o nombres** del examen en vuestro libro de texto o en una enciclopedia, con la página o el enlace.

??? abstract "Grupo 2"
    - **Escenario:** plan de entrenamiento de 8 semanas para correr 10 km, para alguien que nunca ha corrido.
    - **Restricción obligatoria:** solo tres días por semana y ninguna sesión de más de 45 minutos.
    - **Comprobación del grupo:** pedid después al asistente que adapte el plan a alguien con una lesión de rodilla y buscad en una fuente sanitaria fiable si sus recomendaciones son prudentes.

??? abstract "Grupo 3"
    - **Escenario:** menú semanal para una familia de cuatro con una persona celíaca y presupuesto ajustado.
    - **Restricción obligatoria:** máximo 110 € a la semana.
    - **Comprobación del grupo:** elegid **tres productos** del menú y comprobad en la web de la Federación de Asociaciones de Celíacos de España (FACE) o en el etiquetado real si son aptos.

??? abstract "Grupo 4"
    - **Escenario:** guion de un vídeo de 60 segundos para promocionar las jornadas de puertas abiertas del centro.
    - **Restricción obligatoria:** que lo puedan grabar dos alumnos con un móvil, sin música con derechos de autor.
    - **Comprobación del grupo:** leed el guion en voz alta con un cronómetro. ¿Dura de verdad 60 segundos? Anotad el tiempo.

??? abstract "Grupo 5"
    - **Escenario:** comparativa de tres móviles de menos de 300 € para una persona mayor.
    - **Restricción obligatoria:** pantalla de 6,5 pulgadas o más y a la venta hoy en España.
    - **Comprobación del grupo:** buscad el **precio actual** de los tres móviles en dos tiendas reales y comparadlo con lo que dijo la IA.

??? abstract "Grupo 6"
    - **Escenario:** carta de reclamación por un vuelo cancelado.
    - **Restricción obligatoria:** un vuelo de Madrid a Roma cancelado con dos días de aviso.
    - **Comprobación del grupo:** buscad en el Reglamento (CE) 261/2004 o en la web de la Agencia Estatal de Seguridad Aérea (AESA) la **compensación** que corresponde a esa distancia y comparadla con la de la carta.

??? abstract "Grupo 7"
    - **Escenario:** plan de estudio para preparar el B2 de inglés en tres meses.
    - **Restricción obligatoria:** cinco horas a la semana como máximo.
    - **Comprobación del grupo:** comprobad en la web oficial de Cambridge English o de una Escuela Oficial de Idiomas **qué partes tiene el examen B2** y si el plan las cubre todas.

??? abstract "Grupo 8"
    - **Escenario:** organizar una excursión de un día para un grupo de 25 alumnos.
    - **Restricción obligatoria:** salida y vuelta desde vuestro centro, en transporte público.
    - **Comprobación del grupo:** comprobad en la web real de la compañía de transporte los **horarios y precios** que propuso la IA.

??? abstract "Grupo 9"
    - **Escenario:** plan para montar un huerto escolar en un patio de 20 m².
    - **Restricción obligatoria:** presupuesto de 150 € y que se pueda cosechar antes de junio.
    - **Comprobación del grupo:** comprobad en un calendario de siembra de una fuente fiable (un vivero, una cooperativa o el ministerio de agricultura) si las fechas de siembra propuestas valen para vuestra zona.

## Validación en clase

Tendréis que enseñar al profesor:

- Las conversaciones abiertas en el asistente, con el prompt débil, el estructurado y el meta-prompt.
- Una de las verificaciones, con la fuente abierta en el navegador.
- El profesor ejecutará uno de vuestros prompts en otro asistente y le explicaréis para qué sirve cada parte.

## Entregables

- Los cuatro prompts: el débil, el estructurado, vuestra petición de meta-prompt y el prompt que os escribió el asistente.
- Las cuatro respuestas evaluadas, como enlace compartido o captura completa.
- La tabla de puntuaciones con vuestros criterios.
- La verificación con sus fuentes y la comprobación de vuestro grupo.
- Una conclusión (máximo 150 palabras) apoyada en **vuestra** tabla.
