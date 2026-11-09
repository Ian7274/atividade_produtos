from contextlib import closing
from math import isfinite

from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from database import DATABASE_PATH, conectar_banco

produto_bp = Blueprint("estoque", __name__)


@produto_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "GET":
        return render_template("cadastrar.html", valores={})

    nome = request.form.get("nome", "").strip()
    descricao = request.form.get("descricao", "").strip()
    categoria = request.form.get("categoria", "").strip()

    if not nome or len(nome) > 100 or len(categoria) > 50:
        return render_template(
            "cadastrar.html",
            valores=request.form,
            erro="Informe um nome de até 100 caracteres e uma categoria de até 50.",
        ), 400

    try:
        preco = float(request.form.get("preco", ""))
        quantidade = int(request.form.get("quantidade", ""))
    except ValueError:
        return render_template(
            "cadastrar.html",
            valores=request.form,
            erro="Informe um preço e uma quantidade válidos.",
        ), 400

    if not isfinite(preco) or preco < 0 or quantidade < 0:
        return render_template(
            "cadastrar.html",
            valores=request.form,
            erro="Preço e quantidade não podem ser negativos.",
        ), 400

    with closing(conectar_banco(DATABASE_PATH)) as conexao:
        conexao.execute(
            """
            INSERT INTO produtos (nome, descricao, preco, quantidade, categoria)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, descricao, preco, quantidade, categoria),
        )
        conexao.commit()

    return redirect(url_for("estoque.listar", mensagem="Produto cadastrado com sucesso."))


@produto_bp.route("/listar", methods=["GET"])
def listar():
    with closing(conectar_banco(DATABASE_PATH)) as conexao:
        produtos = conexao.execute(
            "SELECT id, nome, descricao, preco, quantidade, categoria "
            "FROM produtos ORDER BY id DESC"
        ).fetchall()

    return render_template(
        "listar.html",
        produtos=produtos,
        mensagem=request.args.get("mensagem"),
    )


@produto_bp.route("/apagar", methods=["POST", "DELETE"])
def apagar():
    if request.method == "DELETE":
        dados = request.get_json()
        produto_id = dados.get("id") if dados else None
    else:
        produto_id = request.form.get("id")

    try:
        produto_id = int(produto_id)
    except (TypeError, ValueError):
        if request.method == "DELETE":
            return jsonify(erro="Informe um ID de produto válido."), 400
        return redirect(url_for("estoque.listar", mensagem="ID de produto inválido."))

    with closing(conectar_banco(DATABASE_PATH)) as conexao:
        cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conexao.commit()

    if cursor.rowcount == 0:
        if request.method == "DELETE":
            return jsonify(erro="Produto não encontrado."), 404
        return redirect(url_for("estoque.listar", mensagem="Produto não encontrado."))

    if request.method == "DELETE":
        return jsonify(mensagem="Produto excluído com sucesso.")
    return redirect(url_for("estoque.listar", mensagem="Produto excluído com sucesso."))