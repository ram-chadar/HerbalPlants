# app.py
from flask import Flask
from flask_mail import Mail
from itsdangerous import Serializer
from config import Config
from models import db , User
from routes.page_routes import page
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

# Token Serializer
s = Serializer(app.config['SECRET_KEY'])

# Initialize database
db.init_app(app)

# Register Blueprints
app.register_blueprint(page) 

# Register auth blueprint with prefix
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables (only for development)
    app.run(debug=True)
