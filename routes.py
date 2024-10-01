import logging
from flask import render_template, request, jsonify
from app import app, db
from models import Participant
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        phone = data.get('phone')
        full_name = data.get('fullName')

        if not all([email, phone, full_name]):
            return jsonify({"success": False, "message": "All fields are required"}), 400

        new_participant = Participant(email=email, phone=phone, full_name=full_name)
        db.session.add(new_participant)
        db.session.commit()
        logger.info(f"New participant registered: {email}")
        return jsonify({"success": True, "message": "Registration successful!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        logger.error(f"Database error: {error_msg}")
        return jsonify({"success": False, "message": f"An error occurred while saving to the database: {error_msg}. Please try again."}), 500
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error: {error_msg}")
        return jsonify({"success": False, "message": f"An unexpected error occurred: {error_msg}. Please try again."}), 500
