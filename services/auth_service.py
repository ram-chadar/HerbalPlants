import secrets
from flask_mail import Message
from flask import current_app
from models.user import db, User


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
    
    return None, user  # No error, return user object


def register_user(data):
    """Handle user registration."""
    # Check if all required fields are provided
    if not data.get('full_name') or not data.get('email') or not data.get('password') or not data.get('mobile'):
        raise ValueError("Missing required fields")

    # Check if the email or mobile is already registered
    existing_user = User.query.filter((User.email == data['email']) | (User.mobile == data['mobile'])).first()
    if existing_user:
        raise ValueError("Email or mobile already registered")

    # Generate a random verification token
    token = generate_verification_token()

    # Create new user instance
    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        mobile=data['mobile'],
        password=data['password'],
        token=token  # Store the token in the database
    )

    # Save the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Send the token via email
    send_verification_email(new_user.email, token)

    return new_user

def generate_verification_token():
    """Generate a random verification token."""
    # Generate a secure random token
    return secrets.token_hex(16)  # Generates a random 32-character hexadecimal string

def send_verification_email(email, token):
    """Send an email with the verification link."""
    verification_url = f"{current_app.config['BASE_URL']}/auth/verify_email/{token}/{email}"
    msg = Message("Verify your email address", recipients=[email])
    msg.body = f"Please click the link to verify your email: {verification_url}"
    try:
        current_app.extensions['mail'].send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

from models.user import db, User

def verify_email_token(token, email):
    """Verify the email token and update the email_verified status if valid."""
    # Check if the token and email exist in the database
    user = User.query.filter_by(token=token, email=email).first()
    
    if not user:
        raise ValueError("Invalid token or email")

    # Update the user's email_verified status to True
    user.email_verified = True
    user.token = None  # Optional: Clear the token after successful verification
    db.session.commit()

    return user.email  # Return the email after successful verification


