from email.mime import message
from flask import Blueprint, flash, redirect, render_template, request, url_for
from services.admin_service import change_user_role, change_user_status, delete_user_by_id, edit_plant_category, get_all_categories, get_all_plants, get_all_users, save_category, update_plant_status
from services.auth_service import login_required
from services.statistics_metrics_service import (
    get_total_registered_users,
    get_active_vs_inactive_users,
    get_total_plant_submissions,
    get_submission_status_counts,
    get_most_common_plant_categories,
    get_most_active_contributors,
    get_unique_visitors_per_period,
    get_visitors_per_period,
)
# Define the Blueprint 'admin'
admin_bp = Blueprint('admin', __name__, url_prefix='/admin') 

@admin_bp.route('/manage_users')
@login_required
def manage_users():
    users = get_all_users() 
    return render_template("manage_users.html", users=users)

@admin_bp.route("/delete-user/<int:user_id>")
@login_required
def delete_user(user_id):
    try:
        result = delete_user_by_id(user_id)  # Call the service function
        if result:
            flash("User deleted successfully!", "success")
        else:
            flash("User not found or could not be deleted!", "danger")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")

    return redirect(url_for("admin.manage_users"))  # Redirect back to user management page




@admin_bp.route("/change_status/<int:user_id>", methods=["GET","POST"])
@login_required
def change_status(user_id):
    status = request.args.get("status")
    if not status:
        flash("Status is required", "danger")
        return redirect(url_for("admin.manage_users"))  # Redirect back

    message = change_user_status(user_id, status)
    
    if "not found" in message:
        flash(message, "danger")  # Error message
    else:
        flash(message, "success")  # Success message

    return redirect(url_for("page.admin_home"))  

@admin_bp.route("/change_role/<int:user_id>", methods=["GET", "POST"])
@login_required
def change_role(user_id):
    role = request.args.get("role")
    if not role:
        flash("Role is required", "danger")
        return redirect(url_for("admin.manage_users"))  # Redirect back

    message = change_user_role(user_id, role)  # Function to update role in DB
    
    if "not found" in message:
        flash(message, "danger")  # Error message
    else:
        flash(message, "success")  # Success message

    return redirect(url_for("page.admin_home"))  



# categories paths*******************************************

@admin_bp.route('/manage_categories', methods=['GET'])
@login_required
def manage_categories():
    # Logic to fetch and display categories
    categories=get_all_categories()
    return render_template("manage_categories.html", categories=categories)

# add category
@admin_bp.route('/add_category', methods=['POST'])
@login_required
def add_category():
    # Logic to add category
    # handle category form
    data = request.form
    new_category = save_category(data)
    return redirect(url_for('admin.manage_categories'))

# edit plant category
@admin_bp.route("/edit-category/<int:category_id>", methods=["GET","POST"])
@login_required
def edit_category(category_id):
    category_name = request.form.get("category_name")

    if edit_plant_category(category_id, category_name):
        flash("Category updated successfully!", "success")
    else:
        flash("Failed to update category.", "danger")

    return redirect(url_for("page.admin_home"))

# approve plants
@admin_bp.route('/approve_plants', methods=['GET'])
@login_required
def approve_plants():
    plants = get_all_plants()  # Assuming you have a service function to get all plants
    return render_template("approve_plants.html", plants=plants)


@admin_bp.route("/change_plant_status/<int:plant_id>", methods=["GET","POST"])
@login_required
def change_plant_status(plant_id):
    status = request.args.get("status")
    if not status:
        flash("Status is required", "danger")
        return redirect(url_for("admin.approve_plants")) 

    message = update_plant_status(plant_id, status)
    
    if "not found" in message:
        flash(message, "danger")  # Error message
    else:
        flash(message, "success")  # Success message

    return redirect(url_for("admin.approve_plants"))


@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    """Fetches statistics and renders the dashboard."""
    status_counts = get_submission_status_counts()

    metrics = {
        "total_users": get_total_registered_users(),
        "active_users": get_active_vs_inactive_users()["active_users"],
        "inactive_users": get_active_vs_inactive_users()["inactive_users"],
        "blocked_users": get_active_vs_inactive_users()["blocked_users"],
        "total_plants": get_total_plant_submissions(),
        "approved_plants": status_counts.get("Approved", 0),
        "pending_plants": status_counts.get("Pending", 0),
        "rejected_plants": status_counts.get("Rejected", 0),
        "common_categories": get_most_common_plant_categories(),
        "top_contributors": get_most_active_contributors(),
        "daily_visitors": get_visitors_per_period("day")["visitors"],
        "monthly_visitors": get_visitors_per_period("month")["visitors"],
        "daily_unique_visitore":get_unique_visitors_per_period("day")["unique_visitors"],
        "monthly_unique_visitore":get_unique_visitors_per_period("month")["unique_visitors"],
    }
    
    return render_template("dashboard.html", metrics=metrics)
      

    

