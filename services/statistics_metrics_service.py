from models import db
from models.user import User
from models.plant import Plant
from models.plant_category import PlantCategory
from models.visitor import Visitor
from sqlalchemy import func, desc
from datetime import datetime

def get_total_registered_users():
    """Returns the total number of registered users."""
    return db.session.query(func.count(User.user_id)).scalar()

def get_active_vs_inactive_users():
    """Returns the number of active vs. inactive users."""
    active_users = db.session.query(func.count(User.user_id)).filter(User.status == 'Active').scalar()
    inactive_users = db.session.query(func.count(User.user_id)).filter(User.status == 'Inactive').scalar()
    return {"active_users": active_users, "inactive_users": inactive_users}

def get_total_plant_submissions():
    """Returns the total number of plant submissions."""
    return db.session.query(func.count(Plant.plant_id)).scalar()

def get_submission_status_counts():
    """Returns the count of approved, pending, and rejected plants."""
    status_counts = db.session.query(
        Plant.submission_status, func.count(Plant.plant_id)
    ).group_by(Plant.submission_status).all()
    return {status: count for status, count in status_counts}

def get_most_common_plant_categories(limit=5):
    """Returns the most commonly submitted plant categories."""
    categories = db.session.query(
        PlantCategory.category_name, func.count(Plant.plant_id)
    ).join(Plant, Plant.category_id == PlantCategory.category_id) \
     .group_by(PlantCategory.category_name) \
     .order_by(desc(func.count(Plant.plant_id))) \
     .limit(limit) \
     .all()
    return [{"category": cat, "count": count} for cat, count in categories]

def get_most_active_contributors(limit=5):
    """Returns the most active contributors (users submitting the most plants)."""
    contributors = db.session.query(
        User.full_name, func.count(Plant.plant_id)
    ).join(Plant, Plant.submitted_by == User.user_id) \
     .group_by(User.full_name) \
     .order_by(desc(func.count(Plant.plant_id))) \
     .limit(limit) \
     .all()
    return [{"user": user, "submissions": count} for user, count in contributors]

def get_visitors_per_period(period='day'):
    """Returns the number of visitors per day or month based on visit_time."""
    if period == 'day':
        date_filter = datetime.utcnow().date()
        visitors_count = db.session.query(func.count(Visitor.visitor_id)) \
            .filter(func.date(Visitor.visit_time) == date_filter) \
            .scalar()
    elif period == 'month':
        start_date = datetime.utcnow().replace(day=1)
        visitors_count = db.session.query(func.count(Visitor.visitor_id)) \
            .filter(Visitor.visit_time >= start_date) \
            .scalar()
    else:
        return {"error": "Invalid period. Use 'day' or 'month'."}
    
    return {"period": period, "visitors": visitors_count}
