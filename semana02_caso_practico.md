# Semana 2 — Caso práctico: la prueba rápida y el teorema de Bayes

Alumno: bambam2907 · Optativa 3 — Ciencia de Datos

## a) Probabilidad de estar enfermo dado un positivo

Eventos: E = tener la enfermedad, S = estar sano, + = la prueba da positivo. Datos: P(E) = 0.01, P(S) = 0.99, sensibilidad P(+|E) = 0.99, especificidad P(-|S) = 0.95, por lo tanto P(+|S) = 1 - 0.95 = 0.05.

Teorema de Bayes: P(E|+) = P(+|E) · P(E) / P(+), con P(+) = P(+|E) · P(E) + P(+|S) · P(S).

Sustituyendo: P(+) = 0.99 · 0.01 + 0.05 · 0.99 = 0.0099 + 0.0495 = 0.0594. Entonces P(E|+) = 0.0099 / 0.0594 = 0.1667, es decir, 16.7 %.

Con frecuencias naturales sobre 10 000 personas el procedimiento se ve directo:

|  | Positivo | Negativo | Total |
|---|---|---|---|
| Enfermos | 99 | 1 | 100 |
| Sanos | 495 | 9 405 | 9 900 |
| Total | 594 | 9 406 | 10 000 |

De los 594 positivos solo 99 están enfermos: 99 / 594 = 16.7 %. El paciente tiene cerca de 5 de 6 probabilidades de estar sano.

## b) Por qué una prueba "99 % precisa" produce tantos falsos positivos

El "99 %" describe la sensibilidad (qué tan bien detecta a los enfermos), no el valor predictivo positivo (qué tan probable es estar enfermo si sales positivo). El 5 % de falsos positivos parece pequeño, pero se aplica a 9 900 sanos y produce 495 falsos positivos, mientras que los enfermos son tan pocos que solo aportan 99 positivos verdaderos. Los sanos son tantos que dominan el grupo de positivos: la mayoría son falsas alarmas aunque la prueba casi nunca falle con un enfermo.

## c) El papel de la probabilidad previa

La prevalencia del 1 % es la probabilidad previa: fija cuántos enfermos hay antes de ver cualquier evidencia. La prueba no da un veredicto, solo actualiza esa creencia para obtener el posterior. Si la enfermedad afectara al 30 % de la población: P(+) = 0.99 · 0.30 + 0.05 · 0.70 = 0.297 + 0.035 = 0.332 y P(E|+) = 0.297 / 0.332 = 0.8946, es decir, 89.5 %. Misma prueba, resultado opuesto. Por eso un positivo se interpreta distinto en la población general que en pacientes con síntomas, donde la previa ya es alta. Si el paciente repite la prueba de forma independiente y vuelve a dar positivo, la previa ahora es 16.7 % y el posterior sube a 0.99 · 0.1667 / (0.99 · 0.1667 + 0.05 · 0.8333) = 0.798, unos 80 %.

## d) Relación con sistemas automáticos de detección

En un antivirus o un filtro de fraude la "enfermedad" (malware, una transacción fraudulenta) es rarísima: la previa es mucho menor que 1 %. Con esa tasa base, hasta un 1 % de falsos positivos genera miles de alertas falsas por cada caso real. Las consecuencias son de ingeniería: fatiga de alertas, clientes legítimos bloqueados, costo de revisión manual y pérdida de confianza en el sistema. Las decisiones también son de ingeniería: elegir el umbral según el costo asimétrico de cada error (precisión contra recall), encadenar una segunda verificación más cara solo para los positivos (como la prueba confirmatoria del hospital), medir la tasa base real en producción y monitorearla, y diseñar la experiencia de usuario para que un positivo sea una revisión y no un veredicto. Bayes dice cuántas falsas alarmas habrá; qué hacer con ellas lo decide el diseño.

Conclusión: un positivo no significa estar enfermo, significa que la probabilidad subió de 1 % a 16.7 %. Antes de entrar en pánico, o de bloquear a un cliente, hay que preguntarse cuál era la tasa base.
