from flask import (render_template, request, redirect,
                   url_for, flash, abort, jsonify, session)
import math
import time
from app import app

from app.config import CLOUD_NAME, CO_API_KEY, CO_API_SECRET, DATABASE_URL

from app.models.model import Product
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, and_, or_
import cloudinary.uploader
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey,
    Numeric, Boolean, Enum, Text, DECIMAL
)
import cloudinary

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))


cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=CO_API_KEY,
    api_secret=CO_API_SECRET
)


def findProductById(id):
    db = SessionLocal()
    products = db.query(Product).all()
    for product in products:
        if product.getId() == id:
            return product
    return False


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/paged")
def paged():
    db = SessionLocal()
    products = db.query(Product).all()
    time.sleep(2)
    page = request.args.get("page", 1, type=int)
    per_page = 10
    start = (page-1) * per_page
    end = start + per_page

    total_page = math.ceil(len(products)/per_page)
    products_da_pagina = products[start:end]
    return render_template("paged.html", products=products_da_pagina, page=page, total_page=total_page)


@app.route("/seedetail/<int:id>")
def detailed(id):
    product = findProductById(id)
    if (product):
        return render_template("detailed.html", product=product)
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    db = SessionLocal()
    products = db.query(Product).all()
    page = request.args.get("page", 1, type=int)
    per_page = 5
    start = (page-1) * per_page
    end = start + per_page

    total_page = math.ceil(len(products)/per_page)
    products_da_pagina = products[start:end]
    return render_template("admin.html", products=products_da_pagina, page=page, total_page=total_page)


def getImgUrl(file):
    try:
        upload_result = cloudinary.uploader.upload(file)
        img_url = upload_result["secure_url"]
        return img_url
    except:
        return None


@app.route("/api/newproduct", methods=["POST", "GET"])
def newProduct():
    db = SessionLocal()
    products = db.query(Product).all()
    data = request.form
    file = request.files.get("img")
    print(f"* Data: {data}, File: {file}")
    if file:

        if data and "name" in data:
            print("hi")
            img_url = getImgUrl(file)
            if (img_url):

                novo_produto = Product(name=data.get("name"),
                                       price=data.get("price"),
                                       img_url=img_url
                                       )

                db.add(novo_produto)
                db.commit()
                return url_for("admin")
    return url_for("index")


@app.route("/api/exclude/<int:id>")
def exclude(id):
    db = SessionLocal()
    products = db.query(Product).all()
    for product in products:
        if (product["id"] == id):
            products.remove(product)
            return jsonify({"Status": "OK, removido"})
        return jsonify({"Status": "Alguma coisa falhou"})
