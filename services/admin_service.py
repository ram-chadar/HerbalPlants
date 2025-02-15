from typing import List
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