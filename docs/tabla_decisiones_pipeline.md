# Tabla de decisiones de mi pipeline

Este documento es el corazon de la entrega: no se califica cuantos controles
pusiste, sino que puedas justificar cada uno.

## Riesgos que introduce MI aplicacion

| # | Riesgo concreto de mi app | Que control lo cubre | Por que ese control |
|---|---|---|---|
| 1 | Exponer credenciales de AWS o RDS | Trivy Secret Scanner | Detecta secretos antes de que lleguen al repositorio |
| 2 | Tener configuraciones inseguras en AWS o Docker | Trivy Config | Revisa Terraform y Dockerfiles antes del despliegue |
| 3 | Desplegar la aplicacion sin que funcione | Prueba del endpoint Health check (/salud) | Confirma que la aplicacion responde correctamente |
| 4 | No tener registro de los componentes usados | SBOM CycloneDX | Permite conocer las dependencias y componentes de la aplicacion |

## Mis etapas y sus umbrales

| Etapa | Herramienta | Que revisa | Umbral que bloquea | Por que ese umbral |
|---|---|---|---|---|
| Secretos | Trivy Secret Scanner | Credenciales en el repositorio | Cualquier secreto encontrado | Una sola credencial expuesta puede comprometer AWS o RDS |
| Configuracion | Trivy Config | Terraform y Dockerfiles | Hallazgos HIGH o CRITICAL | Son los riesgos que pueden afectar mas la seguridad |
| Salud | curl | Endpoint Health check (/salud) | Si no responde correctamente | No se debe desplegar una aplicacion que no funciona |
| SBOM | Trivy CycloneDX | Componentes de la aplicacion | Si no se genera el SBOM | El inventario de componentes es parte de la evidencia requerida |

## Lo que decidi NO cubrir

| Riesgo que dejo fuera | Por que lo dejo fuera | Que haria si tuviera mas tiempo |
|---|---|---|
| Uso de una clave KMS propia para S3 | El proyecto pide S3 cifrado y se uso SSE-S3 con AES256 | Configuraria una clave KMS administrada por el cliente |
| Pruebas DAST completas | Priorice los controles principales del proyecto | Agregaria un escaneo DAST de la aplicacion web |