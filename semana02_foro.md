# Semana 2 — Foro de mediación
**Alumno:** bambam2907 · **Optativa 3 — Ciencia de Datos**

## Respuesta inicial

Antes de creer ese titular preguntaría: ¿a cuántos usuarios se encuestó y cómo se seleccionaron? ¿Quiénes fueron invitados y no contestaron? ¿"Prefiere" contra qué alternativa? ¿Cómo estaba redactada la pregunta y quién pagó el estudio? Un 90 % no dice nada sin el **tamaño de muestra**: con n = 20 el **intervalo de confianza** al 95 % para una proporción es 90 % ± 13 puntos, o sea entre 77 % y 100 %; con n = 1000 baja a ± 1.9 puntos. Y aunque n sea grande, si la encuesta se mandó solo a usuarios activos que quisieron responder hay **sesgo de selección** y **sesgo de no respuesta**: quienes desinstalaron la app nunca aparecen en la muestra.

Un caso real: en 2007 la Advertising Standards Authority del Reino Unido prohibió el anuncio "más del 80 % de los dentistas recomienda Colgate". En la encuesta cada dentista podía recomendar varias marcas y una competidora salía casi igual de recomendada, pero el público entendía que 80 % elegía Colgate sobre las demás.

La estadística revela la verdad cuando se reporta n, el método de muestreo, la tasa de respuesta y el intervalo de confianza. Se manipula con muestras autoseleccionadas, omitiendo el margen de error, con preguntas dirigidas, ejes truncados en las gráficas o eligiendo la medida que más conviene.

## Respuesta a compañero 1 (ampliando)

Coincido con tu punto sobre el tamaño de muestra y lo ampliaría con el intervalo de confianza. Para una proporción se calcula como p ± 1.96·√(p(1−p)/n). Con p = 0.9 y n = 20 el margen es de ± 13 puntos, así que el "90 %" en realidad va de 77 % a 100 %; con n = 1000 el margen baja a ± 1.9 puntos. Pero ese margen solo mide el azar del muestreo, no el sesgo. Si se invitó a 1000 usuarios y contestaron 150, la tasa de no respuesta es del 85 %, y quienes responden suelen ser los más contentos: eso es sesgo de no respuesta y ningún n grande lo corrige.

## Respuesta a compañero 2 (cuestionando)

Estoy de acuerdo en parte, pero cuestionaría que el problema sea solo el tamaño de muestra. Aunque encuestaran a 10 000 personas, si solo contestan quienes siguen usando la app hay sesgo de supervivencia: quienes la desinstalaron, que serían los más críticos, no están en la muestra, y el 90 % describe a los sobrevivientes, no a los usuarios. Además, "prefiere" sin alternativa explícita ni definición operativa no es una variable medible: ¿prefiere sobre qué app, para qué tarea? Antes de aceptar la cifra pediría el n, el método de muestreo, la tasa de respuesta, la pregunta textual y el intervalo de confianza.
