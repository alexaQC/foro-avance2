"""
PARCHE - Nueva funcionalidad: vista previa con formato enriquecido
Tema: Foro y resenas

Producto pide: que el moderador vea la resena YA formateada (negritas,
saltos de linea, enlaces) antes de aprobarla, en vez de texto plano.
"""

from flask import Blueprint, request, render_template_string
from markupsafe import Markup, escape


vista_previa_bp = Blueprint("vista_previa", __name__)


PLANTILLA = """
<div class="resena-preview">
  <h3>Vista previa de la resena #{{ resena_id }}</h3>
  <div class="contenido">{{ contenido_formateado }}</div>
</div>
"""


def formatear_texto_enriquecido(texto_original):
    """
    Escapa primero el contenido controlado por el usuario y después agrega
    únicamente el formato HTML permitido por la aplicación.
    """

    formateado = str(escape(texto_original))

    partes = formateado.split("**")

    resultado = []

    for indice, parte in enumerate(partes):
        if indice % 2 == 1:
            resultado.append(f"<b>{parte}</b>")
        else:
            resultado.append(parte)

    formateado = "".join(resultado)
    formateado = formateado.replace("\n", "<br>")

    return Markup(formateado)


@vista_previa_bp.route(
    "/moderacion/resenas/<int:resena_id>/vista-previa",
    methods=["POST"],
)
def vista_previa_resena(resena_id):
    """Muestra al moderador la resena con el formato enriquecido aplicado."""

    contenido_original = request.form.get("contenido", "")
    contenido_formateado = formatear_texto_enriquecido(contenido_original)

    return render_template_string(
        PLANTILLA,
        resena_id=resena_id,
        contenido_formateado=contenido_formateado,
    )
