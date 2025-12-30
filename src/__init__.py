from flask import Flask
from src import config
from src.extensions import db, migrate

def create_app(config_class = None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config)

    #initialize SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)
    

# Import models after initializing db to avoid circular imports
    from src import models

    return app