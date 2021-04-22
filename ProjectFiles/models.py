from database import db
from datetime import datetime


class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text, date, id):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = id

    def __repr__(self):
        return f"Event('{self.id}', '{self.title}', '{self.text}, '{self.date}')"


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    password = db.Column("password", db.String(30))
    events = db.relationship("Event", backref="user", lazy=True)
<<<<<<< HEAD
=======
    #Trying to figure out a way to save all Event id values into a string that will
    #be recognized by the database
    # rsvpEvents = db.Column("rsvpEvents", db.ARRAY(db.Integer, db.ForeignKey('event.id'), dimensions=1))
>>>>>>> 2efdd5ae23a86901b423f6df85262555df214ea2

    def __init__(self, name, pwd):
        self.username = name
        self.password = pwd
        # self.rsvpEvents = []

    def __repr__(self):
        return f"User('{self.id}', '{self.username}, '{self.password}')"

<<<<<<< HEAD

class RSVP(db.Model):
    RSVP_id = db.Column("RSVP_id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column("event_id", db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def __repr__(self):
        return f"RSVP('{self.user_id}', '{self.event_id}')"
=======
>>>>>>> 2efdd5ae23a86901b423f6df85262555df214ea2
