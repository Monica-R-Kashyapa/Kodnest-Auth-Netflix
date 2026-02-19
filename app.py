from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_here')

# Database configuration - fallback to SQLite if Aiven credentials not set
AIVEN_DB_HOST = os.getenv('AIVEN_DB_HOST')
if AIVEN_DB_HOST:
    # Use Aiven MySQL
    AIVEN_DB_PORT = os.getenv('AIVEN_DB_PORT', '25060')
    AIVEN_DB_NAME = os.getenv('AIVEN_DB_NAME', 'defaultdb')
    AIVEN_DB_USER = os.getenv('AIVEN_DB_USER', 'avnadmin')
    AIVEN_DB_PASSWORD = os.getenv('AIVEN_DB_PASSWORD')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{AIVEN_DB_USER}:{AIVEN_DB_PASSWORD}@{AIVEN_DB_HOST}:{AIVEN_DB_PORT}/{AIVEN_DB_NAME}'
    print("Using Aiven MySQL database")
else:
    # Fallback to SQLite for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    print("Using SQLite database (development mode)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'User'
    
    UserId = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    def __init__(self, UserId, name, password, email, phone):
        self.UserId = UserId
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        
        # Check if user already exists
        existing_user = User.query.filter_by(UserId=user_id).first()
        if existing_user:
            flash('User ID already exists!', 'error')
            return render_template('register.html')
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists!', 'error')
            return render_template('register.html')
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Create new user
        new_user = User(UserId=user_id, name=name, password=hashed_password, email=email, phone=phone)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        # Find user by name instead of UserId
        user = User.query.filter_by(name=name).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.UserId
            session['name'] = user.name
            flash('Login successful!', 'success')
            # Redirect to Kodest Netflix landing page
            return redirect('https://kodnest-netflix.vercel.app/')
        else:
            flash('Invalid name or password!', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
