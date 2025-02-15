from flask import Blueprint, render_template
from services.admin_service import get_all_users

# Define the Blueprint 'admin'
admin = Blueprint('admin', __name__)

@admin.route('/manage_users')
def manage_users():
    users = get_all_users();
    return render_template("manage_user.html", users=users)