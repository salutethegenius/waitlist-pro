import os
from extensions import db, app
from models import Participant

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully")

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
