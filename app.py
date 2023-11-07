from random import randint
import uuid

import names
from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    category = ["All", "Drink", "Food", "Beer", "Energy Drink"]
    active = request.args.get('category')
    products = []
    for i in range(15):
        products.append({
            "id": i,
            "name": names.get_full_name(),
            "old_price": randint(5, 10),
            "discount": randint(5, 25),
            "description": names.get_full_name(),
            "category": category[randint(1, 4)]
        })
    product_filter = []
    print(active)
    if active == "All" or active is None:
        product_filter = products
        active = "All"
    else:
        for p in products:
            if active == p['category']:
                product_filter.append(p)

    return render_template("index.html", products=product_filter, categories=category, active=active)


@app.route("/detail/<id>")
def detail(id):
    return render_template("detail.html", id=id)


@app.route("/admin")
def admin():
    current_url = "/admin"
    return render_template("admin/index.html", url=current_url)


@app.route("/admin/product")
def product():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * from product;")
    products = cur.fetchall()
    current_url = "/admin/product"
    return render_template("admin/product/index.html", url=current_url, products=products)


@app.route("/admin/product/add")
def add_product_view():
    current_url = "/admin/product/add"
    return render_template("admin/product/add.html", url=current_url)


@app.route("/admin/product/add", methods=["POST"])
def add_product():
    current_url = "/admin/product"
    id = str(uuid.uuid4())
    name = request.form.get("name")
    cost = request.form.get("cost")
    price = request.form.get("price")
    qty = request.form.get("qty")
    status = 1
    # img = request.files["img"]
    img = "https://www.coca-cola.com/content/dam/onexp/pk/en/brands/coca-cola/coca-cola-sp-images/en_coca-cola_prod_coke_750x750.jpg"
    if (name == "" or cost == "" or price == "" or qty == ""):
        return render_template("admin/product/add.html", url=current_url, success=False)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product (id,name, quantity,cost,price,image,status) VALUES (?,?,?,?,?,?,?)",
                   (id, name, qty, cost, price, img, status))
    conn.commit()
    conn.close()
    return redirect("/admin/product")


@app.route("/admin/product", methods=["POST"])
def delete_product():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM product WHERE id='{id}'")
    conn.commit()
    conn.close()
    return redirect("/admin/product")


@app.route("/admin/product/edit/<id>")
def edit_product_view(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"select * from product WHERE id='{id}'")
    product = cursor.fetchone()
    return render_template("admin/product/edit.html", product=product, id=id)


@app.route('/admin/product/edit', methods=["POST"])
def edit_product():
    query = '''
    UPDATE product 
    SET name = ?,
        cost = ?,
        price = ?,
        quantity = ?,
        status = ?,
        image = ?
    WHERE id = ?
    '''
    name = request.form.get("name")
    cost = request.form.get("cost")
    price = request.form.get("price")
    qty = request.form.get("qty")
    status = 0
    if (request.form.get("status")):
        status = 1
    # img = request.files["img"]
    img = "https://www.coca-cola.com/content/dam/onexp/pk/en/brands/coca-cola/coca-cola-sp-images/en_coca-cola_prod_coke_750x750.jpg"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (name, cost, price, qty,
                   status, img, request.form.get('id')))
    conn.commit()
    conn.close()
    print(request.form.get('id'))
    return redirect('/admin/product')


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html")


@app.errorhandler(500)
def error_500(e):
    return render_template("500.html")


if __name__ == '__main__':
    app.run()
