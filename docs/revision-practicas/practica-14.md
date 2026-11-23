---
search:
  exclude: true
hide:
  - navigation
---

# Práctica 14. Tu laboratorio de IA local

**Módulo:** [14. IA en tu ordenador: LM Studio y Ollama](../14-ia-local.md) · [Normas comunes de las prácticas](index.md)

**Objetivo:** instalar y configurar LM Studio, medir el rendimiento real de tu equipo y comprobar cómo influyen los ajustes de carga, los de muestreo y el uso de documentos.

## Tu variante (pareja de modelos que vas a comparar)

| N.º | Modelo A | Modelo B |
|---|---|---|
| 1 | Gemma 4 E2B en Q4_K_M | Gemma 4 E2B en Q8_0 |
| 2 | Qwen3 4B en Q4_K_M | Qwen3 4B en Q8_0 |
| 3 | Gemma 4 E2B en Q4_K_M | Gemma 4 E4B en Q4_K_M |
| 4 | Qwen3 1.7B en Q4_K_M | Qwen3 4B en Q4_K_M |
| 5 | Gemma 4 E4B en Q4_K_M | Qwen3 4B en Q4_K_M |
| 6 | Qwen3 4B en Q4_K_M | Qwen3 8B en Q4_K_M |

## Tareas

1. **Tu equipo.** Captura la pantalla **Ajustes → Hardware** de LM Studio y anota la memoria total y la utilizable como VRAM.
2. **Carga.** Descarga los dos modelos de tu variante. Para cada uno, abre los ajustes de carga manuales y anota la **memoria estimada** con un contexto de 4 096 tokens y con uno de 32 768. ¿Cuánto crece? ¿Por qué?
3. **Benchmark.** Con temperatura 0, haz a cada modelo las **cinco preguntas del benchmark** (están más abajo), **tres veces cada una**. Antes, desactiva el botón **Think** si tu modelo lo tiene. Anota en una hoja de cálculo el tiempo hasta el primer token y los tokens por segundo de cada ejecución, y calcula las medias. Haz una gráfica con las medias.
4. **Muestreo.** Con el modelo que prefieras, pide «el principio de un cuento sobre [el objeto que te diga el profesor]» con temperatura 0,2, 1 y 1,6, y después con temperatura 1 y Top K 1. Copia las cuatro respuestas y describe las diferencias.
5. **Documentos.** Guarda el **reglamento del planetario** (más abajo) en un archivo de texto, adjúntalo al chat y responde con el modelo a las cinco preguntas que lo acompañan. Haz además **una pregunta cuya respuesta no esté en el documento**. ¿Qué hace el modelo? ¿Se lo inventa? Comprueba tú cada respuesta en el reglamento.
6. **Preset.** Crea un *preset* con un *System Prompt* para un uso tuyo real (tutor de una asignatura, corrector de tus redacciones…) y guárdalo.

## Material: las cinco preguntas del benchmark

1. Explica en tres frases qué es la fotosíntesis.
2. Escribe una lista de cinco consejos para estudiar mejor.
3. Traduce al inglés: «Mañana tenemos examen de Historia a primera hora».
4. Si un tren sale a las 9:40 y tarda 2 horas y 35 minutos, ¿a qué hora llega? Explica el cálculo.
5. Escribe un poema de cuatro versos sobre la lluvia.

## Material: el reglamento del planetario

Crea un archivo llamado `reglamento-planetario.txt` (en Mac, con **TextEdit** → *Formato → Convertir a texto normal*; en Windows, con el **Bloc de notas**), copia dentro este texto y guárdalo. Es un documento inventado: el modelo no puede conocer las respuestas si no lo lee.

```text
REGLAMENTO DE USO DEL PLANETARIO MUNICIPAL DE VALDEMORA DEL RÍO

Artículo 1. Horario. El Planetario abre de martes a domingo. De octubre a mayo, de 10.15 a 19.45 h;
de junio a septiembre, de 11.00 a 21.30 h. Permanece cerrado los lunes, el 1 de enero, el 24 de junio
(fiesta local de San Juan de la Vega) y el 25 de diciembre.

Artículo 2. Sesiones de cúpula. Hay cuatro sesiones diarias: «Viaje a Proxima» (11.30 h), «El cielo de
los íberos» (13.00 h), «Tormentas solares» (17.15 h) y «Noche de Valdemora» (18.45 h, solo viernes y
sábados). Cada sesión dura 42 minutos y el aforo máximo de la cúpula es de 86 personas.

Artículo 3. Tarifas. Entrada general: 6,40 €. Reducida (menores de 14 años, mayores de 65, carné
joven): 3,90 €. Grupos escolares a partir de 15 alumnos: 2,75 € por alumno, con un docente gratis por
cada 12 alumnos. La entrada es gratuita para todo el público el primer miércoles de cada mes.

Artículo 4. Grupos. Los grupos deben reservar con al menos 9 días de antelación en el teléfono
912 555 041 o en el correo reservas@planetario-valdemora.example. Un grupo que llegue más de 10 minutos
tarde pierde la sesión y no se devuelve el importe.

Artículo 5. Normas en la cúpula. No se permite comer, beber ni usar flashes. Los teléfonos deben ir en
«modo avión». Los menores de 8 años deben ir acompañados de un adulto. No se permite la entrada una vez
empezada la sesión.

Artículo 6. Telescopio solar. Los sábados de 12.00 a 14.00 h, si el cielo está despejado, se instala en
la terraza un telescopio solar con filtro H-alfa. Es gratuito con la entrada y hay turnos de 3 minutos
por persona.

Artículo 7. Accesibilidad. La cúpula tiene 6 plazas para sillas de ruedas y bucle magnético para
audífonos. Las sesiones de los domingos a las 11.30 h incluyen interpretación en lengua de signos.

Artículo 8. Objetos perdidos. Se guardan en la taquilla durante 30 días. Pasado ese plazo, se entregan
al Ayuntamiento.
```

**Las cinco preguntas sobre el reglamento:**

1. ¿Cuánto pagaría un grupo de 24 alumnos con 3 profesores?
2. ¿Qué sesión es solo los fines de semana y a qué hora?
3. ¿Con cuántos días de antelación hay que reservar para un grupo?
4. ¿Qué día de junio cierra el planetario y por qué?
5. ¿Qué sesión tiene interpretación en lengua de signos?

## Entregables

- Capturas completas de los apartados 1, 2, 5 y 6.
- La hoja de cálculo con las mediciones y la gráfica.
- Las respuestas del apartado 4.
- Las respuestas del apartado 5, con tu comprobación de cada una (¿acertó el modelo?).
- Un análisis (máximo 250 palabras) que responda, **con tus cifras**: ¿qué modelo elegirías para tu equipo y para qué tarea? ¿Compensa la diferencia de calidad la diferencia de velocidad?

**Defensa posible:** el profesor te pedirá que cargues uno de tus modelos con un contexto concreto y expliques en directo por qué cambia la memoria estimada, o que compares tus cifras con las de un compañero que haya usado el otro tipo de equipo del aula.
