from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.auth_service import login_required
from services.common_service import get_profile, update_user_profile
from services.user_service import get_user_submissions, save_plant

# Define the Blueprint 'user'
user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/submit_plant', methods=['GET', 'POST'])
@login_required
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

        return redirect(url_for('page.user_home'))

    return render_template('user_home.html')


@user_bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user_id = session.get("user_id")
    
    if not user_id:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for("auth_bp.login"))  

    user_profile = get_profile(user_id)

    return render_template('profile.html', profile=user_profile)
  


@user_bp.route('/update_user', methods=['POST'])
@login_required
def update_user():
    try:
        user_id = session.get("user_id")
        if not user_id:
            flash("You must be logged in to update your profile.", "warning")
            return redirect(url_for("auth_bp.login"))  # Redirect to login page

        # Retrieve form data correctly
        form_data = {
            "user_id": user_id,
            "full_name": request.form.get('full_name'),
            "email": request.form.get('email'),
            "mobile": request.form.get('mobile'),
            "password": request.form.get('password')
        }
        message, category = update_user_profile(form_data)  # Call service
        flash(message, category)

        return redirect(url_for('user.profile'))  # Redirect back to profile page

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("user.profile"))

    except Exception as e:
        flash("An unexpected error occurred.", "danger")
        return redirect(url_for("user.profile"))
    

@user_bp.route('/my_submission')
def my_submission():
    # Assuming you have a user ID stored in the session when the user logs in
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('page.login'))  # Redirect to login if no user is logged in

    # Call the service to get the user's submissions
    submissions = get_user_submissions(user_id)

    # Render the 'my_submission.html' page with the submissions data
    return render_template('my_submission.html', submissions=submissions)    