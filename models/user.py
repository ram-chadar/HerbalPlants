import token
from models import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('Active', 'Inactive', 'Blocked'), default='Inactive')
    role = db.Column(db.Enum('User', 'Admin'), default='User')
    email_verified = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())

    # Relationship with Plant model (Use overlaps to avoid conflict)
    submitted_plants = db.relationship("Plant", backref="submitter", foreign_keys="[Plant.submitted_by]", overlaps="submitted_user")

    def __repr__(self):
        return f"<User {self.email}>"
