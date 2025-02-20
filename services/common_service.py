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

from models.user import db, User
from services.notification_service import NotificationService

def update_user_profile(data):
    """Update user profile and send notification with updated details."""
    user_id = data.get('user_id')
    user = get_profile(user_id)

    if not user:
        return "User not found", "danger"

    # Store old values for comparison (optional)
    old_full_name, old_email, old_mobile = user.full_name, user.email, user.mobile

    # Update only if data exists
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.mobile = data.get('mobile', user.mobile)
    user.password = data.get('password', user.password)  # Hash this in real apps

    db.session.commit()

    # Prepare email content with profile changes
    email_body = f"""
    Hello {user.full_name},

    Your profile has been successfully updated. Here are your updated details:

    - Full Name: {user.full_name} {'(Updated)' if old_full_name != user.full_name else ''}
    - Email: {user.email} {'(Updated)' if old_email != user.email else ''}
    - Mobile: {user.mobile} {'(Updated)' if old_mobile != user.mobile else ''}

    If you did not make this change, please contact support immediately.

    Best Regards,
    Support Team
    """

    # Send notification with profile updates
    NotificationService.send_email(
        subject="Your Profile Has Been Updated",
        recipients=[user.email],
        body=email_body
    )

    return "User profile updated successfully!", "success"

    
