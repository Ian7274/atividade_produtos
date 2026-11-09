from flask import Flask, redirect, url_for
from database import DATABASE_PATH, inicializar_banco
from controllers.produto_controller import produto_bp

app = Flask(__name__)

inicializar_banco(DATABASE_PATH)
app.register_blueprint(produto_bp)

@app.route("/", methods=["GET"])
def inicio():
    return redirect(url_for("estoque.listar"))

if __name__ == '__main__':
    app.run(debug=True)