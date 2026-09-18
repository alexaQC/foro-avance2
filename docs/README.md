# Foro y reseñas

> Avance 2 del Reto - LSCA2314 - Periodo AD26

> Alumno: Alexandra Quintanilla | Matricula: 2976101 | Tema elegido: 4 - Foro y reseñas

## Que hace esta aplicacion

Es una aplicacion donde los usuarios pueden registrarse, iniciar sesion, crear publicaciones (hilos), comentar y dejar reseñas con calificacion.
Antes de publicar contenido, este pasa por un servicio de moderacion que decide si se aprueba o se rechaza.

## Como se levanta

```bash
docker compose up --build
```

La aplicacion queda en http://localhost:5000 y su endpoint de salud responde en `/salud`.

## Arquitectura

La aplicacion usa dos contenedores: uno contiene el foro principal y otro el servicio de moderacion. El foro envia el contenido al servicio de moderacion antes de publicarlo. Los datos principales se guardan en RDS y las publicaciones tambien se almacenan en S3.

Ver el diagrama en `docs/diagrama_arquitectura.png`.

## Servicios de AWS que usa

| Servicio | Para que lo uso | Como lo asegure |
|---|---|---|
| S3 | Guardar una copia de las publicaciones | Cifrado SSE-S3 y bloqueo de acceso publico |
| RDS | Guardar usuarios, publicaciones, comentarios y reseñas | Cifrado, sin acceso publico y acceso limitado por grupo de seguridad |

## Requisitos minimos del tema

| Requisito de mi tema | Donde se cumple |
|---|---|
| Foro con hilos, comentarios y reseñas | `app/app.py` |
| Servicio de moderacion antes de publicar | `app/moderacion.py` |
| Registro e inicio de sesion | `app/app.py` |
| Endpoint de salud | `/salud` |
| Dos contenedores propios | `docker-compose.yml` |
| S3 real, privado y cifrado | AWS S3 |
| RDS real, cifrada y sin acceso publico | AWS RDS |
| Infraestructura como codigo | `infra/main.tf` |
| Cero credenciales en el codigo | `.env` y `.gitignore` |

## Como se corre el pipeline

```bash
chmod +x pipeline/run_pipeline.sh
./pipeline/run_pipeline.sh
```

El pipeline revisa secretos, configuraciones de Terraform y Docker, el health check de la aplicacion y genera un SBOM en formato CycloneDX.
Si alguna etapa supera su umbral, el resultado es:

`DECISION FINAL: DESPLIEGUE BLOQUEADO`

Si todas las etapas pasan, el resultado es:

`DECISION FINAL: DESPLIEGUE PERMITIDO`