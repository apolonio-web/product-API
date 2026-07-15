import requests
import json
from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def root():
    return "Seja bem vindo a minha api"

@app.get("/produtos")
def listar_produtos():
    resposta = requests.get("https://fakestoreapi.com/products")
    dados = resposta.json()
    if resposta.status_code == 200:
        return dados
    else:
     return {
    "erro": "Falha ao consultar a Fake Store.",
    "status": resposta.status_code
            }, resposta.status_code
     
     
@app.get("/produtos/<int:id>")
def buscar_produtos(id):
    resposta = requests.get(f"https://fakestoreapi.com/products/{id}")
    dados = resposta.json()
    if resposta.status_code == 200:
        return dados
    else:
     return {
    "erro": "Falha ao consultar a Fake Store.",
    "status": resposta.status_code
            }, resposta.status_code
     
     
@app.post("/produtos/cadastrar")
def cadastrar_produto():
    novo_produto = {"title": "nome" , "price" : "int:preco" ,"description": "string",
"category": "string"}
    resposta = requests.post("https://fakestoreapi.com/products", json=novo_produto)
    dados = resposta.json()
    if resposta.status_code == 200:
        return dados
    else:
     return {
    "erro": "Falha ao consultar a Fake Store.",
    "status": resposta.status_code
            }, resposta.status_code
     
     
@app.put("/produtos/<id>/atualizar")
def atualizar_produto(id):
    informacao = request.json
    resposta = requests.put(f"https://fakestoreapi.com/products/{id}", json=informacao)
    dados = resposta.json()
    if resposta.status_code == 200:
        return dados
    else:
     return {
    "erro": "Falha ao consultar a Fake Store.",
    "status": resposta.status_code
            }, resposta.status_code
     
@app.patch("/produtos/<id>/mudar")
def mudar_produto(id):
    produto = buscar_produtos(id)
    produto.update(request.json)
    resposta = requests.patch(f"https://fakestoreapi.com/products/{id}", json=produto)
    dados = resposta.json()
    if resposta.status_code == 200:
        return dados
    else:
     return {
    "erro": "Falha ao consultar a Fake Store.",
    "status": resposta.status_code
            }, resposta.status_code
     
@app.delete("/produtos/<id>/deletar")
def apagar_produto(id):
    resposta = requests.delete(f"https://fakestoreapi.com/products/{id}")
    dados = resposta.json()
    if resposta.status_code == 200:
        return dados
    else:
        return {
              "erro": "Falha ao consultar a Fake Store.",
              "status": resposta.status_code
            }, resposta.status_code
        
        
app.run(debug=True)