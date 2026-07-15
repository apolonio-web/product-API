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
    
def tratar_excepts(erro):
    if isinstance(erro, requests.exceptions.ConnectionError):
     return {
    "erro": "Não foi possível conectar à Fake Store."
}, 503
    elif isinstance(erro, requests.exceptions.Timeout):
     return {
    "erro": "A Fake Store demorou muito para responder."
}, 504
    elif isinstance(erro,requests.exceptions.RequestException):
     return {
        "erro": "Erro ao comunicar com a Fake Store."
}, 500  
    else:
     return {
    "erro": "Erro inesperado."
}, 500
    
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
    try:
       resposta = requests.get("https://fakestoreapi.com/products", timeout=5)
       return tratar_resposta(resposta)
    except Exception as erro:
        return tratar_excepts(erro)
        
        
@app.get("/produtos/<int:id>")
def buscar_produtos(id):
    try:
       resposta = requests.get(f"https://fakestoreapi.com/products/{id}", timeout=5)
       return tratar_resposta(resposta)
    except Exception as erro:
        return tratar_excepts(erro)
    
@app.post("/produtos/cadastrar")
def cadastrar_produto():
    try: 
       novo_produto = request.json
       resposta = requests.post("https://fakestoreapi.com/products", json=novo_produto, timeout=5)
       return tratar_resposta(resposta)
    except Exception as erro:
        return tratar_excepts(erro)
     
@app.put("/produtos/<int:id>/atualizar")
def atualizar_produto(id):
    try:
       informacao = request.json
       resposta = requests.put(f"https://fakestoreapi.com/products/{id}", json=informacao, timeout=5)
       return tratar_resposta(resposta)
    except Exception as erro:
        return tratar_excepts(erro)
     
@app.patch("/produtos/<int:id>/mudar")
def mudar_produto(id):
    try:
       produto = obter_produto(id)
       if produto is None:
           return {"erro": "Produto não encontrado."}, 404
       produto.update(request.json)
       resposta = requests.patch(f"https://fakestoreapi.com/products/{id}",json=produto, timeout=5)
       return tratar_resposta(resposta)
    except Exception as erro:
        return tratar_excepts(erro)
     
@app.delete("/produtos/<int:id>/deletar")
def apagar_produto(id):
    try:
       resposta = requests.delete(f"https://fakestoreapi.com/products/{id}", timeout=5)
       return tratar_resposta(resposta)
    except Exception as erro:
        return tratar_excepts(erro)
        
app.run(debug=True)