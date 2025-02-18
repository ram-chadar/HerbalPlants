from typing import List
from models.plant import Plant
from models.plant_category import PlantCategory
from models.user import User  
from models.user import db, User 

def get_all_users() -> List[User]:
    try:
        users = User.query.all()
        return users
    except Exception as e:
        print(f"An error occurred while retrieving users: {e}")
        return []
    
def change_user_status(user_id, status):
    try:
        user = User.query.get(user_id)
        if user:
            user.status = status
            db.session.commit()
            return "User status updated successfully"
        else:
            return "User not found"
    except Exception as e:
        return str(e)
    
def delete_user_by_id(user_id):
    try:
        user = User.query.get(user_id)  
        if user:
            db.session.delete(user)  
            db.session.commit()  
            return True
        return False  
    except Exception as e:
        db.session.rollback()  
        print(f"Error deleting user: {str(e)}")  
        return False    
    
    
# manage_categories function will be added here

def get_all_categories() -> List[PlantCategory]:
    try:
        categories = PlantCategory.query.all()
        return categories
    except Exception as e:
        print(f"An error occurred while retrieving categories: {e}")
        return []

def save_category(data) -> PlantCategory:
    try:
        new_category=PlantCategory(category_name=data['category_name'])
        
        db.session.add(new_category)
        db.session.commit()
        return new_category
    except Exception as e:
        print(f"An error occurred while adding category: {e}")
        return None


def edit_plant_category(category_id, category_name):
    try:
        category = PlantCategory.query.get(category_id)
        if not category:
            return False  # Category not found

        category.category_name = category_name
        db.session.commit()
        return True  # Successfully updated
    except Exception as e:
        db.session.rollback()
        print(f"Error updating category: {e}")
        return False



# plant

def get_all_plants() -> List[Plant]:
    try:
        plants = Plant.query.all()
         # Fetch user details for each plant
        for plant in plants:
            plant.submitter = User.query.get(plant.submitted_by)  # Fetch User Object
        return plants
    except Exception as e:
        print(f"An error occurred while retrieving plants: {e}")
        return []
    
def update_plant_status(plant_id, status):
    plant = Plant.query.get(plant_id)
    if not plant:
        return "Plant not found"

    plant.submission_status = status
    db.session.commit()
    
    return f"Plant status updated to {status}"    