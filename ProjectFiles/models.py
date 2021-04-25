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
    # Trying to figure out a way to save all Event id values into a string that will
    # be recognized by the database
    # RSVP_events =

    def __init__(self, name, pwd):
        self.username = name
        self.password = pwd

    def __repr__(self):
        return f"User('{self.id}', '{self.username}, '{self.password}')"

# an attempt to create friends list
class Friends(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))
    user_id_2 = db.Column("user_id_2", db.Integer, db.ForeignKey('user.id_2'))
    friendUsername = db.Column("username", db.String(100))

    def __init__(self, id, id_2, friendUsername):
        self.userID = id
        self.userID_2 = id_2
        self.friendUsername = friendUsername

    def __repr__(self):
        return f"User('{self.id}', '{self.user_id}', '{self.user_id_2}', '{self.friend_username}')"
