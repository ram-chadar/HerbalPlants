from sqlalchemy import create_engine, text
import pymysql
import os

DB_NAME = "herbalplantdb"
USERNAME = "root"
PASSWORD = "admin"
HOST = "localhost"

# Connect to MySQL server (without specifying the database)
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}")

# Create the database if it doesn't exist
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    conn.commit()  # Commit is needed in some MySQL versions

# Now use the database in your SQLAlchemy config
class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_URL = 'http://127.0.0.1:5000'
    SECRET_KEY = os.urandom(24)  # For token generation
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'dsa360solution@gmail.com'
    MAIL_PASSWORD = 'jchu rvuf haae kewz'
    MAIL_DEFAULT_SENDER = 'dsa360solution@gmail.com'
