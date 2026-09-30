# Evidencia de Producción

## Instancia de Producción

La versión remediada de la aplicación fue promovida a una instancia EC2 nueva después de que el pipeline de QA terminó correctamente en verde.

Datos de la instancia:

- Nombre: `foro-produccion`
- Instance ID: `i-025b4c0e2790ca97f`
- Región: `us-east-1`
- Zona de disponibilidad: `us-east-1b`
- IPv4 pública: `34.202.166.103`
- IPv4 privada: `172.31.20.177`
- Tipo de instancia: `t3.micro`

Esta instancia es diferente a la instancia utilizada como QA durante el Avance 2.

## Código desplegado

La instancia de Producción utiliza la rama `produccion`.

La rama fue actualizada después de que el código remediado pasó satisfactoriamente el pipeline completo en QA.

El commit promovido fue:

`b62d24d - evidencia de pipeline verde`

La remediación principal del hallazgo XSS se encuentra en:

`9be3797 - Remediar XSS en vista previa enriquecida`

## Estado de la aplicación

Los servicios se ejecutan mediante Docker Compose:

- `foro_app`
- `foro_moderacion`

El endpoint `GET /salud` respondió correctamente con:

```json
{"aplicacion":"foro-resenas","estado":"ok"}
```

## Base de datos y almacenamiento

Producción utiliza PostgreSQL en Amazon RDS mediante la variable `DATABASE_URL`.

No se utilizó SQLite como base de datos de Producción.

La aplicación conserva también la configuración del bucket S3 utilizado por el proyecto.

## Aplicación accesible desde Producción

La aplicación fue comprobada desde un navegador utilizando:

`http://34.202.166.103:5000`

Se verificó que la pantalla principal del foro y las vistas de los hilos cargan correctamente desde la nueva instancia.

## Evidencia visual

Se conservaron capturas de:

1. La nueva instancia EC2 `foro-produccion`.
2. La terminal de Producción mostrando la rama `produccion`, el commit desplegado, los contenedores y `/salud`.
3. La aplicación Foro y reseñas funcionando desde la IP pública de Producción.
