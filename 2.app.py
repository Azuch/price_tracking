# backend/app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import asyncio
from aiohttp import ClientSession

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

Base = declarative_base()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/api/products', methods=['POST'])
async def fetch_product():
    product_name = request.json['name']
    async with ClientSession() as session:
        async with session.post('http://example.com', json={'name': product_name}) as response:
            response_data = await response.json()
            product_price = response_data['price']
            product = Product(name=product_name, price=product_price)
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Product added successfully'}), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = [{'name': product.name, 'price': product.price, 'timestamp': product.timestamp} for product in products]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

