import os
import sqlite3
import threading
import time
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "chave_secreta_natorcida_super_segura"
)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Estado global do jogo em memória
estado_jogo = {
    "time_casa": "Equipe A",
    "gols_casa": 0,
    "time_fora": "Equipe B",
    "gols_fora": 0,
    "minutos": 0,
    "segundos": 0,
    "cronometro_rodando": False,
    "periodo": "1º TEMPO",
    "patrocinadores": ["Marca Patrocinadora 1", "Empresa Parceira 2"],
    "animar_gol": False,
}


# Inicialização do Banco de Dados SQLite para Usuários
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


class User(UserMixin):

    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1])
    return None


# Thread do Cronômetro Automático
def thread_cronometro():
    global estado_jogo
    while True:
        if estado_jogo.get("cronometro_rodando", False):
            time.sleep(1)
            if estado_jogo.get("cronometro_rodando", False):
                estado_jogo["segundos"] += 1
                if estado_jogo["segundos"] >= 60:
                    estado_jogo["segundos"] = 0
                    estado_jogo["minutos"] += 1
        else:
            time.sleep(0.5)


t = threading.Thread(target=thread_cronometro, daemon=True)
t.start()


# Rotas de Autenticação
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1])
            login_user(user)
            return redirect(url_for("controle"))
        else:
            flash("Usuário ou senha incorretos.")

    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Preencha todos os campos!")
        return redirect(url_for("login"))

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        conn.close()
        flash("Conta criada com sucesso! Faça login.")
    except sqlite3.IntegrityError:
        flash("Este nome de usuário já existe.")

    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Rota do Painel de Controle (Protegida por Login)
@app.route("/")
@login_required
def controle():
    return render_template("controle.html")


# Rota do OBS (Aberta para carregar direto sem senha)
@app.route("/obs")
def obs():
    return render_template("placar.html")


# APIs de Estado do Jogo
@app.route("/api/estado", methods=["GET"])
def get_estado():
    return jsonify(estado_jogo)


@app.route("/api/atualizar", methods=["POST"])
def atualizar_estado():
    global estado_jogo
    dados = request.json

    if (
        "gols_casa" in dados
        and int(dados["gols_casa"]) > estado_jogo["gols_casa"]
    ) or (
        "gols_fora" in dados
        and int(dados["gols_fora"]) > estado_jogo["gols_fora"]
    ):
        estado_jogo["animar_gol"] = True

    for chave in dados:
        if chave in estado_jogo:
            estado_jogo[chave] = dados[chave]

    return jsonify({"status": "sucesso", **estado_jogo})


@app.route("/api/desativar_animacao", methods=["POST"])
def desativar_animacao():
    global estado_jogo
    estado_jogo["animar_gol"] = False
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)