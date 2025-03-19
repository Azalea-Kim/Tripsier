from exts import db
import json


class UserModel(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR, unique=True)
    email = db.Column(db.TEXT, unique=True)
    password = db.Column(db.VARCHAR, default=1)
    role = db.Column(db.Integer)
    mark = db.Column(db.Integer)


class Destination(db.Model):
    __tablename__ = 'Destinations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR)
    image = db.Column(db.BLOB)
    info = db.Column(db.TEXT)
    score = db.Column(db.Float)
    price = db.Column(db.Integer)
    country = db.Column(db.BLOB)


class Attraction(db.Model):
    __tablename__ = 'Attractions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR)
    info = db.Column(db.TEXT)
    destination_id = db.Column(db.Integer, db.ForeignKey('Destinations.id'))


class Accommodation(db.Model):
    __tablename__ = 'Accommodations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR)
    info = db.Column(db.TEXT)
    destination_id = db.Column(db.Integer, db.ForeignKey('Destinations.id'))


class Reservation(db.Model):
    __tablename__ = 'Reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    accommodation_id = db.Column(db.Integer, db.ForeignKey('Accommodations.id'))
    attraction_id = db.Column(db.Integer, db.ForeignKey('Attractions.id'))
    date = db.Column(db.DATE)
    note = db.Column(db.TEXT)


class Conversation(db.Model):
    __tablename__ = 'Conversations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_a_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    participant_b_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


class Message(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('Conversations.id', ondelete="CASCADE"))
    content = db.Column(db.TEXT)

