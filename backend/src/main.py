# ============================================================
# ARQUIVO: main.py
# O QUE FAZ: liga o servidor Flask.
# Rodar com: python main.py
# ============================================================

# Flask = framework web
# CORS = libera o site (porta 5173) a conversar com a API (5000)
from flask import Flask
from flask_cors import CORS

# Importa o caderno de rotas
from api.routes import bp

# Cria a aplicação
app = Flask(__name__)

# Habilita CORS (senão o navegador bloqueia)
CORS(app)

# Liga as rotas com prefixo /api
app.register_blueprint(bp, url_prefix="/api")

# Este 'if' garante que o servidor só roda quando executamos
# o arquivo diretamente (e não quando é importado)
if __name__ == "__main__":
    app.run(debug=True, port=5000)