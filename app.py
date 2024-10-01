import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    try:
        # SQLAlchemy configuration
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            logger.info(f"DATABASE_URL is set: {database_url[:10]}...") # Print first 10 characters for security
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
            logger.info(f"Modified DATABASE_URL: {database_url[:10]}...")
        else:
            logger.error("DATABASE_URL is not set")
            return None

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "a_secure_secret_key")

        db.init_app(app)

        with app.app_context():
            from models import Participant
            try:
                db.create_all()
                logger.info("Database tables created successfully")
            except Exception as e:
                logger.error(f"Error creating database tables: {str(e)}")
                return None

        from routes import register_routes
        register_routes(app)

        logger.info("Application created successfully")
        return app

    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        return None

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    if app:
        logger.info("Starting Flask application")
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        logger.error("Failed to create the Flask app due to configuration errors.")
