from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app import db
from models import Participant
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from functools import wraps

logger = logging.getLogger(__name__)

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        logger.info(f"Received registration data: {data}")
        if not data:
            logger.error("No JSON data received in the request")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        try:
            participant = Participant(email=data['email'], phone=data['phone'], full_name=data['fullName'])
            db.session.add(participant)
            db.session.commit()
            logger.info(f"New participant registered: {participant.email}")
            return jsonify({'success': True}), 200
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Attempt to register with existing email: {data.get('email')}")
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"SQLAlchemyError during registration: {str(e)}")
            return jsonify({'success': False, 'message': 'An error occurred during registration'}), 500
        except KeyError as e:
            logger.error(f"KeyError during registration: {str(e)}")
            return jsonify({'success': False, 'message': f'Missing required field: {str(e)}'}), 400
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['admin_logged_in'] = True
                flash('You have been successfully logged in.', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        return render_template('admin_login.html')

    @app.route('/admin_logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('admin_login'))

    @app.route('/admin_dashboard')
    @login_required
    def admin_dashboard():
        participants = Participant.query.all()
        return render_template('admin_dashboard.html', participants=participants)

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/test_db')
    def test_db():
        try:
            participants = Participant.query.all()
            return jsonify({'success': True, 'message': f'Database connection successful. {len(participants)} participants found.'}), 200
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {str(e)}")
            return jsonify({'success': False, 'message': f'Database connection failed: {str(e)}'}), 500
