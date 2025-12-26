import os

# Navigates to the base directory of the project outside of the src folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# Database configuration
# Default to a SQLite database located in the data folder for development
default_db= 'sqlite:///' + os.path.join(BASE_DIR, 'data', 'patient_file_tracking.db')

#Change database URI based on environment variable, useful for production deployment
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default_db)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'your_secret_key_here'  # Replace with a secure key in production