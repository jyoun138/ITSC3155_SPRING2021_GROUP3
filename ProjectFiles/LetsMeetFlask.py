import os  # os is used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

from database import db
from models import Event as Event, User as User, RSVP as RSVP, Comment as Comment, Friend as Friend
from datetime import datetime, date
import calendar
import math as math
from forms import RegisterForm, LoginForm, EventForm, CommentForm, FriendForm
import bcrypt

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///letsmeet_flask_event_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'
# Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# db = SQLAlchemy(app)
# Setup models
with app.app_context():
    db.create_all() # run under the app context


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # Check to see everything entered is valid
    if request.method == 'POST' and login_form.validate_on_submit():
        # Check to see if the User information entered exists in the database
        the_user = db.session.query(User).filter_by(username=request.form['username']).one_or_none()
        # If the user doesn't exist then refresh the page
        if the_user == None:
            return render_template('LetsMeetLogin.html', form=login_form)
        # Decrypt the password to log the user in
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.username
            session['user_id'] = the_user.id
            return redirect(url_for('get_events'))

        login_form.password.errors = ["Incorrect username or password"]
        return render_template('LetsMeetLogin.html', form=login_form)
    else:
        return render_template('LetsMeetLogin.html', form=login_form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    register_form = RegisterForm()
    # Check to see everything entered is valid
    if request.method == 'POST' and register_form.validate_on_submit():
        # hash password
        h_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        username = request.form['username']
        new_user = User(username, h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = username
        session['user_id'] = new_user.id
        return redirect(url_for('get_events'))
    return render_template('LetsMeetRegister.html', form=register_form)


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if session.get('user'):
        my_events = db.session.query(Event).all()
        eventDays = []
        for i in my_events:
            eventDays.append(i.date)
        if request.method == 'POST':
            month = int(request.form["calendar_month"])
        else:
            month = date.today().month
        # Returns a template with many python arguments to make the calendar work on the Home page
        return render_template('LetsMeetMain.html', today=date.today(), math=math, calendar=calendar,
                               user=session['user'], date=date, eventDates=eventDays, events=my_events, sum=sum,
                               enumerate=enumerate, month=month)
    return redirect(url_for('login'))


@app.route('/events')
def get_events():
    if session.get('user'):
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).all()
        return render_template('LetsMeetEvents.html', events=my_events, user=session['user'])
    return redirect(url_for('login'))


@app.route('/events/<event_id>')
def get_event(event_id):
    if session.get('user'):
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        this_RSVP = db.session.query(RSVP).filter_by(event_id=event_id, user_id=session['user_id']).one_or_none()
        all_RSVPs = db.session.query(RSVP).filter_by(event_id=event_id).all()
        form = CommentForm()
        return render_template('LetsMeetEvent.html', event=my_event, user=session['user'], user_id=session['user_id'],
                               this_RSVP=this_RSVP, all_RSVPs=all_RSVPs, form=form)
    return redirect(url_for('login'))


# Trying to figure out how to add RSVP'd Event id's to Users database (see models.py/Users)
@app.route('/events/rsvp/<event_id>', methods=['GET', 'POST'])
def RSVP_event(event_id):
    if session.get('user'):
        new_RSVP = RSVP(session['user_id'], session['user'], event_id)
        db.session.add(new_RSVP)
        db.session.commit()
        return redirect(url_for('get_event', event_id=event_id))
    else:
        return redirect(url_for('login'))


@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if session.get('user'):
        eventForm = EventForm()
        if request.method == 'POST' and eventForm.validate_on_submit():
            title = request.form['title']
            text = request.form['eventText']
            eventDate = request.form['eventDate']
            new_record = Event(title=title, text=text, date=eventDate, id=session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('get_events'))
        else:
            return render_template('LetsMeetNew.html', user=session['user'], form=eventForm, today=date.today())
    return redirect(url_for('login'))


@app.route('/events/edit/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if session.get('user'):
        eventForm = EventForm()
        if request.method == 'POST' and eventForm.validate_on_submit():
            my_event = db.session.query(Event).filter_by(id=event_id).one()
            my_event.title = request.form['title']
            my_event.text = request.form['eventText']
            my_event.date = request.form['eventDate']
            db.session.add(my_event)
            db.session.commit()
            return redirect(url_for('get_events'))
        else:
            my_event = db.session.query(Event).filter_by(id=event_id).one()
            eventForm.title.data = my_event.title
            eventForm.eventText.data = my_event.text
            eventForm.eventDate.data = my_event.date
            return render_template('LetsMeetNew.html', event=my_event, user=session['user'], form=eventForm,
                                   today=date.today())
    else:
        return redirect(url_for('login'))


@app.route('/events/<event_id>/remove_event')
def remove_event(event_id):
    if session.get('user'):
        db.session.query(Event).filter_by(id=event_id).delete()
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/events/rsvp/<event_id>/remove_RSVP_event/<RSVP_id>', methods=['GET', 'POST'])
def remove_RSVP_event(event_id, RSVP_id):
    if session.get('user'):
        db.session.query(RSVP).filter_by(id=RSVP_id).delete()
        db.session.commit()
    return redirect(url_for('get_event', event_id=event_id))

@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('login'))


@app.route('/events/<event_id>/comment', methods=['POST'])
def new_comment(event_id):
    if session.get('user'):
        commentForm = CommentForm()
        # validate_on_submit only validates using POST
        if commentForm.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(event_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_event', event_id=event_id))

    else:
        return redirect(url_for('login'))


@app.route('/calendar')
def calendarpage():
    if session.get('user'):
        my_events = db.session.query(Event).all()
        eventDays = []
        for i in my_events:
            eventDays.append(i.date)
        # Returns a template with many python arguments to make the calendar work on the Home page
        return render_template('LetsMeetCalendar.html', today=date.today(), math=math, calendar=calendar,
                               user=session['user'], date=date, eventDates=eventDays, events=my_events, sum=sum,
                               enumerate=enumerate)
    return redirect(url_for('login'))


# route for friends list
@app.route('/friends')
def friendspage():
    if session.get('user'):
        # displays list of friends
        list_friends = db.session.query(Friend).filter_by(user_id=session['user_id']).all()
        return render_template('LetsMeetFriends.html', friends=list_friends, user=session['user'])
    else:
        return redirect(url_for('login'))



# route for adding users as friends
@app.route('/friends/new', methods=['GET', 'POST'])
def add_friend():
    if session.get('user'):
        friendForm = FriendForm()

        if request.method == 'POST' and friendForm.validate_on_submit():

            friend_username = request.form['friendUsername']

            new_friend = Friend(session['user_id'], friend_username)
            db.session.add(new_friend)
            db.session.commit()
            return redirect(url_for('friendspage'))
        else:
            list_users = db.session.query(User).all()
            return render_template('LetsMeetAddFriend.html', users=list_users, user=session['user'], form=friendForm)

    else:
        return redirect(url_for('login'))

@app.route('/friends/<friend_id>')
def friend_details(friend_id):
    if session.get('user'):
        my_friend = db.session.query(Friend).filter_by(id=friend_id).one()

        return render_template('LetsMeetEvent.html', friend=my_friend, user=session['user'], user_id=session['user_id'])
    return redirect(url_for('login'))

@app.route('/friends/<friend_id>/remove_friend')
def remove_friend(friend_id):
    if session.get('user'):
        db.session.query(Friend).filter_by(id=friend_id).delete()
        db.session.commit()
        return redirect(url_for('friendspage'))
    return redirect(url_for('login'))

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
