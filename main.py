import logging
from app import app

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=5001, debug=True)
