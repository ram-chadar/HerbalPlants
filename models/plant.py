from models import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Plant(db.Model):
    __tablename__ = 'plant'

    plant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('plant_category.category_id'), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    submission_status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending')
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())

    benefits = db.Column(db.Text, nullable=False)
    uses = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # Store image filename

    # Relationship to fetch submitted user details
    submitted_user = relationship("User", foreign_keys=[submitted_by])

    def __repr__(self):
        return f"<Plant {self.name}, Status: {self.submission_status}>"
