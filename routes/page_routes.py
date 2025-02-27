# routes/page_routes.py
from flask import Blueprint, render_template

from services.admin_service import get_all_categories
from services.common_service import get_approved_plants, track_visitor

# Define the Blueprint 'page'
page = Blueprint('page', __name__)

# Define routes for 'page'
@page.route('/')
def home():
  track_visitor()
  approved_plants=  get_approved_plants()
  return render_template('index.html',approved_plants=approved_plants)

@page.route('/register')
def register():
    return render_template('register.html')

@page.route('/login')
def login():
    return render_template('login.html')

@page.route('/user_home')
def user_home():
    return render_template('user_home.html')

@page.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')

@page.route('/submit_plant')
def submit_plant():
    categories=get_all_categories()
    return render_template('submit_plant.html',categories=categories)



