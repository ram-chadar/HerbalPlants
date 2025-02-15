from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.user_service import save_plant

# Define the Blueprint 'user'
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/submit_plant', methods=['GET', 'POST'])
def submit_plant():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()  # Convert form data to dictionary
            image_file = request.files.get('image')  # Get image file

            # Call the service function to save the plant
            result = save_plant(data, image_file)

            if result["success"]:
                flash("Plant submitted successfully!", "success")  # Flash success message
            else:
                flash(result["message"], "danger")  # Flash error message

        except Exception as e:
            flash(f"Server Error: {str(e)}", "danger")  # Flash error message

        # ✅ Redirect to the same page to ensure flash messages persist
        return redirect(url_for('page.user_home'))

    return render_template('user_home.html')
