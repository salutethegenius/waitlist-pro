import logging
from flask import render_template, request, jsonify, redirect, url_for, session, flash
from extensions import app, db, mail
from models import Participant
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from flask_mail import Message
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session['admin_logged_in']:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

def send_confirmation_email(participant):
    token = participant.generate_confirmation_token()
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('email/confirm_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    msg = Message(subject=subject, recipients=[participant.email], html=html)
    mail.send(msg)

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
        
        send_confirmation_email(new_participant)
        
        logger.info(f"New participant registered: {email}")
        return jsonify({"success": True, "message": "Registration successful! Please check your email to confirm your registration."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        logger.error(f"Database error: {error_msg}")
        return jsonify({"success": False, "message": f"An error occurred while saving to the database: {error_msg}. Please try again."}), 500
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error: {error_msg}")
        return jsonify({"success": False, "message": f"An unexpected error occurred: {error_msg}. Please try again."}), 500

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = Participant.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))
    
    user = Participant.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':  # Replace with secure authentication
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    participants = Participant.query.all()
    return render_template('admin_dashboard.html', participants=participants)

@app.route('/admin/delete/<int:participant_id>', methods=['POST'])
@admin_required
def delete_participant(participant_id):
    participant = Participant.query.get_or_404(participant_id)
    db.session.delete(participant)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
