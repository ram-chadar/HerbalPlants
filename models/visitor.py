from models import db
from sqlalchemy.sql import func

class Visitor(db.Model):
    __tablename__ = 'visitor'

    visitor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip_address = db.Column(db.String(50), nullable=False)
    visit_time = db.Column(db.TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Visitor {self.ip_address}>"
