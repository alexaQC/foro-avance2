# Tabla de decisiones de mi pipeline

Este documento es el corazon de la entrega: no se califica cuantos controles
pusiste, sino que puedas justificar cada uno.


## Riesgos que introduce MI aplicacion

| # | Riesgo concreto de mi aplicación | Control que lo cubre | Por qué ese control |
|---|---|---|---|
| 1 | Exponer credenciales de AWS, RDS u otros secretos | Trivy Secret Scanner | Detecta credenciales o secretos incrustrados antes de que lleguen al repositorio |
| 2 | Tener configuraciones inseguras en Terraform o Docker | Trivy Config | Revisa la infraestructura y los Dockerfiles antes del despliegue |
| 3 | Introducir código inseguro en Python | Bandit | Analiza el código Python y detecta patrones relacionados con problemas de seguridad |
| 4 | Renderizar contenido del usuario de forma insegura y permitir XSS | Semgrep | Detecta el patrón inseguro utilizado en la vista previa, como el uso de `| safe` sobre contenido dinámico |
| 5 | Utilizar dependencias con vulnerabilidades conocidas | pip-audit | Revisa las versiones instaladas de las dependencias de Python |
| 6 | Desplegar una aplicación que no funciona correctamente | Health check con `curl` | Comprueba que el endpoint `/salud` responda correctamente |
| 7 | No tener un inventario de los componentes utilizados | SBOM CycloneDX | Permite identificar las dependencias y componentes utilizados por la aplicación |


## Mis etapas y sus umbrales

| Etapa | Herramienta | Qué revisa | Umbral que bloquea | Por qué |
|---|---|---|---|---|
| Secretos | Trivy Secret Scanner | Credenciales y secretos en el repositorio | Cualquier secreto encontrado | Una credencial expuesta puede comprometer los servicios utilizados por la aplicación |
| Configuración | Trivy Config | Terraform y Dockerfiles | Hallazgos HIGH o CRITICAL | Son configuraciones con mayor impacto potencial en la seguridad |
| SAST | Bandit | Código Python | Hallazgos HIGH | Los problemas de severidad alta deben corregirse antes del despliegue |
| Regla XSS | Semgrep | Patrones inseguros en el código | Cualquier hallazgo de la regla configurada | El hallazgo puede indicar que contenido controlado por el usuario se está mostrando de forma insegura |
| SCA | pip-audit | Dependencias de Python | Vulnerabilidades conocidas encontradas | No se debe promover una versión que utilice dependencias conocidas como vulnerables |
| Salud | `curl` | Endpoint `/salud` | Si el endpoint no responde correctamente | La aplicación debe estar funcionando antes de permitir el despliegue |
| SBOM | CycloneDX | Componentes y dependencias | Si no se genera el SBOM | Permite conservar un inventario de los componentes utilizados |



## Lo que decidi NO cubrir

| Riesgo que dejo fuera | Por qué lo dejo fuera | Qué haría si tuviera más tiempo |
|---|---|---|
| Uso de una clave KMS propia para S3 | El proyecto utiliza cifrado SSE-S3 y no era un requisito implementar una clave propia | Configuraría una clave KMS administrada específicamente para el proyecto |
| Pruebas DAST completas dentro de este pipeline | Se priorizaron los controles requeridos para código, dependencias, secretos e infraestructura | Agregaría un escaneo DAST automatizado de la aplicación web |