import time

from flask import *
from models import *
from main import db
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

wp_2_review = Blueprint("WP2_Review_Blue",__name__)

@login_required
@wp_2_review.route("/reviewReceiveAttraction",methods = ['POST'])
def reviewReceiveAttraction():
    print(request.form)
    sender_id = request.form.get('sender_id')
    content = request.form.get('content')
    rate = request.form.get('rate')
    attraction_id = request.form.get('attraction_id')
    review_new = Review_Attraction(content = content,attraction_id = attraction_id,rate = rate, sender_id = sender_id)
    db.session.add(review_new)
    db.session.commit()
    sender = db.session.query(User).filter(User.id == sender_id).one()

    data_dict = {"sender_name":sender.name,"sender_avatar":sender.avatar,"content":content,"rate":rate}
    return jsonify(data_dict)

@login_required
@wp_2_review.route("/reviewReceiveAccommodation",methods = ['POST'])
def reviewReceiveAccommodation():
    sender_id = request.form.get('sender_id')
    content = request.form.get('content')
    rate = request.form.get('rate')
    accommodation_id = request.form.get('accommodation_id')
    review_new = Review_Attraction(content = content,accommodation_id = accommodation_id,rate = rate, sender_id = sender_id)
    db.session.add(review_new)
    db.session.commit()
    sender_name = db.session.query(User.name).filter(User.id == sender_id).one()
    data_dict = {"sender": sender_name, "content": content}
    return jsonify(data_dict)
