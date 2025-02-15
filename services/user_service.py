import os
from models import db
from werkzeug.utils import secure_filename
from models.plant import Plant

UPLOAD_FOLDER = 'static/upload/plants'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_plant(data, image_file):
    try:
        # Handle image upload
        image_filename = None  # Default: No image
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)  # Save image to folder
            image_filename = filename  # Store filename in DB

        # Create a new Plant instance using extracted data
        new_plant = Plant(
            name=data['name'],  # Required
            description=data['description'],  # Required
            category_id=data['category_id'],  # Required
            submitted_by=data['submitted_by'],  # Required
            approved_by=data.get('approved_by'),  # Optional
            submission_status=data.get('submission_status', 'Pending'),  # Default to 'Pending'
            benefits=data['benefits'],  # Required
            uses=data['uses'],  # Required
            image=image_filename  # Store filename in DB
        )

        # Add and commit the new plant to the database
        db.session.add(new_plant)
        db.session.commit()

        return {"success": True, "message": "Plant saved successfully!"}

    except Exception as e:
        db.session.rollback()
        return {"success": False, "message": f"Error saving plant: {str(e)}"}