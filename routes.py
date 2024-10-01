from flask import render_template, request, jsonify, url_for
from app import db
from models import Participant
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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

    @app.route('/admin_login')
    def admin_login():
        return render_template('admin_login.html')

    @app.route('/dashboard')
    def dashboard():
        # For now, we'll just render a simple dashboard template
        # In the future, you might want to add authentication to this route
        return render_template('dashboard.html')

    @app.route('/test_db')
    def test_db():
        try:
            participants = Participant.query.all()
            return jsonify({'success': True, 'message': f'Database connection successful. {len(participants)} participants found.'}), 200
        except SQLAlchemyError as e:
            return jsonify({'success': False, 'message': f'Database connection failed: {str(e)}'}), 500

    @app.route('/test_create_participant')
    def test_create_participant():
        try:
            new_participant = Participant(email='test@example.com', phone='1234567890', full_name='Test User')
            db.session.add(new_participant)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Test participant created successfully.'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Failed to create test participant: {str(e)}'}), 500

    # Add other routes here
