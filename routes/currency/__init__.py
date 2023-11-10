from flask import Blueprint

product_bp = Blueprint('routes', __name__)

from routes.products import routes
