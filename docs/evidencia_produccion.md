# Evidencia de Producción

## Instancia de Producción

La versión remediada de la aplicación fue promovida a una instancia EC2 nueva después de que el pipeline de QA terminó correctamente en verde.

Datos de la instancia:

- Nombre: `foro-produccion`
- Instance ID: `i-025b4c0e2790ca97f`
- Región: `us-east-1`
- Zona de disponibilidad: `us-east-1b`
- IPv4 pública utilizada durante la evidencia: `34.202.166.103`
- IPv4 privada: `172.31.20.177`
- Tipo de instancia: `t3.micro`

Esta instancia es diferente a la instancia utilizada como ambiente de QA durante el Avance 2.

## Código desplegado

La instancia de producción utiliza la rama `produccion`.

El código solamente fue pasado después de corregir la vulnerabilidad y obtener un resultado exitoso del pipeline en QA.

El commit de aplicación promovido a producción fue:

`b62d24d - evidencia de pipeline verde`

La corrección principal del hallazgo XSS se realizó en:

`9be3797 - Remediar XSS en vista previa enriquecida`

Los commits posteriores en la rama `produccion` corresponden principalmente a documentación y evidencias de la entrega.

## Estado de la aplicación

Los servicios se ejecutaron mediante Docker Compose:

- `foro_app`
- `foro_moderacion`

El endpoint `GET /salud` respondió correctamente con:

```json
{"aplicacion":"foro-resenas","estado":"ok"}
```

Esto confirmó que la aplicación estaba activa en la nueva instancia.


## Base de datos y almacenamiento
La aplicación de producción utiliza PostgreSQL en Amazon RDS mediante la variable DATABASE_URL.
Se verificó que producción no utiliza SQLite como base de datos.
La aplicación mantiene la configuración de Amazon S3 utilizada por el proyecto para el almacenamiento.


## Aplicación funcionando en producción
Durante la toma de evidencias, la aplicación funcionaba en:
http://34.202.166.103:5000
Se verificó que la pantalla principal del foro y las vistas de los hilos cargaran correctamente desde la instancia de producción.


## Evidencia visual
Las capturas de la entrega se encuentran en:
docs/evidencias_final_capturas/