from flask import Flask
from applications.database import db
from flask_security import Security

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = "TrekkingApp-secret-key "
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trekking.sqlite3"
    db.init_app(app)
    app.app_context().push()

    return app

app = create_app()
from applications.controllers import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        Admin = User.query.filter_by(username = "admin").first()
        if not Admin:
            admin = User(username = "admin", password = "admin123", email = "admin123@gmail.com", role = admin)
            db.session.add(admin)
            db.session.commit()

    app.run()


