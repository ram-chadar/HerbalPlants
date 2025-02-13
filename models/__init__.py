from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models
from models.analytics import Analytics
from models.user import User
from models.plant import Plant
from models.visitor import Visitor
from models.plant_category import PlantCategory
