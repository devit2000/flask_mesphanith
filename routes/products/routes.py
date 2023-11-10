import sqlite3

import uuid
from flask import render_template, request, redirect
from dotenv import load_dotenv
import os
from routes.products import product_bp

load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = product_bp


@app.route("/admin/product")
def product():
    succeeded = ''
    type_name = 0
    success = request.args.get("success")
    type = request.args.get("type")
    if success == TRUE:
        succeeded = True
    if success == FALSE:
        succeeded = False
    if type == CREATE:
        type_name = 1
    elif type == UPDATE:
        type_name = 2
    elif type == DELETE:
        type_name = 3
    else:
        type_name = 0

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * from product;")
    products = cur.fetchall()
    current_url = "/admin/product"
    return render_template("admin/product/index.html", url=current_url, products=products, success=succeeded,
                           type=type_name)


@app.route("/admin/product/add")
def add_product_view():
    current_url = "/admin/product"
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
    img=request.form.get("img")
    if (name == "" or cost == "" or price == "" or qty == ""):
        return render_template("admin/product/add.html", url=current_url, success=False)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product (id,name, quantity,cost,price,image,status) VALUES (?,?,?,?,?,?,?)",
                   (id, name, qty, cost, price, img, status))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/product?success={TRUE}&type={CREATE}")
    else:
        return redirect(f"/admin/product?success={FALSE}&type={CREATE}")


@app.route("/admin/product", methods=["POST"])
def delete_product():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM product WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        return redirect(f"/admin/product?success={TRUE}&type={DELETE}")
    else:
        return redirect(f"/admin/product?success={FALSE}&type={DELETE}")


@app.route("/admin/product/edit/<id>")
def edit_product_view(id):
    url = "/admin/product"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from product WHERE id = ?", (id,))
    product = cursor.fetchone()
    return render_template("admin/product/edit.html", product=product, id=id, url=url)


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
    img = request.form.get("img")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (name, cost, price, qty,
                           status, img, request.form.get('id')))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/product?success={TRUE}&type={UPDATE}")
    else:
        return redirect(f"/admin/product?success={FALSE}&type={UPDATE}")
