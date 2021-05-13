from database import db
from datetime import datetime, date


class Event(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)
    image = db.Column("image", db.Text)
    image_name = db.Column("image_name", db.Text)
    image_type = db.Column("image_type", db.Text)

    def __init__(self, title, text, date, id, image, image_name, image_type):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = id
        self.image = image
        self.image_name = image_name
        self.image_type = image_type

    def __repr__(self):
        return f"Event('{self.id}', '{self.title}', '{self.text}, '{self.date}', '{self.image}', '{self.image_name}'," \
               f"'{self.image_type}')"


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(100))
    password = db.Column("password", db.String(30))
    events = db.relationship("Event", backref="user", lazy=True)
    friends = db.relationship("Friend", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    # Trying to figure out a way to save all Event id values into a string that will
    # be recognized by the database
    # RSVP_events =
    def __init__(self, name, pwd):
        self.username = name
        self.password = pwd

    def __repr__(self):
        return f"User('{self.id}', '{self.username}, '{self.password}')"


# an attempt to create friends list
class Friend(db.Model):
    id = db.Column("friend_id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))
    friendUsername = db.Column("username", db.String(100))

    def __init__(self, user_id, friendUsername):
        self.user_id = user_id
        self.friendUsername = friendUsername

    def __repr__(self):
        return f"User('{self.id}', '{self.user_id}', '{self.friend_username}')"


class RSVP(db.Model):
    id = db.Column("RSVP_id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('user.id'))
    user_username = db.Column("username", db.String(100), db.ForeignKey('user.username'))
    event_id = db.Column("event_id", db.Integer, db.ForeignKey('event.id'))

    def __init__(self, user_id, user_username, event_id):
        self.user_id = user_id
        self.event_id = event_id
        self.user_username = user_username

    def __repr__(self):
        return f"RSVP('{self.id}', '{self.user_id}', '{self.event_id}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, event_id, user_id):
        self.date_posted = date.today()
        self.content = content
        self.event_id = event_id
        self.user_id = user_id
