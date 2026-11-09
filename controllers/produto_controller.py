from flask import Blueprint, request, jsonify
from database import conectar_banco

produto = Blueprint("estoque", __name__)

@produto.route("/cadastrar", methods=["POST"])
def cadastrar():
    pass

@produto.route("/listar", methods=["GET"])
def listar():
    pass

@produto.route("/apagar", methods=["DELETE"])
def apagar():
    pass