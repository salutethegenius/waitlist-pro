from extensions import db
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def generate_confirmation_token(self):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt='email-confirm-salt')

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt='email-confirm-salt',
                max_age=expiration
            )
        except:
            return False
        return email
