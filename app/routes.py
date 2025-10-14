from flask import (render_template,request,redirect,url_for,flash,abort,jsonify,session)
import math
import time
from app import app

from app.models.products import products
from app.models.product import Product
def findProductById(id):
    for product in products:
        if product.getId() == id:
            return product
    return False

@app.route("/")
def index():


    return render_template("index.html")


@app.route("/paged")
def paged():
    time.sleep(2)
    page = request.args.get("page",1,type = int)
    per_page = 10
    start = (page-1) * per_page
    end = start + per_page

    total_page = math.ceil(len(products)/per_page)
    products_da_pagina = products[start:end]
    return render_template("paged.html",products=products_da_pagina,page=page,total_page = total_page)

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

    total_page = math.ceil(len(products)/per_page)
    products_da_pagina = products[start:end]
    return render_template("admin.html",products=products_da_pagina,page=page,total_page = total_page)

@app.route("/api/newproduct", methods=["POST","GET"])
def newProduct():
    data = request.get_json()
    print(data)
    if data and "nome" in data:
        products.append({
            Product( len(products)+1,
            data["nome"],
            data["preco"]
            )
        })
        return jsonify({
            "Status": "OK"
        })
    return jsonify({"Status": "Alguma coisa falhou"})


@app.route("/api/exclude/<int:id>")
def exclude(id):
    for product in products:
        if ( product["id"] == id ):
            products.remove(product)
            return jsonify({"Status": "OK, removido"})
        return jsonify({"Status": "Alguma coisa falhou"})
    