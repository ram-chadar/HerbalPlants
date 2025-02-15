from math import log
from typing import List
from models.user import User  
from models.user import db, User 

def get_all_users() -> List[User]:
    try:
        users = User.query.all()
        return users
    except Exception as e:
        print(f"An error occurred while retrieving users: {e}")
        return []