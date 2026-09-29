#!/usr/bin/env bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORTES="$ROOT/reportes"

FALLO_CONTROLES=0

echo ""
echo "--------------------------------------------------"
echo "ETAPA FINAL A - SAST CON BANDIT"
echo "Umbral: bloquea hallazgos de severidad HIGH"
echo "--------------------------------------------------"

BANDIT="$HOME/qa-tools/bin/bandit"

if [ ! -x "$BANDIT" ]; then
    echo "[BLOQUEO] Bandit no esta disponible."
    FALLO_CONTROLES=1
else
    if "$BANDIT" -r "$ROOT/app" -lll -f txt \
        > "$REPORTES/bandit.txt" 2>&1
    then
        cat "$REPORTES/bandit.txt"
        echo "[OK] Bandit no encontro hallazgos HIGH."
    else
        cat "$REPORTES/bandit.txt"
        echo "[BLOQUEO] Bandit encontro hallazgos HIGH."
        FALLO_CONTROLES=1
    fi
fi

echo ""
echo "--------------------------------------------------"
echo "ETAPA FINAL B - SAST CON SEMGREP"
echo "Umbral: bloquea el uso inseguro de Jinja | safe"
echo "--------------------------------------------------"

if sudo docker run --rm \
    -v "$ROOT:/src" \
    semgrep/semgrep \
    semgrep \
    --error \
    --config /src/pipeline/reglas/xss_jinja_safe.yml \
    /src/app \
    > "$REPORTES/semgrep.txt" 2>&1
then
    cat "$REPORTES/semgrep.txt"
    echo "[OK] Semgrep no encontro el patron inseguro."
else
    cat "$REPORTES/semgrep.txt"
    echo "[BLOQUEO] Semgrep detecto contenido dinamico renderizado con | safe."
    FALLO_CONTROLES=1
fi

echo ""
echo "--------------------------------------------------"
echo "ETAPA FINAL C - SCA CON PIP-AUDIT"
echo "Umbral: bloquea dependencias con vulnerabilidades conocidas"
echo "--------------------------------------------------"

if sudo docker run --rm \
    -v "$ROOT:/src" \
    -w /src \
    python:3.12.10-slim-bookworm \
    sh -c "pip install --quiet pip-audit && pip-audit -r app/requirements.txt" \
    > "$REPORTES/pip_audit.txt" 2>&1
then
    cat "$REPORTES/pip_audit.txt"
    echo "[OK] pip-audit no encontro vulnerabilidades conocidas."
else
    cat "$REPORTES/pip_audit.txt"
    echo "[BLOQUEO] pip-audit encontro dependencias vulnerables."
    FALLO_CONTROLES=1
fi

echo ""

exit "$FALLO_CONTROLES"
