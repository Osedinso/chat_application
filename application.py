import os
import time
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from wtform_fields import *
from models import *


app = Flask(__name__)

app.secret_key= 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jfonlqnwnhdtsz:47a59888138d16b111fe1c5e70713b361bea801048def326531cf86c9e842f2b@ec2-34-200-101-236.compute-1.amazonaws.com:5432/d306dbb732u1iu'
db = SQLAlchemy(app)

# Initialize login manager

login = LoginManager(app)

login.init_app(app)



@login.user_loader

def load_user(id):

    return User.query.get(int(id))



socketio = SocketIO(app, manage_session=False)



# Predefined rooms for chat

ROOMS = ["lounge", "news", "games", "coding"]





@app.route("/", methods=['GET', 'POST'])

def index():



    reg_form = RegistrationForm()



    # Update database if validation success

    if reg_form.validate_on_submit():

        username = reg_form.username.data

        password = reg_form.password.data



        # Hash password

        #hashed_pswd = pbkdf2_sha256.hash(password)



        # Add username & hashed password to DB

        user = User(username=username, hashed_pswd=hashed_pswd)

        db.session.add(user)

        db.session.commit()



        flash('Registered successfully. Please login.', 'success')

        return redirect(url_for('login'))



    return render_template("index.html", form=reg_form)





@app.route("/login", methods=['GET', 'POST'])

def login():



    login_form = LoginForm()



    # Allow login if validation success

    if login_form.validate_on_submit():

        user_object = User.query.filter_by(username=login_form.username.data).first()

        login_user(user_object)

        return redirect(url_for('chat'))



    return render_template("login.html", form=login_form)





@app.route("/logout", methods=['GET'])

def logout():



    # Logout user

    logout_user()

    flash('You have logged out successfully', 'success')

    return redirect(url_for('login'))





@app.route("/chat", methods=['GET', 'POST'])

def chat():



    if not current_user.is_authenticated:

        flash('Please login', 'danger')

        return redirect(url_for('login'))



    return render_template("chat.html", username=current_user.username, rooms=ROOMS)





@app.errorhandler(404)

def page_not_found(e):

    # note that we set the 404 status explicitly

    return render_template('404.html'), 404





@socketio.on('incoming-msg')

def on_message(data):

    """Broadcast messages"""



    msg = data["msg"]

    username = data["username"]

    room = data["room"]

    # Set timestamp

    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())

    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)





@socketio.on('join')

def on_join(data):

    """User joins a room"""



    username = data["username"]

    room = data["room"]

    join_room(room)



    # Broadcast that new user has joined

    send({"msg": username + " has joined the " + room + " room."}, room=room)





@socketio.on('leave')

def on_leave(data):

    """User leaves a room"""



    username = data['username']

    room = data['room']

    leave_room(room)

    send({"msg": username + " has left the room"}, room=room)



if __name__ == "__main__":

    app.run(debug=True)