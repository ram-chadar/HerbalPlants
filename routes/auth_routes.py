from flask import Blueprint, render_template, request
from services.auth_service import authenticate_user, register_user, verify_email_token


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login_user', methods=['POST'])
def login():
    """Handles user login"""
    data = request.form
    message, user = authenticate_user(data['email'], data['password'])

    if message:
        return render_template("login.html", message=message), 400
    
    # Redirect user based on role
    return render_template("admin_home.html") if user.role == 'Admin' else render_template("user_home.html"), 200

@auth_bp.route('/logout', methods=['GET'])
def logout():
    return render_template("index.html"), 200

@auth_bp.route('/register_user', methods=['POST'])
def registeruser():
    data = request.form
    try:
        user = register_user(data)
        if not user:
            return render_template("register.html", message="User already exists"), 400
        else:
            return render_template("register.html", message="Please check your email for verification."), 200
    except ValueError as e:
        return render_template("register.html", message=str(e)), 400

@auth_bp.route('/verify_email/<token>/<email>', methods=['GET'])
def verify_email(token, email):
    try:
        # Call the service function to verify the token and email, and update the user's status
        user_email = verify_email_token(token, email)
        
        return render_template("index.html", message=f"Email successfully verified!"), 200
    except ValueError as e:
        return render_template("index.html", message=str(e)), 400
