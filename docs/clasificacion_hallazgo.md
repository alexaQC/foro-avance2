# Clasificación del hallazgo

## Hallazgo

La nueva funcionalidad de vista previa enriquecida para moderación recibe contenido enviado por el usuario y posteriormente lo renderiza dentro de una plantilla Jinja utilizando el filtro `safe`.

El hallazgo fue detectado por Semgrep en:

`app/vista_previa_resena.py`

Línea detectada:

```html
<div class="contenido">{{ contenido_formateado | safe }}</div>
Semgrep reportó el hallazgo como bloqueante durante la ejecución del pipeline de QA.
Tipo de falla
Cross-Site Scripting (XSS) por renderizado inseguro de contenido controlado por el usuario.
CWE asociado:
CWE-79 — Improper Neutralization of Input During Web Page Generation
La aplicación toma el contenido recibido mediante request.form, lo transforma a HTML y después lo marca explícitamente como seguro mediante el filtro Jinja safe.
Esto evita que Jinja aplique el escape automático de HTML sobre ese contenido.
Severidad
Alta
Justificación de severidad
Impacto
Si un usuario introduce contenido HTML o JavaScript malicioso, ese contenido puede llegar a renderizarse en el navegador del moderador como parte de la vista previa.
Esto podría permitir la ejecución de código JavaScript dentro de la sesión del usuario que visualiza la reseña, afectando la confidencialidad e integridad de la aplicación.
Dependiendo del contexto de sesión y de los permisos del moderador, un atacante podría intentar realizar acciones utilizando la sesión de la víctima o manipular el contenido mostrado.
Facilidad de explotación
La explotación requiere controlar el contenido enviado al endpoint de vista previa.
El código no realiza sanitización HTML antes de utilizar el filtro safe, por lo que el contenido dinámico puede llegar a la plantilla sin una neutralización adecuada.
No se requiere modificar el servidor ni tener acceso al código fuente para aprovechar la falla; basta con enviar contenido especialmente construido a la funcionalidad vulnerable.
Evidencia
Durante la corrida del pipeline en QA, Semgrep detectó:
- Archivo: app/vista_previa_resena.py
- Regla: jinja-safe-en-vista-previa
- Resultado: 1 finding
- Estado: Blocking
- Mensaje: uso de | safe en contenido dinámico con posible XSS
La corrida completa se encuentra en:
reportes/pipeline_bloqueado.txt
El reporte específico se encuentra en:
reportes/semgrep.txt
¿Es un falso positivo?
No.
El hallazgo corresponde directamente al flujo real de la nueva funcionalidad:
1. El contenido llega desde request.form.
2. Se procesa mediante formatear_texto_enriquecido().
3. El resultado se envía a la plantilla.
4. La plantilla utiliza | safe.
5. El contenido deja de recibir el escape automático de Jinja.
Por lo tanto, el patrón reportado por la herramienta sí está presente en una ruta alcanzable de la aplicación y corresponde a una condición real que debe remediarse antes de promover el código a Producción.
EOFSemgrep reportó el hallazgo como bloqueante durante la ejecución del pipeline de QA.
Tipo de falla
Cross-Site Scripting (XSS) por renderizado inseguro de contenido controlado por el usuario.
CWE asociado:
CWE-79 — Improper Neutralization of Input During Web Page Generation
La aplicación toma el contenido recibido mediante request.form, lo transforma a HTML y después lo marca explícitamente como seguro mediante el filtro Jinja safe.
Esto evita que Jinja aplique el escape automático de HTML sobre ese contenido.
Severidad
Alta
Justificación de severidad
Impacto
Si un usuario introduce contenido HTML o JavaScript malicioso, ese contenido puede llegar a renderizarse en el navegador del moderador como parte de la vista previa.
Esto podría permitir la ejecución de código JavaScript dentro de la sesión del usuario que visualiza la reseña, afectando la confidencialidad e integridad de la aplicación.
Dependiendo del contexto de sesión y de los permisos del moderador, un atacante podría intentar realizar acciones utilizando la sesión de la víctima o manipular el contenido mostrado.
Facilidad de explotación
La explotación requiere controlar el contenido enviado al endpoint de vista previa.
El código no realiza sanitización HTML antes de utilizar el filtro safe, por lo que el contenido dinámico puede llegar a la plantilla sin una neutralización adecuada.
No se requiere modificar el servidor ni tener acceso al código fuente para aprovechar la falla; basta con enviar contenido especialmente construido a la funcionalidad vulnerable.
Evidencia
Durante la corrida del pipeline en QA, Semgrep detectó:
- Archivo: app/vista_previa_resena.py
- Regla: jinja-safe-en-vista-previa
- Resultado: 1 finding
- Estado: Blocking
- Mensaje: uso de | safe en contenido dinámico con posible XSS
La corrida completa se encuentra en:
reportes/pipeline_bloqueado.txt
El reporte específico se encuentra en:
reportes/semgrep.txt
¿Es un falso positivo?
No.
El hallazgo corresponde directamente al flujo real de la nueva funcionalidad:
1. El contenido llega desde request.form.
2. Se procesa mediante formatear_texto_enriquecido().
3. El resultado se envía a la plantilla.
4. La plantilla utiliza | safe.
5. El contenido deja de recibir el escape automático de Jinja.
Por lo tanto, el patrón reportado por la herramienta sí está presente en una ruta alcanzable de la aplicación y corresponde a una condición real que debe remediarse antes de promover el código a Producción.
