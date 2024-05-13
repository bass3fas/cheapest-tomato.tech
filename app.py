from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bassant:@localhost/cheapest-tomato'  # Update with your credentials and database name
db = SQLAlchemy(app)

# Define SQLAlchemy models
class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    attributes = db.Column(db.Text)

class Shop(db.Model):
    __tablename__ = 'shops'  # Match the table name in your database

    shop_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    branches = db.Column(db.Text)

class Price(db.Model):
    __tablename__ = 'prices'  # Match the table name in your database

    price_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'))
    price = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def landing():
    return render_template('landing.html')

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'id': product.product_id, 'name': product.name} for product in products]
    return jsonify(product_list)

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    # Perform search logic using SQLAlchemy query
    results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    product_list = [{'id': product.id, 'name': product.name} for product in results]
    return jsonify(product_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
