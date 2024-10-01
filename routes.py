from flask import render_template, request, jsonify
from app import db
from models import Participant
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

logger = logging.getLogger(__name__)

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        participant = Participant(email=data['email'], phone=data['phone'], full_name=data['fullName'])
        try:
            db.session.add(participant)
            db.session.commit()
            return jsonify({'success': True}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'An error occurred'}), 500

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/test_db')
    def test_db():
        try:
            participants = Participant.query.all()
            return jsonify({'success': True, 'message': f'Database connection successful. {len(participants)} participants found.'}), 200
        except SQLAlchemyError as e:
            return jsonify({'success': False, 'message': f'Database connection failed: {str(e)}'}), 500
