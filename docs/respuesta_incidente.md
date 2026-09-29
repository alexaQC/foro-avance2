# Respuesta al incidente

## Contención inmediata

La medida inmediata sería deshabilitar temporalmente la funcionalidad de vista previa enriquecida en el ambiente de QA mientras se prepara la corrección definitiva.

La funcionalidad vulnerable no debe promoverse a Producción mientras el pipeline continúe detectando el uso inseguro del filtro `safe`.

Como medida operativa temporal también se puede bloquear el acceso al endpoint:

`POST /moderacion/resenas/<resena_id>/vista-previa`

hasta que el código sea remediado y vuelva a pasar correctamente los controles de seguridad.

La contención busca impedir que el contenido no confiable llegue a renderizarse de manera insegura mientras se prepara la corrección definitiva.

## Prevención

La prevención consiste en corregir la causa raíz en el código, manteniendo la funcionalidad de vista previa enriquecida pero evitando renderizar directamente contenido controlado por el usuario mediante `| safe`.

La corrección debe:

1. Mantener el formato permitido de la vista previa.
2. Sanitizar el contenido generado antes de renderizarlo.
3. Permitir únicamente etiquetas HTML explícitamente autorizadas.
4. Eliminar atributos o etiquetas capaces de ejecutar JavaScript.
5. Mantener activo el control de Semgrep dentro del pipeline para evitar que vuelva a introducirse un uso inseguro equivalente.

La remediación se validará nuevamente en QA mediante el pipeline completo.

Solo cuando el pipeline termine con:

`DECISION FINAL: DESPLIEGUE PERMITIDO`

la versión corregida será promovida a la instancia nueva de Producción.

## Diferencia entre contención y prevención

La contención es una medida temporal para detener el riesgo mientras se prepara el arreglo.

La prevención es el cambio permanente en el código que elimina la causa raíz de la vulnerabilidad.

En este proyecto, la contención consiste en impedir temporalmente el uso de la vista previa vulnerable, mientras que la prevención consistirá en sanitizar correctamente el HTML antes de renderizarlo y mantener el control automático dentro del pipeline.
