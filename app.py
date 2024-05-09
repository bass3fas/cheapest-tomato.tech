from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Dummy product data (replace with actual data from your database)
products = [
    {"id": 1, "name": "Tomatoes"},
    {"id": 2, "name": "Potatoes"},
    {"id": 3, "name": "Onions"},
    # Add more products
]

@app.route('/')
def index():
    return "Welcome to Cheapest Tomato API!"

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    # Perform search logic here (e.g., search in your database)
    results = [p for p in products if query.lower() in p['name'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
