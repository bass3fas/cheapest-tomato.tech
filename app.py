from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bassant:@localhost/cheapest-tomato'
db = SQLAlchemy(app)

# Define SQLAlchemy models
class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    attributes = db.Column(db.Text)

class Shop(db.Model):
    __tablename__ = 'shops'
    shop_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    branches = db.Column(db.Text)

class Price(db.Model):
    __tablename__ = 'prices'
    price_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'))
    price = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/shops', methods=['GET'])
def get_shops():
    shops = Shop.query.all()
    return render_template('shops.html', shops=shops)

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_shops(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    prices = Price.query.filter_by(product_id=product_id).all()
    shop_list = [{'shop_name': Shop.query.get(price.shop_id).name, 'price': price.price} for price in prices]
    return render_template('product_shops.html', product=product, shops=shop_list)

@app.route('/shop/<int:shop_id>', methods=['GET'])
def get_shop_products(shop_id):
    shop = Shop.query.get(shop_id)
    if not shop:
        return jsonify({'error': 'Shop not found'}), 404

    prices = Price.query.filter_by(shop_id=shop_id).all()
    product_list = [{'product_name': Product.query.get(price.product_id).name, 'price': price.price} for price in prices]
    return render_template('shop_products.html', shop=shop, products=product_list)

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q')
    if not query:
        return render_template('search.html')

    sql_query = text(f"""
        SELECT pr.name AS product_name, pr.attributes AS product_attributes, s.name AS shop_name,
        p.price, p.last_updated
        FROM prices p
        JOIN products pr ON p.product_id = pr.product_id
        JOIN shops s ON p.shop_id = s.shop_id
        WHERE LOWER(pr.name) LIKE LOWER(:query)
        ORDER BY p.price ASC
    """)

    results = db.session.execute(sql_query, {'query': f'%{query}%'})
    product_list = [{'product_name': row.product_name, 'product_attributes': row.product_attributes,
                     'shop_name': row.shop_name, 'price': row.price, 'last_updated': row.last_updated}
                    for row in results]

    db.session.close()
    return render_template('search_results.html', products=product_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)

