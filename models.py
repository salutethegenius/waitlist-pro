from app import db

class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    def __init__(self, email, phone, full_name):
        self.email = email
        self.phone = phone
        self.full_name = full_name

    def __repr__(self):
        return f'<Participant {self.email}>'
