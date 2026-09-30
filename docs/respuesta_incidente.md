# Respuesta al incidente

## Contención inmediata
La contención inmediata consistió en mantener el parche vulnerable únicamente en el ambiente de QA y no pasarlo a producción.

Al ejecutar el pipeline, Semgrep detectó el uso inseguro de `| safe` y el despliegue fue bloqueado con:
`DECISION FINAL: DESPLIEGUE BLOQUEADO`

De esta forma, el código vulnerable permaneció en QA mientras se preparaba la corrección.


## Prevención
La prevención consistió en corregir la causa raíz del problema sin eliminar la funcionalidad de vista previa enriquecida.

Se eliminó el uso inseguro de `| safe` sobre contenido controlado por el usuario y se modificó el procesamiento para que el texto recibido se tratara de forma segura antes de agregar el formato permitido.

La corrección mantuvo funciones como negritas y saltos de línea, pero evitó que contenido HTML o JavaScript enviado por el usuario pudiera interpretarse directamente en la página.

También se mantuvo la regla de Semgrep dentro del pipeline para detectar nuevamente este patrón si llegara a introducirse en el código.

Después de la corrección, el pipeline se ejecutó nuevamente en QA y terminó con:
`DECISION FINAL: DESPLIEGUE PERMITIDO`


## Diferencia entre contención y prevención
La contención fue la medida temporal para evitar que la versión vulnerable avanzara a producción (el bloqueo del pipeline en QA)

La prevención fue el cambio permanente en el código que corrigió la causa del XSS y permitió mantener funcionando la vista previa de forma segura (la corrección del manejo del contenido enviado por el usuario)