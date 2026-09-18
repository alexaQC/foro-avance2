from flask import Flask, request, jsonify

app = Flask(__name__)

PALABRAS_BLOQUEADAS = [
    "spam",
    "estafa",
    "idiota",
    "odio"
]


@app.get("/salud")
def salud():
    return jsonify({
        "servicio": "moderacion",
        "estado": "ok"
    })


@app.post("/moderar")
def moderar():
    datos = request.get_json(silent=True) or {}
    contenido = datos.get("contenido", "").strip()

    if not contenido:
        return jsonify({
            "aprobado": False,
            "estado": "rechazado",
            "motivo": "El contenido está vacío."
        }), 400

    contenido_minusculas = contenido.lower()

    for palabra in PALABRAS_BLOQUEADAS:
        if palabra in contenido_minusculas:
            return jsonify({
                "aprobado": False,
                "estado": "rechazado",
                "motivo": f"Contenido marcado por la palabra: {palabra}"
            })

    if len(contenido) > 1000:
        return jsonify({
            "aprobado": False,
            "estado": "rechazado",
            "motivo": "El contenido supera los 1000 caracteres."
        })

    return jsonify({
        "aprobado": True,
        "estado": "aprobado",
        "motivo": "Contenido permitido."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)