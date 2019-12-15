"""User goals"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, g 
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Goal, connect_to_db, db

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEFG"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

#------------------------------------------------------------------------------#
@app.route('/')
def index():
    """Homepage."""
    
    return render_template('homepage.html')

#------------------------------------------------------------------------------#
@app.route('/register', methods=["GET"])
def registration_form(): 
    """Render template registration.html"""

    return render_template('register.html')

@app.route('/register', methods=["POST"])
def registration_process(): 
    """Registering user and saving form inputs to users datatable"""

    name = request.form["name"]
    email = request.form["email"]
    password_hash = request.form["password"]

    # Adding new user to users data table 
    new_user = User(name=name, 
                    email=email,
                    password_hash=password_hash)

    new_user.set_password(password_hash)

    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.user_id


    return redirect('/')

#------------------------------------------------------------------------------#
@app.route('/login', methods=["GET"])
def login(): 
    """Render template login.html"""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_process(): 
    """User login process"""

    email = request.form["email"]
    password_hash = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password_hash):

        session["user_id"] = user.user_id

        flash('Logged in')
        return redirect('/')
    else:
        flash('You have entered the wrong email or password.')
        return redirect('/login')

#------------------------------------------------------------------------------#
@app.route("/logout")
def logout():
    """Log out user from session"""

    #delete info from session
    del session["user_id"]
    flash('Logged Out.')
    return redirect('/')

#------------------------------------------------------------------------------#
@app.route('/goals', methods=["GET"])
def comments(): 
    """Render recommendations.html"""
    goals = Goal.query.filter_by(user_id=session['user_id']).all()

    return render_template("goals.html", goals=goals)


@app.route('/goals', methods=["POST"])
def get_comments(): 
    """Save user comments in recs datatable"""
    goal = request.form["goal"]

    add_comment = Goal(user_id=session['user_id'], goal=goal)
    db.session.add(add_comment)
    db.session.commit()

    return redirect('/goals')


#------------------------------------------------------------------------------#
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')