from flask import (render_template,request,redirect,url_for,flash,abort,jsonify,session)
import math
from app import app


produtos = [
    {"id": 1 , "nome": "Tênis", "preco": 5000},
    {"id": 2 , "nome": "Notebook", "preco": 10000},
    {"id": 3 , "nome": "Monitor", "preco": 1500},
    {"id": 4 , "nome": "Tablet", "preco": 5500},
    {"id": 5 , "nome": "Teclado", "preco": 340},
    {"id": 6 , "nome": "Celular", "preco": 7500},
    {"id": 7 , "nome": "Controle", "preco": 300},
    {"id": 8 , "nome": "Bateria", "preco": 1500},
    {"id": 9 , "nome": "Geladeira", "preco": 9000},
    {"id": 10 , "nome": "Placa Mãe", "preco": 450},
    {"id": 11 , "nome": "Mouse", "preco": 110},
    {"id": 12 , "nome": "Óculos", "preco": 150},
    {"id": 13 , "nome": "Strap", "preco": 20},
    {"id": 14 , "nome": "Ventilador", "preco": 100},
    {"id": 15 , "nome": "Freezer", "preco": 7000},
    {"id": 16 , "nome": "Mousepad", "preco": 33},


]

def findProductById(id):
    for product in produtos:
        if product["id"] == id:
            return product
    return False

@app.route("/")
def index():


    return render_template("index.html")


@app.route("/paged")
def paged():
    page = request.args.get("page",1,type = int)
    per_page = 5
    start = (page-1) * per_page
    end = start + per_page

    total_page = math.ceil(len(produtos)/per_page)
    produtos_da_pagina = produtos[start:end]
    return render_template("paged.html",produtos=produtos_da_pagina,page=page,total_page = total_page)

@app.route("/seedetail/<int:id>")
def detailed(id):
    product = findProductById(id)
    if (product):
        return render_template("detailed.html",product=product)
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    page = request.args.get("page",1,type = int)
    per_page = 5
    start = (page-1) * per_page
    end = start + per_page

    total_page = math.ceil(len(produtos)/per_page)
    produtos_da_pagina = produtos[start:end]
    return render_template("admin.html",produtos=produtos_da_pagina,page=page,total_page = total_page)

@app.route("/api/newproduct", methods=["POST","GET"])
def newProduct():
    data = request.get_json()
    print(data)
    if data and "nome" in data:
        produtos.append({
            "id": len(produtos)+1,
            "nome" : data["nome"],
            "preco": data["preco"]
        })
        return jsonify({
            "Status": "OK"
        })
    return jsonify({"Status": "Alguma coisa falhou"})


@app.route("/api/exclude/<int:id>")
def exclude(id):
    for product in produtos:
        if ( product["id"] == id ):
            produtos.remove(product)
            return jsonify({"Status": "OK, removido"})
        return jsonify({"Status": "Alguma coisa falhou"})
    