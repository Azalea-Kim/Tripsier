from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.security import check_password_hash

from extension import db
from tools import img_to_blob


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    name = db.Column(db.VARCHAR)
    email = db.Column(db.VARCHAR)
    password = db.Column(db.VARCHAR)
    role = db.Column(db.Integer)
    mark = db.Column(db.Integer)
    avatar = db.Column(db.TEXT,default = img_to_blob("static/temp_photo_test/user_avatar/user_2.jpg"))
    sender1 = db.relationship('Review_Attraction', backref='sender', lazy='dynamic')
    sender2 = db.relationship('Review_Accommodation', backref='sender', lazy='dynamic')
    user1 = db.relationship('Cart_Accommodation', backref='user', lazy='dynamic')
    user2 = db.relationship('Cart_Attraction', backref='user', lazy='dynamic')
    user3 = db.relationship('Reservation_Accommodation',backref='user', lazy='dynamic')
    user4 = db.relationship('Reservation_Attraction',backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User ('{self.name}', '{self.email}')"

    def verify_password(self, password1):
        if self.password is None:
            return False
        return check_password_hash(self.password, password1)




class Destination(db.Model):
    __tablename__ = 'Destinations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR)
    info = db.Column(db.TEXT)
    location = db.Column(db.TEXT)
    country = db.Column(db.TEXT)
    avatar = db.Column(db.TEXT)
    coord = db.Column(db.TEXT)
    map_url = db.Column(db.TEXT)
    hotspot_index = db.Column(db.Integer)
    tags = db.Column(db.TEXT)
    view = db.Column(db.Integer,default = 0)
    des_1 = db.relationship('Attraction',backref = 'destination', lazy = 'dynamic')
    des_2 = db.relationship('Accommodation', backref='destination', lazy='dynamic')
    name_cn = db.Column(db.VARCHAR)
    info_cn = db.Column(db.TEXT)
    location_cn = db.Column(db.TEXT)



class Attraction(db.Model):
    __tablename__ = 'Attractions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR)
    info = db.Column(db.TEXT)
    score = db.Column(db.Integer)
    price = db.Column(db.Integer)
    location = db.Column(db.TEXT)
    tags = db.Column(db.TEXT)
    view = db.Column(db.Integer,default = 0)
    destination_id = db.Column(db.Integer,db.ForeignKey('Destinations.id',ondelete = "CASCADE"))
    avatar = db.Column(db.TEXT)
    des_1 = db.relationship('Cart_Attraction', backref='attraction', lazy='dynamic')
    des_2 = db.relationship('Reservation_Attraction', backref='attraction', lazy='dynamic')
    # attt_1 = db.relationship('Destination',backref = 'attractions')
    name_cn = db.Column(db.VARCHAR)
    info_cn = db.Column(db.TEXT)
    location_cn = db.Column(db.TEXT)

class Accommodation(db.Model):
    __tablename__ = 'Accommodations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR)
    info = db.Column(db.TEXT)
    score = db.Column(db.Integer)
    price = db.Column(db.Integer)
    location = db.Column(db.TEXT)
    tags = db.Column(db.TEXT)
    view = db.Column(db.Integer,default = 0)
    destination_id = db.Column(db.Integer, db.ForeignKey('Destinations.id',ondelete = "CASCADE"))
    avatar = db.Column(db.TEXT)
    des_1 = db.relationship('Cart_Accommodation', backref='accommodation', lazy='dynamic')
    des_2 = db.relationship('Reservation_Accommodation', backref='accommodation', lazy='dynamic')
    # attt_1 = db.relationship('Destination', backref='accommodations')
    name_cn = db.Column(db.VARCHAR)
    info_cn = db.Column(db.TEXT)
    location_cn = db.Column(db.TEXT)

class Reservation_Attraction(db.Model):
    __tablename__ = 'Reservations_Attr'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id',ondelete = "CASCADE"))
    attraction_id = db.Column(db.Integer, db.ForeignKey('Attractions.id',ondelete = "CASCADE"))
    date = db.Column(db.Date)
    note = db.Column(db.TEXT)

class Reservation_Accommodation(db.Model):
    __tablename__ = 'Reservations_Acc'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id',ondelete = "CASCADE"))
    accommodation_id = db.Column(db.Integer, db.ForeignKey('Accommodations.id',ondelete = "CASCADE"))
    date = db.Column(db.Date)
    note = db.Column(db.TEXT)

class Conversation(db.Model):
    __tablename__ = 'Conversations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete ="CASCADE"))
    staff_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete ="CASCADE"))

class Message(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('Conversations.id',ondelete = "CASCADE"))
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.id',ondelete = "CASCADE"))
    receiver_id = db.Column(db.Integer, db.ForeignKey('Users.id',ondelete = "CASCADE"))
    content = db.Column(db.TEXT)

class Review_Attraction(db.Model):
    __tablename__ = 'Review_Attraction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    rate = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.id',ondelete = "CASCADE"))
    attraction_id = db.Column(db.ForeignKey('Attractions.id',ondelete = "CASCADE"))

class Review_Accommodation(db.Model):
    __tablename__ = 'Review_Accommodation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    rate = db.Column(db.Integer)
    sender_id = db.Column(db.Integer, db.ForeignKey('Users.id', ondelete="CASCADE"))
    accommodation_id = db.Column(db.ForeignKey('Accommodations.id',ondelete = "CASCADE"))


class Planning(db.Model):
    __tablename__ = 'Plannings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    encoded_content = db.Column(db.TEXT)
    # content = "[2023/4/5:a10,a12,a13,h5,d5],[2023/4/6:a15,a16,a14,h3,d3],[2023/4/7:a15,a16,a14,h3,d3]"

class Cart_Accommodation(db.Model):
    __tablename__ = 'Cart_Accommodation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    accommodation_id = db.Column(db.ForeignKey('Accommodations.id',ondelete = "CASCADE"))
    date = db.Column(db.TEXT)

class Cart_Attraction(db.Model):
    __tablename__ = 'Cart_Attraction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    attraction_id = db.Column(db.ForeignKey('Attractions.id',ondelete = "CASCADE"))
    date = db.Column(db.TEXT)

class Tag(db.Model):
    __tablename__ = 'Tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)

class Visit(db.Model):
    __tablename__ = 'Visit'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('Users.id'))##用户的id
    Tag = db.Column(db.TEXT)##标签
    Visits = db.Column(db.Integer, default=0)##浏览量
    Recommened_score = db.Column(db.Integer,default=0) ##推荐指数
