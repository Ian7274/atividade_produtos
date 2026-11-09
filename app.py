from flask import Flask
from database import inicializar_banco
from controllers.produto_controller import produto_bp

app = Flask(__name__)

app.register_blueprint(produto_bp)

@app.route("/", methods=["GET"])
def inicio():
    pass

if __name__ == '__main__':
    app.run(debug=True)