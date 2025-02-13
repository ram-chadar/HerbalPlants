from models import db
from sqlalchemy.sql import func

class Analytics(db.Model):
    __tablename__ = 'analytics'

    analytics_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_users = db.Column(db.Integer, default=0)
    total_plants = db.Column(db.Integer, default=0)
    total_visitors = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<Analytics Users:{self.total_users}, Plants:{self.total_plants}, Visitors:{self.total_visitors}>"
