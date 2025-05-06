from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unirent.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    price_per_day = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price_per_day = float(request.form['price_per_day'])
        product = Product(name=name, description=description, price_per_day=price_per_day, owner_id=session['user_id'])
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/rent/<int:product_id>', methods=['GET', 'POST'])
def rent(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        days = int(request.form['days'])
        total = product.price_per_day * days
        return render_template('rent.html', product=product, total=total, days=days)
    return render_template('rent.html', product=product)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
