from flask import Flask
from applications.database import db
from flask_cors import CORS
from applications.models import User
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    
    app = Flask(__name__)
    app.debug = True
    app.config.from_object("applications.config.Config")

    CORS(app, origins = ["http://localhost:5173", "http://127.0.0.1:5173"], supports_credentials = True)

    db.init_app(app)
    JWTManager(app)
    app.app_context().push()

    return app

app = create_app()

from applications.controllers.auth import *
from applications.controllers.admin import *
from applications.controllers.staff import *
from applications.controllers.trekkers import *


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        Admin = User.query.filter_by(username = "admin").first()
        if not Admin:
            admin = User(username = "admin", password = generate_password_hash("admin"), email = "admin123@gmail.com", phone ="123456789", role = "admin")
            db.session.add(admin)
            db.session.commit()

    app.run()


