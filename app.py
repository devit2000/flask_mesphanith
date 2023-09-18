from flask import Flask, render_template
import names
from random import randint

app = Flask(__name__)


@app.route('/')
def home():
    products = []
    for i in range(15):
        products.append({
            "id": i,
            "name": names.get_full_name(),
            "old_price": randint(5,10),
            "discount": randint(5,25),
            "description": names.get_full_name()
        })

    return render_template("index.html", products=products)


if __name__ == '__main__':
    app.run()
