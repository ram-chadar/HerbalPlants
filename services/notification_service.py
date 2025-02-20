from flask_mail import Message
from flask import current_app

class NotificationService:
    """Handles email notifications synchronously."""

    @staticmethod
    def send_email(subject, recipients, body):
        """Send email synchronously."""
        with current_app.app_context():  # Ensure the app context is available
            msg = Message(subject, recipients=recipients)
            msg.body = body
            try:
                # Send the email through the Flask-Mail extension
                current_app.extensions['mail'].send(msg)
                current_app.logger.info(f"Email sent to {recipients} | Subject: {subject}")
            except Exception as e:
                current_app.logger.error(f"Error sending email: {e}")

    @staticmethod
    def notify_user_status_change(user):
        """Notify user when their account status changes."""
        NotificationService.send_email(
            subject="Account Status Changed",
            recipients=[user.email],
            body=f"Your account status has been updated to: {user.status}",
        )

    @staticmethod
    def notify_user_deletion(user):
        """Notify user that their account has been deleted."""
        NotificationService.send_email(
            subject="Account Deleted",
            recipients=[user.email],
            body="Your account has been removed from our system.",
        )

    @staticmethod
    def notify_plant_status_update(user, plant):
        """Notify user when their plant submission status changes."""
        NotificationService.send_email(
            subject="Plant Submission Status Updated",
            recipients=[user.email],
            body=f"Your plant submission '{plant.name}' has been updated to: {plant.submission_status}",
        )
