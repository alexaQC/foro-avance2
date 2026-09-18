import json
import os

import boto3


AWS_REGION = os.getenv(
    "AWS_REGION",
    "us-east-1"
)

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    ""
)


def cliente_s3():
    return boto3.client(
        "s3",
        region_name=AWS_REGION
    )


def guardar_publicacion_s3(
    hilo_id,
    titulo,
    contenido,
    autor
):
    if not S3_BUCKET:
        return False

    datos = {
        "id": hilo_id,
        "titulo": titulo,
        "contenido": contenido,
        "autor": autor
    }

    nombre_objeto = (
        f"publicaciones/hilo_{hilo_id}.json"
    )

    cliente_s3().put_object(
        Bucket=S3_BUCKET,
        Key=nombre_objeto,
        Body=json.dumps(
            datos,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8"),
        ContentType="application/json",
        ServerSideEncryption="AES256"
    )

    return True


def eliminar_publicacion_s3(hilo_id):
    if not S3_BUCKET:
        return False

    nombre_objeto = (
        f"publicaciones/hilo_{hilo_id}.json"
    )

    cliente_s3().delete_object(
        Bucket=S3_BUCKET,
        Key=nombre_objeto
    )

    return True