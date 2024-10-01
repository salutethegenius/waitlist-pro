from flask import render_template, request, jsonify, url_for, redirect, flash, session
from app import db
from models import Participant, Admin
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
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

    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password):
                session['admin_id'] = admin.id
                flash('Logged in successfully.', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        return render_template('admin_login.html')

    @app.route('/admin_logout')
    @login_required
    def admin_logout():
        session.pop('admin_id', None)
        flash('Logged out successfully.', 'success')
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

    @app.route('/create_admin')
    def create_admin():
        try:
            admin = Admin.query.filter_by(username='admin').first()
            if admin:
                return jsonify({'success': False, 'message': 'Admin user already exists'}), 400
            
            new_admin = Admin(username='admin')
            new_admin.set_password('admin123')
            db.session.add(new_admin)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Admin user created successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'Failed to create admin user: {str(e)}'}), 500
