# cheapest-tomato.tech

This is my Project portfolio and all related documents.

steps:
## 1-Define Data Structure:
Products: Name, attributes (color, size, etc.)
Shops: Name, location, branches
Prices: Product price in each shop


Products Table:

product_id (Primary Key), 
name, 
attributes (e.g., color, size)

Shops Table:

shop_id (Primary Key), 
name, 
location, 
branches

Prices Table:

price_id (Primary Key), 
product_id (Foreign Key referencing Products Table), 
shop_id (Foreign Key referencing Shops Table), 
price, 
last_updated (Timestamp for price update)

```
-- Create user
CREATE USER 'bassant'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'bassant'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Create Database
CREATE DATABASE cheapest-tomato;
USE cheapest-tomato;
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    attributes TEXT
);
CREATE TABLE shops (
    shop_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    branches TEXT
);
CREATE TABLE prices (
    price_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    shop_id INT,
    price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
);

-- Retrive prices information
SELECT p.price_id, pr.name AS product_name, s.name AS shop_name, p.price
FROM prices p
JOIN products pr ON p.product_id = pr.product_id
JOIN shops s ON p.shop_id = s.shop_id;

-- Insert random products with valid names and attributes
INSERT INTO products (name, attributes)
VALUES
('Tomato', 'Red, Fresh'),
('Potato', 'Brown, Large'),
('Apple', 'Green, Sweet'),
('Banana', 'Yellow, Ripe'),
('Milk', 'Fresh, Dairy'),
('Bread', 'Whole Wheat, Sliced'),
('Chicken', 'Fresh, Boneless'),
('Eggs', 'Large, Brown'),
('Cheese', 'Cheddar, Sliced'),
('Coffee', 'Roasted, Ground');

-- Insert random shops with valid names and locations
INSERT INTO shops (name, location, branches)
VALUES
('Fresh Mart', 'City Center', 'Main Branch'),
('Green Grocer', 'Downtown', 'Branch A'),
('Mega Market', 'Suburb', 'Branch B'),
('Organic Foods', 'Town Square', 'Branch C'),
('Marketplace', 'Shopping Mall', 'Branch D'),
('Family Grocers', 'Residential Area', 'Branch E'),
('Gourmet Delights', 'Business District', 'Branch F'),
('Farmers Market', 'Rural Area', 'Branch G'),
('Health Food Store', 'Fitness Center', 'Branch H'),
('Super Savers', 'Commercial Zone', 'Branch I');

-- Insert random prices for other products in remaining shops
INSERT INTO prices (product_id, shop_id, price, last_updated)
SELECT
    pr.product_id,
    s.shop_id,
    ROUND(RAND() * (10 - 1) + 1, 2) AS price,
    NOW() - INTERVAL FLOOR(RAND()*30) DAY AS last_updated
FROM
    (SELECT DISTINCT product_id FROM products WHERE product_id < 10) AS pr
CROSS JOIN
    (SELECT DISTINCT shop_id FROM shops WHERE shop_id < 10) AS s;

-- show tomato prices ascendingly
SELECT pr.name AS product_name, s.name AS shop_name, p.price, p.last_updated
FROM prices p
JOIN products pr ON p.product_id = pr.product_id
JOIN shops s ON p.shop_id = s.shop_id
WHERE pr.name = 'Tomato' -- Search by product name
ORDER BY p.price ASC; -- Order prices from lowest to highest

OR

DELIMITER //

CREATE PROCEDURE search_product_prices(IN product_name_param VARCHAR(255))
BEGIN
    SELECT pr.name AS product_name, s.name AS shop_name, p.price, p.last_updated
    FROM prices p
    JOIN products pr ON p.product_id = pr.product_id
    JOIN shops s ON p.shop_id = s.shop_id
    WHERE LOWER(pr.name) = LOWER(product_name_param) -- Case insensitive search
    ORDER BY p.price ASC; -- Order prices from lowest to highest
END//

DELIMITER ;

CALL search_product_prices('Tomato'); -- Example usage for searching tomatoes
```


## 2-Choose Technologies:
### Backend: Python (Flask), MySQL for database storage
#### Set Up Flask App:
Make sure you have Flask installed in your Python environment. If not, you can install it using pip:
```
pip install flask
```
Then, create a Flask application and set up your project structure. 
```
#app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy data (replace with database interactions)
products = [
    {"id": 1, "name": "Tomatoes"},
    {"id": 2, "name": "Potatoes"},
    # Add more products
]

@app.route('/')
def index():
    return "Welcome to Cheapest Tomato API!"

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q')  # Get 'q' parameter from query string
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    # Perform search logic (e.g., search in database)
    results = [p for p in products if query.lower() in p['name'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)  # Run the app in debug mode
```
#### Run Your Flask App:
```
python app.py
```
#### Test API Endpoints:
```
curl http://localhost:8080/ #to see your welcome message.
curl http://localhost:8080/products #to see the list of products
curl http://localhost:8080/search?q=tomato #to search for products containing "tomato" in their names.
```

or simply write in your browser:

cheapest-tomato.tech:8080

cheapest-tomato.tech:8080/products

cheapest-tomato.tech:8080/search?q=tomato
### Nginx and Landing page
adde landing page to Flask, Configured Nginx to launch the flask app continously
```
#/etc/nginx/sites-available/flask_app
server {
    listen 80;
    server_name cheapest-tomato.tech;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Database Integration:
Replace the dummy data and search logic with actual database queries to fetch product information and prices from your MySQL database.

Frontend: HTML, CSS for a simple user interface
## 3-Implementing the Backend:
Use Flask to create routes for handling user requests.
Design database schema to store product, shop, and price information.
Create functions to fetch cheapest prices and suggest stores.
## 4-User Interaction:
Prompt the user for the item they want to buy and their location.
Query the database to find the cheapest prices for the item in nearby stores.
Display results to the user and suggest the cheapest store.
## 5-Cart Functionality:
Allow users to add items to their cart.
Calculate total prices from different stores based on cart items.
Suggest the most cost-effective combination of stores for their shopping list.
## 6-Update Data:
Regularly update prices and store information to ensure accuracy.
Consider integrating APIs or web scraping for real-time data updates.
## 7-User Interface:
Create a simple and intuitive interface using HTML and CSS.
Display search results, store details, and cart information clearly.
## 8-Testing and Deployment:
Test the application thoroughly to ensure accurate price comparisons.
Deploy the application on a server for public access.
