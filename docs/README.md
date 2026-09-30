# Foro y reseñas

> Entrega Final del Reto - LSCA2314 - Periodo AD26

> Alumno: Stephani Alexandra Quintanilla Cervantes | Matrícula: 2976101 | Tema elegido: 4 - Foro y reseñas

## Qué hace esta aplicación

Es una aplicación de foro y reseñas donde los usuarios pueden registrarse, iniciar sesión, crear publicaciones (hilos), comentar y dejar reseñas con calificación.
La aplicación también cuenta con un servicio separado de moderación que revisa contenido antes de publicarlo.
Para la Entrega Final se agregó una funcionalidad de vista previa enriquecida para moderación. Durante las pruebas en QA, el pipeline detectó una vulnerabilidad XSS en esta función, el problema fue corregido antes de pasar el código a producción.

## Cómo se levanta

```bash
docker compose up --build
```

La aplicacion queda en http://localhost:5000 y su endpoint de salud responde en `/salud`.

## Arquitectura

La aplicación utiliza dos contenedores propios:
- foro_app: aplicación principal desarrollada con Flask y Gunicorn.
- foro_moderacion: servicio separado de moderación.
Los datos principales se almacenan en PostgreSQL mediante Amazon RDS y la aplicación también utiliza Amazon S3 para almacenamiento relacionado con el proyecto.
Para la Entrega Final se utilizaron dos ambientes separados:
- QA: instancia EC2 utilizada para probar el parche, ejecutar el pipeline y realizar la remediación.
- Producción: instancia EC2 nueva que recibió únicamente el código corregido después de que el pipeline terminó correctamente.

Ver el diagrama en: `docs/diagrama_arquitectura.png`

## Servicios de AWS que usa

| Servicio | Uso | Seguridad |
|---|---|---|
| EC2 | Ejecutar la aplicación con Docker Compose | Grupos de seguridad y acceso controlado |
| RDS PostgreSQL | Usuarios, publicaciones, comentarios y reseñas | Cifrado, sin acceso público y acceso limitado |
| S3 | Almacenamiento utilizado por la aplicación | Bucket privado, cifrado y bloqueo de acceso público |

## Requisitos minimos del tema

| Requisito | Dónde se cumple |
|---|---|
| Foro con hilos, comentarios y reseñas | `app/app.py` |
| Servicio de moderación | `app/moderacion.py` |
| Vista previa enriquecida | `app/vista_previa_resena.py` |
| Registro e inicio de sesión | `app/app.py` |
| Endpoint de salud | `/salud` |
| Dos contenedores propios | `docker-compose.yml` |
| Amazon S3 | AWS S3 |
| PostgreSQL en Amazon RDS | AWS RDS |
| Infraestructura como código | `infra/main.tf` |
| Credenciales fuera del código | `.env` y `.gitignore` |

## Como se corre el pipeline

```bash
chmod +x pipeline/run_pipeline.sh
./pipeline/run_pipeline.sh
```

El pipeline incluye controles de seguridad y validación con:
- Trivy para secretos y configuraciones.
- Bandit para análisis estático de seguridad en Python.
- Semgrep para detectar patrones inseguros en el código.
- pip-audit para revisar vulnerabilidades conocidas en dependencias.
- Health check de la aplicación.
- Generación de SBOM en formato CycloneDX.

Si alguna etapa supera su umbral de seguridad, el pipeline muestra:
DECISION FINAL: DESPLIEGUE BLOQUEADO

Si todas las etapas pasan correctamente:
DECISION FINAL: DESPLIEGUE PERMITIDO

## Hallazgo de la Entrega Final
Semgrep detectó un posible Cross-Site Scripting (XSS) asociado a CWE-79 en:
app/vista_previa_resena.py

El problema era el uso de: {{ contenido_formateado | safe }}
La vulnerabilidad fue corregida eliminando el uso inseguro de | safe y haciendo que el contenido enviado por el usuario se muestre como texto seguro antes de aplicar el formato permitido.
