from models import db

class PlantCategory(db.Model):
    __tablename__ = 'plant_category'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationship: One category can have many plants
    plants = db.relationship('Plant', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.category_name}>"
