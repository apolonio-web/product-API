import requests
import json
from flask import Flask, request

app = Flask(__name__)

ERROS = {
    400: "Requisição inválida.",
    401: "Não autorizado.",
    403: "Acesso negado.",
    404: "Produto não encontrado.",
    500: "Erro interno da Fake Store.",
    503: "Serviço temporariamente indisponível."
}

def tratar_resposta(resposta):
    dados = resposta.json()

    if resposta.status_code == 200:
        return dados

    return {
        "erro": ERROS.get(
            resposta.status_code,
            "Erro desconhecido."
        ),
        "status": resposta.status_code
    }, resposta.status_code
    
def obter_produto(id):
    resposta = requests.get(f"https://fakestoreapi.com/products/{id}")

    if resposta.status_code == 200:
        return resposta.json()

    return None    

@app.get("/")
def root():
    return "Seja bem vindo a minha api"

@app.get("/produtos")
def listar_produtos():
    resposta = requests.get("https://fakestoreapi.com/products")
    dados = resposta.json()
    return tratar_resposta(resposta)
        
@app.get("/produtos/<int:id>")
def buscar_produtos(id):
    resposta = requests.get(f"https://fakestoreapi.com/products/{id}")
    dados = resposta.json()
    return tratar_resposta(resposta)
     
@app.post("/produtos/cadastrar")
def cadastrar_produto():
    novo_produto = request.json
    resposta = requests.post("https://fakestoreapi.com/products", json=novo_produto)
    dados = resposta.json()
    return tratar_resposta(resposta)
     
@app.put("/produtos/<int:id>/atualizar")
def atualizar_produto(id):
    informacao = request.json
    resposta = requests.put(f"https://fakestoreapi.com/products/{id}", json=informacao)
    dados = resposta.json()
    return tratar_resposta(resposta)
     
@app.patch("/produtos/<int:id>/mudar")
def mudar_produto(id):
    produto = obter_produto(id)
    if produto is None:
        return {"erro": "Produto não encontrado."}, 404
    produto.update(request.json)
    resposta = requests.patch(f"https://fakestoreapi.com/products/{id}",json=produto)
    return tratar_resposta(resposta)
     
@app.delete("/produtos/<int:id>/deletar")
def apagar_produto(id):
    resposta = requests.delete(f"https://fakestoreapi.com/products/{id}")
    dados = resposta.json()
    return tratar_resposta(resposta)
        
app.run(debug=True)