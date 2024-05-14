# Cheapest Tomato

## Overview
This project encompasses a web application that aids users in finding the best prices for products across various stores. It integrates data analysis techniques, user interactions, and database management to provide a seamless shopping experience.

![image](https://github.com/bass3fas/cheapest-tomato.tech/assets/115794820/3936e6ad-080a-44ba-9aa8-17342f2a73ba)

## Steps Taken

1. **Define Data Structure**:
    - Products: Name, attributes (color, size, etc.)
    - Shops: Name, location, branches
    - Prices: Product price in each shop

2. **Choose Technologies**:
    - Backend: Python (Flask), MySQL for database storage
    - Frontend: HTML, CSS for user interface

3. **Flask Application Setup**:
    - Created routes for handling user requests
    - Designed database schema for storing product, shop, and price information
    - Integrated database queries to fetch real-time product and price data

4. **Nginx and Landing Page Configuration**:
    - Added a landing page to Flask application
    - Configured Nginx to launch the Flask app continuously

## Implementation Highlights
- **Backend Development**:
    - Utilized Flask to create API endpoints for user interactions
    - Designed functions to fetch cheapest prices and suggest stores
    - Integrated database interactions for dynamic data retrieval

- **Database Integration**:
    - Developed SQL queries to replace dummy data with real-time information
    - Managed database connections securely

- **Frontend Design**:
    - Created a simple and intuitive user interface using HTML and CSS
    - Displayed search results, store details, and cart information clearly

- **User Interaction**:
    - Implemented cart functionality for users to add items and calculate total prices
    - Utilized geolocation or user input to suggest the most cost-effective shopping options

- **Testing and Deployment**:
    - Conducted thorough testing to ensure accurate price comparisons and smooth user experience
    - Deployed the application on a server for public access

## Next Steps
- Implement real-time price updates using APIs or web scraping
- Enhance user interface with dynamic features and responsive design
- Incorporate user authentication and secure payment gateways for transactions

## How to Run
1. Install necessary dependencies (Flask, MySQL, etc.)
2. Configure database settings in the Flask app
3. Run the Flask app using `python app.py`
4. Access the application in your browser
