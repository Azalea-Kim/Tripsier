from flask import *
from models import *
from main import db,current_user

wp_3_Extra = Blueprint("WP3_E_Blue",__name__)

def get_user_current_destination_set_base_page():
    """
    返回有任何用户预定记录的城市，以便在主页进行展示
    :return: set of destinations
    """
    destination_set = set()
    current_id = current_user.id
    cart_attractions = db.session.query(Cart_Attraction).filter(Cart_Attraction.user_id == current_id)
    cart_accommodations = db.session.query(Cart_Accommodation).filter(Cart_Accommodation.user_id == current_id)

    for cart in cart_attractions:
        destination_set.add(cart.attraction.destination)

    for cart in cart_accommodations:
        destination_set.add(cart.destination.destination)

    return destination_set

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
