# Declaracion de uso de inteligencia artificial

Las Notas de Ensenanza del curso permiten usar IA como apoyo, no como
sustituto. Esta declaracion es obligatoria y forma parte de la entrega.

## Que genere con ayuda de IA

| Parte del proyecto | Herramienta de IA | Que le pedi | Que cambie yo despues |
|---|---|---|---|
| Codigo de la aplicacion | ChatGPT | Ayuda para crear y corregir funciones del foro | Ajuste textos, botones y funciones |
| Docker y AWS | ChatGPT | Pasos para configurar contenedores, EC2, RDS y S3 | Revise los valores y adapte nombres y configuraciones |
| Pipeline | ChatGPT | Ayuda para crear las etapas y los comandos | Cambie umbrales, corregi errores y adapte el pipeline al proyecto |

## Que hice sin IA

Realice algunas configuraciones de AWS, ejecute los comandos, probe la aplicacion, revise los resultados del pipeline y tome/realice las evidencias necesarias.

## Algo que la IA me dio mal y tuve que corregir

En una parte del pipeline se uso la opcion `--no-progress` con un comando de Trivy que no la aceptaba, al ejecutar el pipeline aparecio un error por lo que revise la salida, elimine esa opcion y volvi a ejecutar la prueba hasta obtener correctamente la corrida roja y la corrida verde.