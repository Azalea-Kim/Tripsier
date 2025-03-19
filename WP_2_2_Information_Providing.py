from flask import *
from models import *
from main import db,current_user
from flask_login import *

wp_2 = Blueprint("WP2_Blue",__name__)

@wp_2.route("/",methods = ['GET','POST'])
def index():
    """
    Show recommended destinations
    :return: A page that could be our index
    """
    dest_list = []
    # 取前6个作为推荐点
    i = 0
    for dest in db.session.query(Destination).all():
        i += 1
        if(i==7):
            break
        dest_list.append(dest)

    bej = db.session.query(Destination).filter(Destination.id == 1).one()
    chq = db.session.query(Destination).filter(Destination.id == 0).one()
    shn = db.session.query(Destination).filter(Destination.id == 2).one()
    rec_list = [bej,chq,shn]

    return render_template('home.html',dest_list = dest_list,rec_list = rec_list)

@wp_2.route("/destinations",methods = ['GET','POST'])
def show_destinations():
    """
    Show destinations in a list
    :return: A page that shows destination information
    """
    dest_list = db.session.query(Destination).all()
    return render_template("destinations.html",dest_list = dest_list)

def show_attractions_relate_destination(destination):
    """
    Show a destination's attractions
    :param destination: destination's name
    :return: a list of attractions
    """
    dest_id = db.session.query(Destination.id).filter(Destination.name == destination).one()
    attractions = db.session.query(Attraction).filter(Attraction.destination_id == dest_id).all()
    return attractions

def show_accommodations_relate_destination(destination):
    """
    Show a destination's accommodations
    :param destination: destination's name
    :return: a list of accommodations
    """
    dest_id = db.session.query(Destination.id).filter(Destination.name == destination).one()
    accommodations = db.session.query(Accommodation).filter(Accommodation.destination_id == dest_id).all()
    return accommodations

@wp_2.route("/detail/destination/<id>",methods = ['GET','POST'])
def destination_chosen(id):
    """
    After user choose the destination, he could see the recommend information of this page.
    :return: template of this page
    """
    destination_object = db.session.query(Destination).filter(Destination.id == id).one()
    attractions = db.session.query(Attraction).filter(Attraction.destination_id == id).all()
    accommodations = db.session.query(Accommodation).filter(Accommodation.destination_id == id).all()
    destination_object.view = destination_object.view + 1
    db.session.add(destination_object)
    db.session.commit()

    return render_template("specificDestination.html",destination = destination_object, attractions = attractions, accommodations = accommodations)


@wp_2.route("/detail/destinationtest111/<id>",methods = ['GET','POST'])
def detail_page_destination(id):
    """
    A detail page of the destination
    :return: template of this page
    This page might be unuseful
    """
    destination_object = db.session.query(Destination).filter(Destination.id == id).one()

    return render_template("detail_destination.html", destination = destination_object)

@wp_2.route("/detail/attraction/<id>",methods = ['GET','POST'])
def detail_page_attraction(id):
    """
    A detail page of the attraction
    :return: template of this page
    Also show reviews in this page
    """
    addVisit_Attraction(id)
    attract_object = db.session.query(Attraction).filter(Attraction.id == id).one()
    reviews = db.session.query(Review_Attraction).filter(Review_Attraction.attraction_id == id).all()
    attract_object.view = attract_object.id + 1
    db.session.add(attract_object)
    db.session.commit()

    return render_template("detail_attraction.html", attraction = attract_object, reviews = reviews)

@login_required
@wp_2.route("/detail/attraction/<id>/review",methods = ['POST'])
def review_attraction(id):
    """
    Send a review to the attraction
    :return: redirect
    """
    rate = request.form.get('rate')
    content = request.form.get('content')
    review_new = Review_Attraction(content = content, rate = rate, attraction_id = id)
    db.session.add(review_new)
    db.session.commit()
    return redirect("/detail/attraction/"+id)


@wp_2.route("/detail/accommodation/<id>",methods = ['GET','POST'])
def detail_page_accommodation(id):
    """
    A detail page of the accommodation
    :return: template of this page
    """
    addVisit_Accommodation(id)
    accommodation_object = db.session.query(Accommodation).filter(Accommodation.id == id).one()
    destination = accommodation_object.destination
    reviews = db.session.query(Review_Accommodation).filter(Review_Accommodation.accommodation_id == id).all()
    accommodation_object.view = accommodation_object.view + 1
    db.session.add(accommodation_object)
    db.session.commit()

    return render_template("detail_accommodation.html", accommodation = accommodation_object,reviews = reviews,destination = destination)

@login_required
@wp_2.route("/detail/accommodation/<id>/review",methods = ['POST'])
def review_accommodation(id):
    """
    Send a review to the accommodation
    :return: redirect
    """
    rate = request.form.get('rate')
    content = request.form.get('content')
    review_new = Review_Accommodation(content = content, rate = rate, accommodation_id = id)
    db.session.add(review_new)
    db.session.commit()
    return redirect("/detail/accommodation/" + id)

@wp_2.route("/search/<key_word>",methods = ['GET','POST'])
def search_page(key_word):
    """
    A page for searching information by key words
    :return: template of this page
    """
    if(key_word == None or key_word == ""):
        d_list = db.session.query(Destination).all()
        attract_list = db.session.query(Attraction).all()
        accommo_list = db.session.query(Accommodation).all()
    else:
        d_list,attract_list,accommo_list = search_for_everything(key_word)

    return render_template("search_page.html", d_list = d_list, attract_list = attract_list, accommo_list = accommo_list, current_keyword = key_word)

@wp_2.route("/add_accommodation/<id>",methods = ['GET','POST'])
def add_to_cart_1(id):
    current_cart = Cart_Accommodation(user_id = current_user.id,accommodation_id = id)
    db.session.add(current_cart)
    db.session.commit("/detail/accommodation/"+id)

@wp_2.route("/add_attraction/<id>", methods=['GET', 'POST'])
def add_to_cart_2(id):
    current_cart = Cart_Attraction(user_id=current_user.id, attraction_id=id)
    db.session.add(current_cart)
    db.session.commit()
    return redirect("/detail/attraction/"+id)

def search_for_everything(search_key_word):
    """
    Use the key word to search accommodation, destination, or attraction
    :param search_key_word: String of the key word
    :return: lists of destinations, attractions and accommodations
    """
    search_key_word = "%" + search_key_word + "%"
    dest_list = db.session.query(Destination).filter(Destination.name.like(search_key_word)).all()
    dest_list_by_country = db.session.query(Destination).filter(Destination.country.like(search_key_word)).all()
    sum_dest_list = dest_list + dest_list_by_country

    attraction_list = db.session.query(Attraction).filter(Attraction.name.like(search_key_word)).all()
    attraction_list_by_location = db.session.query(Attraction).filter(Attraction.location.like(search_key_word)).all()
    attraction_list_by_info =  db.session.query(Attraction).filter(Attraction.info.like(search_key_word)).all()
    attraction_list_by_country = db.session.query(Attraction).join(Destination).filter(Destination.country.like(search_key_word)).all()
    sum_attraction = attraction_list + attraction_list_by_location + attraction_list_by_info + attraction_list_by_country

    accommodation_list = db.session.query(Accommodation).filter(Accommodation.name.like(search_key_word)).all()
    accommodation_list_by_location = db.session.query(Accommodation).filter(Accommodation.location.like(search_key_word)).all()
    accommodation_list_by_info = db.session.query(Accommodation).filter(Accommodation.info.like(search_key_word)).all()
    accommodation_list_by_country = db.session.query(Accommodation).join(Destination).filter(Destination.country.like(search_key_word)).all()
    sum_accommodation = accommodation_list + accommodation_list_by_info + accommodation_list_by_location + accommodation_list_by_country

    return sum_dest_list,sum_attraction,sum_accommodation

def addVisit_Accommodation(qid):
    this_question = db.session.query(Accommodation.tags).filter(Accommodation.id == qid).one()
    this_question = this_question[0]
    try:
        this_tag = db.session.query(Visit).filter(Visit.Tag == this_question,Visit.user_id == current_user.id).one()
        this_tag.Visits = this_tag.Visits+1
        db.session.add(this_tag)
        db.session.commit()
    except Exception as e:
        pass

def addVisit_Attraction(qid):
    this_question = db.session.query(Attraction.tags).filter(Attraction.id == qid).one()
    this_question = this_question[0]
    try:
        this_tag = db.session.query(Visit).filter(Visit.Tag == this_question,Visit.user_id == current_user.id).one()
        this_tag.Visits = this_tag.Visits+1
        db.session.add(this_tag)
        db.session.commit()
    except Exception as e:
        pass


