import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully")

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
