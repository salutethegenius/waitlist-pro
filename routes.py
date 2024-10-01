from flask import render_template, request, jsonify
from app import app, db
from models import Participant

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    phone = data.get('phone')
    full_name = data.get('fullName')

    if not all([email, phone, full_name]):
        return jsonify({"success": False, "message": "All fields are required"}), 400

    new_participant = Participant(email=email, phone=phone, full_name=full_name)
    db.session.add(new_participant)
    
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Registration successful!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "An error occurred. Please try again."}), 500
