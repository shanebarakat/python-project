from flask import render_template, abort
from . import main
from ..models import Product, Category

@main.route('/')
def index():
    """Home page."""
    # For the home page, you might want to feature some products
    featured_products = Product.query.order_by(Product.id.desc()).limit(4).all()
    return render_template('main/index.html', products=featured_products)

@main.route('/products')
def list_products():
    """Page to list all products, possibly with filtering."""
    products = Product.query.all()
    return render_template('main/products.html', products=products)

@main.route('/product/<int:product_id>')
def product_details(product_id):
    """Page to show details for a single product."""
    product = Product.query.get_or_404(product_id)
    return render_template('main/product_details.html', product=product)

@main.route('/category/<int:category_id>')
def list_products_by_category(category_id):
    """Page to list products belonging to a specific category."""
    category = Category.query.get_or_404(category_id)
    products = category.products.all()
    return render_template('main/products.html', products=products, category=category) 