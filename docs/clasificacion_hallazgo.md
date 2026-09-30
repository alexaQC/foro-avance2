# Clasificación del hallazgo

## Hallazgo
La funcionalidad de vista previa enriquecida mostraba contenido enviado por el usuario dentro de una plantilla Jinja utilizando el filtro `| safe`
Semgrep detectó el problema en:

`app/vista_previa_resena.py`

```html
<div class="contenido">{{ contenido_formateado | safe }}</div>
```

## Tipo
Cross-Site Scripting (XSS) — CWE-79
El contenido enviado por el usuario podía mostrarse como HTML sin aplicar el escape automático de Jinja debido al uso de | safe


## Severidad
Alta
Un usuario podía enviar contenido HTML o JavaScript malicioso que podía ejecutarse al mostrar la vista previa. La explotación era relativamente fácil porque solo era necesario enviar contenido especialmente preparado a la funcionalidad vulnerable.


## ¿Falso positivo?
No
Semgrep detectó un problema real, el contenido provenía de request.form, se procesaba y después se mostraba utilizando | safe, por lo que la ruta vulnerable sí existía en la aplicación.


## Contención inmediata
El parche vulnerable se mantuvo únicamente en QA y no se pasó a producción, el pipeline detectó el problema y bloqueó el despliegue mientras se preparaba la corrección.


## Prevención
Se eliminó el uso de `| safe` sobre el contenido enviado por el usuario, el texto ahora se escapa antes de mostrarse y solo se agrega el formato permitido de forma controlada.
Después de la corrección, Semgrep dejó de detectar la vulnerabilidad y el pipeline pasó en verde.