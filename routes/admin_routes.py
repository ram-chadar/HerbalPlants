from email.mime import message
from flask import Blueprint, redirect, render_template, request, url_for
from services.admin_service import get_all_categories, get_all_users, save_category

# Define the Blueprint 'admin'
admin_bp = Blueprint('admin', __name__, url_prefix='/admin') 

@admin_bp.route('/manage_users')
def manage_users():
    users = get_all_users() 
    return render_template("manage_users.html", users=users)

@admin_bp.route("/edit-user/<int:user_id>")
def edit_user(user_id):
    # Logic to fetch and edit user details
    pass

@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    # Logic to delete user
    pass


# categories paths

@admin_bp.route('/manage_categories', methods=['GET'])
def manage_categories():
    # Logic to fetch and display categories
    categories=get_all_categories()
    return render_template("manage_categories.html", categories=categories)

# add category
@admin_bp.route('/add_category', methods=['POST'])
def add_category():
    # Logic to add category
    # handle category form
    data = request.form
    new_category = save_category(data)
    return redirect(url_for('admin.manage_categories'))

@admin_bp.route("/edit_category/<int:category_id>")
def edit_category(category_id):
    # Logic to fetch and edit user details
    pass

@admin_bp.route("/delete-category/<int:category_id>")
def delete_category(category_id):
    # Logic to delete user
    pass

    

