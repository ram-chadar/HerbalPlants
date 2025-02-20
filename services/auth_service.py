from functools import wraps
import secrets
from flask_mail import Message
from flask import current_app, flash, redirect, session, url_for
from models.user import db, User
from services.notification_service import NotificationService

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:  # Check if user is logged in
            flash("You must be logged in to access this page", "danger")
            return redirect(url_for("page.login"))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

def authenticate_user(email, password):
    """Authenticate user with plain text password (not recommended for production)."""
    user = User.query.filter_by(email=email).first()

    if not user:
        return "Invalid Email", None
    if user.password != password:  # Direct comparison (plain text)
        return "Invalid Password", None
    if not user.email_verified:
        return "Please verify your email", None
    if user.status == 'Inactive':
        return "User is inactive", None
    if user.status == 'Blocked':
        return "User is Blocked", None
    
    # Store user details in session after successful login
    session["user_id"] = user.user_id
    session["full_name"] = user.full_name
    session["email"] = user.email
    return None, user  # No error, return user object


def register_user(data):
    """Handle user registration and send notifications asynchronously."""
    if not data.get('full_name') or not data.get('email') or not data.get('password') or not data.get('mobile'):
        raise ValueError("Missing required fields")

    existing_user = User.query.filter((User.email == data['email']) | (User.mobile == data['mobile'])).first()
    if existing_user:
        raise ValueError("Email or mobile already registered")

    token = secrets.token_hex(16)

    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        mobile=data['mobile'],
        password=data['password'],
        token=token
    )

    db.session.add(new_user)
    db.session.commit()

    # Send email verification asynchronously
    verification_url = f"{current_app.config['BASE_URL']}/auth/verify_email/{token}/{new_user.email}"
    NotificationService.send_email(
        subject="Verify Your Email",
        recipients=[new_user.email],
        body=f"Please click the link to verify your email: {verification_url}"
    )

    # Send welcome email asynchronously
    NotificationService.send_email(
        subject="Welcome to Our Platform!",
        recipients=[new_user.email],
        body=f"Hello {new_user.full_name},\n\nThank you for registering with us."
    )

    return new_user




def verify_email_token(token, email):
    """Verify the email token and update the email_verified status if valid."""
    # Check if the token and email exist in the database
    user = User.query.filter_by(token=token, email=email).first()
    
    if not user:
        raise ValueError("Invalid token or email")

    # Update the user's email_verified status to True
    user.email_verified = True
    user.token = None
    db.session.commit()

    return user.email





