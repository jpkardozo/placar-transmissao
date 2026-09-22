import os
import threading
import time
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Estado inicial do jogo guardado na memória do servidor
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


@app.route("/")
def controle():
    return render_template("controle.html")


@app.route("/obs")
def obs():
    return render_template("placar.html")


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
    # O Render define automaticamente a porta pela variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)