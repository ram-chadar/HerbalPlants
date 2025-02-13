# routes/page_routes.py
from flask import Blueprint, render_template

# Define the Blueprint 'page'
page = Blueprint('page', __name__)

# Define routes for 'page'
@page.route('/')
def home():
    return render_template('index.html')

@page.route('/register')
def register():
    return render_template('register.html')

@page.route('/login')
def login():
    return render_template('login.html')
