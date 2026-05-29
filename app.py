from flask import Flask
from devserver import encontrar_porta_livre, abrir_navegador

app = Flask(__name__)

@app.route("/")
def home():
    return "Servidor funcionando 🚀"

if __name__ == "__main__":

    porta = encontrar_porta_livre()

    abrir_navegador(porta)

    print(f"""
====================================
🚀 Projeto iniciado com sucesso
🌐 URL: http://127.0.0.1:{porta}
====================================
""")

    app.run(port=porta, debug=True)