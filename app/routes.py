from flask import (render_template, request, redirect,
                   url_for, flash, abort, jsonify, session)
import math
import time
from app import app

from app.config import CLOUD_NAME, CO_API_KEY, CO_API_SECRET, DATABASE_URL
import os
from app.models.model import Product
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, and_, or_
import cloudinary.uploader
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, ForeignKey,
    Numeric, Boolean, Enum, Text, DECIMAL
)
import cloudinary
from werkzeug.utils import secure_filename

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))

products_img_folder = "app/static/assets/productsimgs"

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
    print(products)
    page = request.args.get("page", 1, type=int)
    per_page = 5
    start = (page-1) * per_page
    end = start + per_page

    total_page = math.ceil(len(products)/per_page)
    print("Total Page: ",total_page)
    if total_page == 0:
        total_page = 1
    products_da_pagina = products[start:end]
    print("Da pagina: ",products_da_pagina)
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
    
    secure_img_filename = secure_filename(file.filename)

    complete_file_name = os.path.join(products_img_folder,secure_img_filename)
    os.makedirs(products_img_folder,exist_ok=True)
    file.save(complete_file_name)
    img_url = complete_file_name
    novo_produto = Product(name=data.get("name"),
                                    price=data.get("price"),
                                    img_url=img_url
                                    )
    db.add(novo_produto)
    db.commit()
    return redirect(url_for("admin"))
    # except :
    #     print("Algo aconteceu",E) 
    #     return url_for("admin")
            
    # if file:

    #     if data and "name" in data:
    #         print("hi")
    #         img_url = getImgUrl(file)
    #         if (img_url):

    #             novo_produto = Product(name=data.get("name"),
    #                                    price=data.get("price"),
    #                                    img_url=img_url
    #                                    )

    #             db.add(novo_produto)
    #             db.commit()
    #             return url_for("admin")
            
    return url_for("admin")


@app.route("/api/exclude/<int:id>")
def exclude(id):
    db = SessionLocal()
    products = db.query(Product).all()
    product = db.query(Product).filter_by(id=id).first()
    try:
        db.delete(product)
        print("Deleted")
        db.commit()
        flash("Removido","sucess")
        return redirect(url_for("admin"))
    except:
        return redirect(url_for("admin"))
   
            
        
