# ADR-001: Decisiones tecnicas de Foro y reseñas

Fecha: 17/09/2026

Estado: aceptada

## Contexto

Estoy construyendo una aplicacion de foro y reseñas donde los usuarios pueden registrarse, iniciar sesion, crear hilos (publicaciones), comentar y dejar calificaciones.
La principal restriccion fue el tiempo, por lo que busque hacerlo cumpliendo unicamente lo que pide las instrucciones sin agregar cosas extra. 

## Decisiones

### 1. Framework del backend

**Elegi:** Flask

**Por que:** Es sencillo, rapido de configurar y suficiente para una aplicacion pequeña como este foro.

**Que descarte y por que:** Descarte FastAPI porque no necesitaba funciones avanzadas de API y Flask era mas rapido de implementar.

### 2. Separacion en servicios

**Elegi:** Dos contenedores propios: uno para la aplicacion principal y otro para el servicio de moderacion.

**Por que:** La moderacion es una funcion separada y asi puede revisar el contenido antes de publicarlo.

**Que descarte y por que:** Descarte crear mas servicios porque aumentaba la complejidad y tiempo de implementación y no eran necesarios para esta actividad.

### 3. Almacenamiento

**Elegi:** RDS para usuarios, publicaciones, comentarios y reseñas, S3 para guardar una copia de las publicaciones.

**Por que:** RDS funciona bien para datos relacionados y S3 permite guardar objetos de forma separada.

**Que descarte y por que:** Descarte guardar todo en archivos locales porque no cumpliria con el uso de AWS.

## Consecuencias

Estas decisiones hicieron mas facil terminar mas rapido y completo. 
La parte mas complicada fue conectar correctamente la aplicacion con RDS, S3 y la instancia EC2, porque habia que configurar permisos, variables y grupos de seguridad. Tambien fue necesario ajustar Gunicorn para que la aplicacion funcionara correctamente en AWS.