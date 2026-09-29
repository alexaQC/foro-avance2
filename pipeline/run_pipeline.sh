#!/usr/bin/env bash

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTES="$ROOT/reportes"
TRIVY_IMAGE="aquasec/trivy:0.67.2"

mkdir -p "$REPORTES"

FALLO=0

echo "=================================================="
echo " PIPELINE DE SEGURIDAD - FORO Y RESEÑAS"
echo "=================================================="
echo ""


# --------------------------------------------------
# CONTROLES DE ENTREGA FINAL - SAST Y SCA
# --------------------------------------------------

echo "--------------------------------------------------"
echo "CONTROLES DE ENTREGA FINAL - SAST Y SCA"
echo "--------------------------------------------------"

if "$ROOT/pipeline/controles_final.sh"
then
    echo "[OK] Controles SAST/SCA completados."
else
    echo "[BLOQUEO] Uno o mas controles SAST/SCA fallaron."
    FALLO=1
fi

echo ""


# --------------------------------------------------
# ETAPA 1 - SECRETOS
# --------------------------------------------------

echo "--------------------------------------------------"
echo "ETAPA 1 - Deteccion de secretos"
echo "Umbral: bloquea si encuentra cualquier secreto"
echo "--------------------------------------------------"

if sudo docker run --rm \
    -v "$ROOT:/src" \
    "$TRIVY_IMAGE" \
    fs \
    --scanners secret \
    --skip-files "/src/.env" \
    --exit-code 1 \
    --no-progress \
    /src \
    > "$REPORTES/trivy_secretos.txt" 2>&1
then
    cat "$REPORTES/trivy_secretos.txt"
    echo "[OK] No se encontraron secretos en el repositorio."
else
    cat "$REPORTES/trivy_secretos.txt"
    echo "[BLOQUEO] Se encontraron secretos."
    FALLO=1
fi

echo ""


# --------------------------------------------------
# ETAPA 2 - IAC Y DOCKER
# --------------------------------------------------

echo "--------------------------------------------------"
echo "ETAPA 2 - Configuracion segura"
echo "Umbral: bloquea con hallazgos HIGH o CRITICAL"
echo "--------------------------------------------------"

if sudo docker run --rm \
    -v "$ROOT:/src" \
    "$TRIVY_IMAGE" \
    config \
    --severity HIGH,CRITICAL \
    --ignorefile /src/.trivyignore \
    --exit-code 1 \
    /src \
    > "$REPORTES/trivy_config.txt" 2>&1
then
    cat "$REPORTES/trivy_config.txt"
    echo "[OK] No hay configuraciones HIGH o CRITICAL."
else
    cat "$REPORTES/trivy_config.txt"
    echo "[BLOQUEO] Existen configuraciones HIGH o CRITICAL."
    FALLO=1
fi

echo ""


# --------------------------------------------------
# ETAPA 3 - SALUD DE LA APLICACION
# --------------------------------------------------

echo "--------------------------------------------------"
echo "ETAPA 3 - Endpoint de salud"
echo "Umbral: bloquea si /salud no responde"
echo "--------------------------------------------------"

if curl -fsS \
    http://localhost:5000/salud \
    > "$REPORTES/salud.txt" 2>&1
then
    cat "$REPORTES/salud.txt"
    echo ""
    echo "[OK] La aplicacion responde correctamente."
else
    cat "$REPORTES/salud.txt"
    echo ""
    echo "[BLOQUEO] La aplicacion no responde en /salud."
    FALLO=1
fi

echo ""


# --------------------------------------------------
# ETAPA 4 - SBOM
# --------------------------------------------------

echo "--------------------------------------------------"
echo "ETAPA 4 - Generacion de SBOM CycloneDX"
echo "Umbral: bloquea si no se puede generar el SBOM"
echo "--------------------------------------------------"

if sudo docker run --rm \
    -v "$ROOT:/src" \
    "$TRIVY_IMAGE" \
    fs \
    --format cyclonedx \
    --output /src/reportes/sbom_cyclonedx.json \
    --no-progress \
    /src
then
    echo "[OK] SBOM generado en reportes/sbom_cyclonedx.json"
else
    echo "[BLOQUEO] No se pudo generar el SBOM."
    FALLO=1
fi

echo ""


# --------------------------------------------------
# DECISION FINAL
# --------------------------------------------------

echo "=================================================="

if [ "$FALLO" -eq 0 ]; then
    echo "DECISION FINAL: DESPLIEGUE PERMITIDO"
    echo "Todas las etapas obligatorias pasaron."
    echo "=================================================="
    exit 0
else
    echo "DECISION FINAL: DESPLIEGUE BLOQUEADO"
    echo "Al menos una etapa supero su umbral de bloqueo."
    echo "=================================================="
    exit 1
fi