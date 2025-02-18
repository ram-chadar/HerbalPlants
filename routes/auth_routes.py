from flask import Blueprint, redirect, render_template, request, session, url_for
from services.auth_service import authenticate_user, register_user, verify_email_token
from services.common_service import get_approved_plants


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login_user', methods=['POST','GET'])
def login():
    """Handles user login"""
    data = request.form
    message, user = authenticate_user(data['email'], data['password'])

    if message:
        return render_template("login.html", message=message), 400

    # 🔹 Use `redirect()` to ensure session persists across requests
    return redirect(url_for("page.admin_home")) if user.role == 'Admin' else redirect(url_for("page.user_home"))


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    approved_plants=  get_approved_plants()
    return render_template('index.html',approved_plants=approved_plants)

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
    

