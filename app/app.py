import os
import requests

from s3_storage import guardar_publicacion_s3, eliminar_publicacion_s3
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    session,
    render_template_string,
    flash,
    jsonify,
)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "solo-desarrollo"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///foro.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

MODERACION_URL = os.getenv(
    "MODERACION_URL",
    "http://moderacion:5001/moderar"
)


# ---------------------------------------------------
# MODELOS
# ---------------------------------------------------

class Usuario(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )


class Hilo(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    contenido = db.Column(
        db.Text,
        nullable=False
    )

    autor = db.Column(
        db.String(80),
        nullable=False
    )


class Comentario(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    contenido = db.Column(
        db.Text,
        nullable=False
    )

    autor = db.Column(
        db.String(80),
        nullable=False
    )

    hilo_id = db.Column(
        db.Integer,
        db.ForeignKey("hilo.id"),
        nullable=False
    )


class Resena(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    calificacion = db.Column(
        db.Integer,
        nullable=False
    )

    comentario = db.Column(
        db.Text,
        nullable=False
    )

    autor = db.Column(
        db.String(80),
        nullable=False
    )

    hilo_id = db.Column(
        db.Integer,
        db.ForeignKey("hilo.id"),
        nullable=False
    )


# ---------------------------------------------------
# MODERACIÓN
# ---------------------------------------------------

def revisar_contenido(contenido):
    try:

        respuesta = requests.post(
            MODERACION_URL,
            json={
                "contenido": contenido
            },
            timeout=5
        )

        datos = respuesta.json()

        return (
            datos.get("aprobado", False),
            datos.get(
                "motivo",
                "Sin respuesta"
            )
        )

    except Exception:

        return (
            False,
            "No fue posible contactar al servicio de moderación."
        )


# ---------------------------------------------------
# HTML / ESTILOS
# ---------------------------------------------------

ESTILO = """
<style>

body {
    font-family: Arial, sans-serif;
    max-width: 950px;
    margin: 40px auto;
    padding: 0 20px;
    background: #f5f5f5;
}

h1, h2 {
    color: #333;
}

nav {
    background: #333;
    padding: 15px;
    margin-bottom: 25px;
}

nav a {
    color: white;
    margin-right: 15px;
    text-decoration: none;
}

.card {
    background: white;
    padding: 20px;
    margin-bottom: 15px;
    border-radius: 8px;
}

input,
textarea,
select {
    width: 100%;
    padding: 10px;
    margin: 7px 0 15px 0;
    box-sizing: border-box;
}

button {
    background: #333;
    color: white;
    border: none;
    padding: 10px 18px;
    cursor: pointer;
    border-radius: 5px;
}

button:hover {
    opacity: 0.9;
}

.btn-eliminar {
    background: #b42318;
    margin-top: 12px;
}

.mensaje {
    background: #fff3cd;
    padding: 10px;
    margin-bottom: 15px;
}

.estrellas {
    color: #d49b00;
    font-weight: bold;
}

.autor {
    color: #666;
}

</style>
"""


def pagina(contenido):

    mensajes = """
    {% with mensajes = get_flashed_messages() %}

        {% if mensajes %}

            {% for mensaje in mensajes %}

                <div class="mensaje">
                    {{ mensaje }}
                </div>

            {% endfor %}

        {% endif %}

    {% endwith %}
    """

    nav = """
    <nav>

        <a href="/">
            Inicio
        </a>

        {% if session.get("usuario") %}

            <a href="/nuevo">
                Nuevo hilo
            </a>

            <a href="/logout">
                Cerrar sesión
            </a>

            <span style="color:white;">
                Usuario: {{ session.get("usuario") }}
            </span>

        {% else %}

            <a href="/registro">
                Registro
            </a>

            <a href="/login">
                Iniciar sesión
            </a>

        {% endif %}

    </nav>
    """

    return ESTILO + nav + mensajes + contenido


# ---------------------------------------------------
# SALUD
# ---------------------------------------------------

@app.get("/salud")
def salud():

    return jsonify({
        "aplicacion": "foro-resenas",
        "estado": "ok"
    })


# ---------------------------------------------------
# INICIO
# ---------------------------------------------------

@app.get("/")
def inicio():

    hilos = Hilo.query.order_by(
        Hilo.id.desc()
    ).all()

    html = pagina("""
    <h1>
        Foro y reseñas
    </h1>

    <p>
        Comparte opiniones, comentarios y calificaciones
        sobre productos o lugares.
    </p>

    {% for hilo in hilos %}

        <div class="card">

            <h2>
                {{ hilo.titulo }}
            </h2>

            <p>
                {{ hilo.contenido }}
            </p>

            <small class="autor">
                Publicado por {{ hilo.autor }}
            </small>

            <br><br>

            <a href="/hilo/{{ hilo.id }}">
                Ver hilo y reseñas
            </a>

            {% if session.get("usuario") == hilo.autor %}

                <form
                    method="POST"
                    action="/eliminar/{{ hilo.id }}"
                    onsubmit="return confirm('¿Seguro que quieres eliminar esta publicación?');"
                >

                    <button
                        type="submit"
                        class="btn-eliminar"
                    >
                        Eliminar publicación
                    </button>

                </form>

            {% endif %}

        </div>

    {% else %}

        <div class="card">
            Todavía no hay publicaciones.
        </div>

    {% endfor %}
    """)

    return render_template_string(
        html,
        hilos=hilos
    )


# ---------------------------------------------------
# REGISTRO
# ---------------------------------------------------

@app.route(
    "/registro",
    methods=["GET", "POST"]
)
def registro():

    if request.method == "POST":

        usuario = request.form.get(
            "usuario",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not usuario or not password:

            flash(
                "Completa todos los campos."
            )

            return redirect(
                url_for("registro")
            )

        existente = Usuario.query.filter_by(
            usuario=usuario
        ).first()

        if existente:

            flash(
                "Ese usuario ya existe."
            )

            return redirect(
                url_for("registro")
            )

        nuevo = Usuario(
            usuario=usuario,
            password=generate_password_hash(
                password
            )
        )

        db.session.add(nuevo)

        db.session.commit()

        flash(
            "Usuario registrado correctamente."
        )

        return redirect(
            url_for("login")
        )

    html = pagina("""
    <div class="card">

        <h1>
            Registro
        </h1>

        <form method="POST">

            <label>
                Usuario
            </label>

            <input
                name="usuario"
                required
            >

            <label>
                Contraseña
            </label>

            <input
                type="password"
                name="password"
                required
            >

            <button type="submit">
                Registrarme
            </button>

        </form>

    </div>
    """)

    return render_template_string(
        html
    )


# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        usuario = request.form.get(
            "usuario",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        encontrado = Usuario.query.filter_by(
            usuario=usuario
        ).first()

        if encontrado and check_password_hash(
            encontrado.password,
            password
        ):

            session["usuario"] = usuario

            return redirect(
                url_for("inicio")
            )

        flash(
            "Usuario o contraseña incorrectos."
        )

    html = pagina("""
    <div class="card">

        <h1>
            Iniciar sesión
        </h1>

        <form method="POST">

            <label>
                Usuario
            </label>

            <input
                name="usuario"
                required
            >

            <label>
                Contraseña
            </label>

            <input
                type="password"
                name="password"
                required
            >

            <button type="submit">
                Entrar
            </button>

        </form>

    </div>
    """)

    return render_template_string(
        html
    )


# ---------------------------------------------------
# LOGOUT
# ---------------------------------------------------

@app.get("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("inicio")
    )


# ---------------------------------------------------
# NUEVO HILO
# ---------------------------------------------------

@app.route(
    "/nuevo",
    methods=["GET", "POST"]
)
def nuevo_hilo():

    if not session.get("usuario"):
        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        titulo = request.form.get(
            "titulo",
            ""
        ).strip()

        contenido = request.form.get(
            "contenido",
            ""
        ).strip()

        if not titulo or not contenido:

            flash(
                "Completa todos los campos."
            )

            return redirect(
                url_for("nuevo_hilo")
            )

        aprobado, motivo = revisar_contenido(
            titulo + " " + contenido
        )

        if not aprobado:

            flash(
                "Publicación rechazada por moderación: "
                + motivo
            )

            return redirect(
                url_for("nuevo_hilo")
            )

        hilo = Hilo(
            titulo=titulo,
            contenido=contenido,
            autor=session["usuario"]
        )

        db.session.add(hilo)

        try:
            db.session.flush()

            guardar_publicacion_s3(
                hilo.id,
                hilo.titulo,
                hilo.contenido,
                hilo.autor
            )

            db.session.commit()

        except Exception as error:
            db.session.rollback()

            flash(
                "No se pudo guardar la publicación en S3: "
                + str(error)
            )

            return redirect(
                url_for("nuevo_hilo")
            )

        flash(
            "Publicación aprobada, guardada en S3 y publicada."
        )

        return redirect(
            url_for("inicio")
        )

    html = pagina("""
    <div class="card">

        <h1>
            Nuevo hilo
        </h1>

        <form method="POST">

            <label>
                Producto o lugar
            </label>

            <input
                name="titulo"
                placeholder="Ejemplo: Cafetería Central"
                required
            >

            <label>
                Tu opinión
            </label>

            <textarea
                name="contenido"
                rows="6"
                required
            ></textarea>

            <button type="submit">
                Enviar a moderación y publicar
            </button>

        </form>

    </div>
    """)

    return render_template_string(
        html
    )


# ---------------------------------------------------
# VER HILO
# ---------------------------------------------------

@app.get(
    "/hilo/<int:hilo_id>"
)
def ver_hilo(hilo_id):

    hilo = Hilo.query.get_or_404(
        hilo_id
    )

    comentarios = Comentario.query.filter_by(
        hilo_id=hilo_id
    ).all()

    resenas = Resena.query.filter_by(
        hilo_id=hilo_id
    ).all()

    html = pagina("""
    <div class="card">

        <h1>
            {{ hilo.titulo }}
        </h1>

        <p>
            {{ hilo.contenido }}
        </p>

        <small class="autor">
            Publicado por {{ hilo.autor }}
        </small>

        {% if session.get("usuario") == hilo.autor %}

            <form
                method="POST"
                action="/eliminar/{{ hilo.id }}"
                onsubmit="return confirm('¿Seguro que quieres eliminar esta publicación?');"
            >

                <button
                    type="submit"
                    class="btn-eliminar"
                >
                    Eliminar publicación
                </button>

            </form>

        {% endif %}

    </div>


    <div class="card">

        <h2>
            Reseñas
        </h2>

        {% for resena in resenas %}

            <p class="estrellas">
                {{ resena.calificacion }} / 5 estrellas
            </p>

            <p>
                {{ resena.comentario }}
            </p>

            <small class="autor">
                {{ resena.autor }}
            </small>

            <hr>

        {% else %}

            <p>
                No hay reseñas todavía.
            </p>

        {% endfor %}


        {% if session.get("usuario") %}

            <form
                method="POST"
                action="/resena/{{ hilo.id }}"
            >

                <label>
                    Calificación
                </label>

                <select name="calificacion">

                    <option value="5">
                        5 estrellas
                    </option>

                    <option value="4">
                        4 estrellas
                    </option>

                    <option value="3">
                        3 estrellas
                    </option>

                    <option value="2">
                        2 estrellas
                    </option>

                    <option value="1">
                        1 estrella
                    </option>

                </select>

                <label>
                    Reseña
                </label>

                <textarea
                    name="comentario"
                    rows="3"
                    required
                ></textarea>

                <button type="submit">
                    Publicar reseña
                </button>

            </form>

        {% endif %}

    </div>


    <div class="card">

        <h2>
            Comentarios
        </h2>

        {% for comentario in comentarios %}

            <p>
                {{ comentario.contenido }}
            </p>

            <small class="autor">
                {{ comentario.autor }}
            </small>

            <hr>

        {% else %}

            <p>
                No hay comentarios todavía.
            </p>

        {% endfor %}


        {% if session.get("usuario") %}

            <form
                method="POST"
                action="/comentario/{{ hilo.id }}"
            >

                <textarea
                    name="contenido"
                    rows="3"
                    placeholder="Escribe un comentario"
                    required
                ></textarea>

                <button type="submit">
                    Agregar comentario
                </button>

            </form>

        {% endif %}

    </div>
    """)

    return render_template_string(
        html,
        hilo=hilo,
        comentarios=comentarios,
        resenas=resenas
    )


# ---------------------------------------------------
# ELIMINAR HILO
# ---------------------------------------------------

@app.post(
    "/eliminar/<int:hilo_id>"
)
def eliminar_hilo(hilo_id):

    if not session.get("usuario"):

        return redirect(
            url_for("login")
        )

    hilo = Hilo.query.get_or_404(
        hilo_id
    )

    if hilo.autor != session["usuario"]:

        flash(
            "No puedes eliminar una publicación que no es tuya."
        )

        return redirect(
            url_for("inicio")
        )

    try:
        eliminar_publicacion_s3(
            hilo_id
        )

        Comentario.query.filter_by(
            hilo_id=hilo_id
        ).delete()

        Resena.query.filter_by(
            hilo_id=hilo_id
        ).delete()

        db.session.delete(hilo)

        db.session.commit()

    except Exception as error:
        db.session.rollback()

        flash(
            "No se pudo eliminar la publicación: "
            + str(error)
        )

        return redirect(
            url_for("inicio")
        )

    flash(
        "Publicación eliminada correctamente."
    )

    return redirect(
        url_for("inicio")
    )


# ---------------------------------------------------
# COMENTARIOS
# ---------------------------------------------------

@app.post(
    "/comentario/<int:hilo_id>"
)
def agregar_comentario(hilo_id):

    if not session.get("usuario"):

        return redirect(
            url_for("login")
        )

    # Confirmar que el hilo existe
    Hilo.query.get_or_404(
        hilo_id
    )

    contenido = request.form.get(
        "contenido",
        ""
    ).strip()

    if not contenido:

        flash(
            "El comentario no puede estar vacío."
        )

        return redirect(
            url_for(
                "ver_hilo",
                hilo_id=hilo_id
            )
        )

    aprobado, motivo = revisar_contenido(
        contenido
    )

    if not aprobado:

        flash(
            "Comentario rechazado: "
            + motivo
        )

        return redirect(
            url_for(
                "ver_hilo",
                hilo_id=hilo_id
            )
        )

    comentario = Comentario(
        contenido=contenido,
        autor=session["usuario"],
        hilo_id=hilo_id
    )

    db.session.add(
        comentario
    )

    db.session.commit()

    flash(
        "Comentario aprobado y publicado."
    )

    return redirect(
        url_for(
            "ver_hilo",
            hilo_id=hilo_id
        )
    )


# ---------------------------------------------------
# RESEÑAS
# ---------------------------------------------------

@app.post(
    "/resena/<int:hilo_id>"
)
def agregar_resena(hilo_id):

    if not session.get("usuario"):

        return redirect(
            url_for("login")
        )

    # Confirmar que el hilo existe
    Hilo.query.get_or_404(
        hilo_id
    )

    comentario = request.form.get(
        "comentario",
        ""
    ).strip()

    if not comentario:

        flash(
            "La reseña no puede estar vacía."
        )

        return redirect(
            url_for(
                "ver_hilo",
                hilo_id=hilo_id
            )
        )

    try:

        calificacion = int(
            request.form.get(
                "calificacion",
                5
            )
        )

    except ValueError:

        calificacion = 5

    if calificacion not in [
        1,
        2,
        3,
        4,
        5
    ]:

        flash(
            "La calificación debe estar entre 1 y 5."
        )

        return redirect(
            url_for(
                "ver_hilo",
                hilo_id=hilo_id
            )
        )

    aprobado, motivo = revisar_contenido(
        comentario
    )

    if not aprobado:

        flash(
            "Reseña rechazada: "
            + motivo
        )

        return redirect(
            url_for(
                "ver_hilo",
                hilo_id=hilo_id
            )
        )

    resena = Resena(
        calificacion=calificacion,
        comentario=comentario,
        autor=session["usuario"],
        hilo_id=hilo_id
    )

    db.session.add(
        resena
    )

    db.session.commit()

    flash(
        "Reseña aprobada y publicada."
    )

    return redirect(
        url_for(
            "ver_hilo",
            hilo_id=hilo_id
        )
    )


# ---------------------------------------------------
# CREAR TABLAS
# ---------------------------------------------------

with app.app_context():

    db.create_all()


# ---------------------------------------------------
# INICIO DE LA APP
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )