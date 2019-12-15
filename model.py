"""Models and database functions for User goals"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from werkzeug.security import generate_password_hash, check_password_hash

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
db = SQLAlchemy()

################################################################################

class User(db.Model):
    """User of goals page"""
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), nullable=True, index=True)
    email = db.Column(db.String(70), nullable=True, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
 #below our user model, we will create our hashing functions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Helpful representation when printed"""

        return f"<User Info: user_id= {self.user_id}, name= {self.name}, email={self.email}>"

class Goal(db.Model):
    """Recommendations table"""
    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    goal = db.Column(db.Text, nullable=True)
    goal_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", 
                                backref=db.backref("goals"))

    def __repr__(self):
        """Helpfull representation when printed"""
        return f"""<rec_date: {self.goal_date}, 
                    user_id: {self.user_id},
                    goal: {self.goal}>"""

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///goals'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")













