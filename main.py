import json
from flask import Flask, request

def carregar_produtos():
    with open("produtos.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
def salvar_produtos(produtos):
    with open("produtos.json", "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)    


app = Flask(__name__)

@app.get("/")
def inicio():
    return "Seja Bem vindo ao Sistema de Gereciamento de Evento"


@app.get("/produtos")
def listar_produtos():
     return carregar_produtos()


@app.get("/produtos/<nome>")
def buscar_produto(nome):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto["nome"].lower() == nome.lower():
            return produto

    return {"erro": "Produto não encontrado"}, 404


@app.post("/produtos/cadastro")
def cadastrar_produto():
   produtos = carregar_produtos()
   novo_produto = request.json
   produtos.append(novo_produto)
   salvar_produtos(produtos)
   return {
        "mensagem": "Produto cadastrado com sucesso!",
        "produto": novo_produto
    }, 201
   
   
@app.delete("/produtos/<nome>/deletar")
def apagar_produto(nome):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto["nome"].lower() == nome.lower():
            produtos.remove(produto)
            salvar_produtos(produtos)

            return {
                "mensagem": "Produto deletado com sucesso!",
                "produto": produto
            }, 201
    return {"erro" : "Produto não encontrado"}, 404 
@app.patch("/produtos/<nome>/atualizar")
def atualizar_produtos(nome):
    produtos = carregar_produtos()
    for produto in produtos:
     if produto["nome"].lower() == nome.lower():
         
        produto.update(request.json)
        salvar_produtos(produtos)
        
        return{
            "mensagem": "Produto atualizado com sucesso!",
            "produto" : produto          
        }
    return {
"erro" : "Produto não encontrado"
         }, 404


app.run(debug=True)