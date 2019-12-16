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

#------------------------------------------------------------------------------#
#test samples 
def example_data():
    """Populate a databse with sample data for testing purposes."""

    db.create_all()


    #Empty out data from previous runs
    User.query.delete()
    Metric.query.delete()
    Rec.query.delete()

    #Add sample users, books, and ratings

    #sample users
    user1 = User(user_id=1, email='123@test.com', password_hash='password')
    user2 = User(user_id=2, email='456@test.com', password_hash='password')
    user3 = User(user_id=3, email='789@test.com', password_hash='password')
    user4 = User(user_id=4, email='987@test.com', password_hash='password')
    user5 = User(user_id=5, email='654@test.com', password_hash='password')

    user1_goal = Goal(goal_id=1, 
                        user_id=1, 
                        goal="I want to eat more veggies", 
                        goal_date="2019-11-27 03:44:48.075786")

    user2_goal = Goal(goal_id=2, 
                        user_id=2, 
                        goal="Drink more water", 
                        goal_date="2019-11-27 03:44:48.075786")
    user3_goal = Goal(goal_id=3, 
                        user_id=3, 
                        goal="Exercise more", 
                        goal_date="2019-11-27 03:44:48.075786")
    user4_goal = Goal(goal_id=4, 
                        user_id=4, 
                        goal="Read more books", 
                        goal_date="2019-11-27 03:44:48.075786")
    user5_goal = Goal(goal_id=5, 
                        user_id=5, 
                        goal="Become vegetarian", 
                        goal_date="2019-11-27 03:44:48.075786")

    #Add all to session and commit
    db.session.add_all([user1, user2, user3, user4, user5, user1_goal, user2_goal, 
                        user3_goal, user4_goal, user5_goal])

    db.session.commit()
#------------------------------------------------------------------------------#
def connect_to_db(app, db_uri='postgresql:///goals'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__": # pragma: no cover
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    init_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False









