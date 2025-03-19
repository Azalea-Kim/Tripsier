from flask import *
from models import *
from app import db,current_user
from flask_login import login_required

wp_3_Extra = Blueprint("WP3_E_Blue",__name__)



@login_required
@wp_3_Extra.route("/addChart/accommodation/<id>")
def add_accommodation_cart(id):
    """
    添加一个accommodation到cart中，此链接必须被隐藏，除非用户已经登录
    :param id: accommodation_id
    :return: redirect
    """
    new_cart_record = Cart_Accommodation(user_id = current_user.id,accommodation_id = id)
    db.session.add(new_cart_record)
    db.session.commit()
    return redirect("/detail/accommodation/"+id)

@login_required
@wp_3_Extra.route("/addChart/attraction/<id>")
def add_attraction_cart(id):
    """
    添加一个attraction到cart中，此链接必须被隐藏，除非用户已经登录
    :param id: attraction
    :return: redirect
    """
    new_cart_record = Cart_Attraction(user_id = current_user.id,attraction_id = id)
    db.session.add(new_cart_record)
    db.session.commit()
    redirect("/detail/attraction/"+id)
