import os
from models import db
from models.plant import Plant
from models.user import User

def get_approved_plants():
    try:
        # Fetch only plants with status 'Approved'
        approved_plants = Plant.query.filter_by(submission_status='Approved').all()

        # If no approved plants found
        if not approved_plants:
            return "No approved plants found."

        return approved_plants
    except Exception as e:

        return f"Error: {str(e)}"

def get_profile(user_id):
    """Retrieve the logged-in user's profile details."""
    user = User.query.filter_by(user_id=user_id).first()
    
    if not user:
        raise ValueError("User not found")

    return user

def update_user_profile(data):
    user_id = data.get('user_id')
    user = get_profile(user_id)

    if not user:
        return "User not found", "danger"

    # Update only if data exists
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.mobile = data.get('mobile', user.mobile)
    user.password = data.get('password', user.password)  # Hash this in real apps

    db.session.commit()
    return "User profile updated successfully!", "success"
    
