import sqlite3

import uuid
from flask import render_template, request, redirect
from dotenv import load_dotenv
import os
from routes.category import category_bp

load_dotenv()

TRUE = os.environ.get('true_code')
FALSE = os.environ.get('false_code')
CREATE = os.environ.get('create_code')
UPDATE = os.environ.get('update_code')
DELETE = os.environ.get('delete_code')

app = category_bp


@app.route("/admin/category")
def category():
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
    cur.execute("SELECT * from category;")
    categorys = cur.fetchall()
    current_url = "/admin/category"
    return render_template("admin/category/index.html", url=current_url, categorys=categorys, success=succeeded,
                           type=type_name)


@app.route("/admin/category/add")
def add_category_view():
    current_url = "/admin/category"
    return render_template("admin/category/add.html", url=current_url)


@app.route("/admin/category/add", methods=["POST"])
def add_category():
    id = str(uuid.uuid4())
    name = request.form.get("name")
    status = 0
    if request.form.get("status"):
        status = 1
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO category (id,name,status) VALUES (?,?,?)",
                   (id, name, status))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/category?success={TRUE}&type={CREATE}")
    else:
        return redirect(f"/admin/category?success={FALSE}&type={CREATE}")


@app.route("/admin/category", methods=["POST"])
def delete_category():
    id = request.form.get("id")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM category WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(cursor.rowcount)
    if cursor.rowcount > 0:
        return redirect(f"/admin/category?success={TRUE}&type={DELETE}")
    else:
        return redirect(f"/admin/category?success={FALSE}&type={DELETE}")


@app.route("/admin/category/edit/<id>")
def edit_category_view(id):
    current_url = "/admin/category"
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("select * from category WHERE id = ?", (id,))
    category = cursor.fetchone()
    return render_template("admin/category/edit.html", category=category, id=id, url=current_url)


@app.route('/admin/category/edit', methods=["POST"])
def edit_category():
    query = '''
    UPDATE category 
    SET name = ?, status = ? WHERE id = ?
    '''
    name = request.form.get("name")
    status = 0
    if (request.form.get("status")):
        status = 1
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query, (name,status, request.form.get('id')))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        return redirect(f"/admin/category?success={TRUE}&type={UPDATE}")
    else:
        return redirect(f"/admin/category?success={FALSE}&type={UPDATE}")
