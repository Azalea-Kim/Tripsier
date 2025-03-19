from flask import *
from models import *
from extension import db
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

wp_4 = Blueprint("WP4_Blue",__name__, url_prefix='/')

@login_required
@wp_4.route("/admin",methods = ['GET',"POST"])
def index_of_admin():
    if current_user.role == 1:
        users = db.session.query(User).limit(10).all()

        visits = db.session.query(Visit).all()
        total_visit = 0
        for visit in visits:
            total_visit += visit.Visits

        total_user = 0
        users = db.session.query(User).all()
        for user in users:
            total_user += 1

        expenses = 0
        carts_attr = db.session.query(Reservation_Attraction).all()
        carts_acc = db.session.query(Reservation_Accommodation).all()

        for cart in carts_attr:
            expenses += int(cart.attraction.price[0:-1])
        for cart in carts_acc:
            expenses += int(cart.accommodation.price[0:-1])

        expenses_per_user = expenses/total_user


        return render_template("index_admin.html",users = users,total_user = total_user,total_visit = total_visit,expenses = expenses,expenses_per_user = expenses_per_user)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/customers",methods = ['GET',"POST"])
def customers_page():
    if current_user.role == 1:
        user_list = db.session.query(User).filter(User.role == 0).all()
        return render_template("information/information-customer.html",user_list = user_list)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/destinations",methods = ['GET',"POST"])
def destinations_page():
    if current_user.role == 1:
        dest_list = db.session.query(Destination).all()
        return render_template("information/information-destination.html",dest_list = dest_list)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/attractions",methods = ['GET',"POST"])
def attractions_page():
    if current_user.role == 1:
        attraction_list = db.session.query(Attraction).all()
        return render_template("information/information-attraction.html",attraction_list = attraction_list)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/accommodations",methods = ['GET',"POST"])
def accommodations_page():
    if current_user.role == 1:
        accommodations_list = db.session.query(Accommodation).all()
        return render_template("information/information-accommodation.html",accommodations_list = accommodations_list)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/destination/detail/<id>")
def detail_destination(id):
    if current_user.role == 1:
        object = db.session.query(Destination).filter(Destination.id == id).one()
        related_accommodations = db.session.query(Accommodation).filter(Accommodation.destination_id == id).all()
        related_attraction = db.session.query(Attraction).filter(Attraction.destination_id == id).all()
        return render_template("information/detail/detail-destination.html",destination = object,accommodations = related_accommodations,
                               attractions = related_attraction)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/customer/detail/<id>")
def detail_customer(id):
    if current_user.role == 1:
        object = db.session.query(User).filter(User.id == id).one()
        return render_template("information/detail/detail-user.html",user_info = object)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/attraction/detail/<id>")
def detail_attraction(id):
    if current_user.role == 1:
        object = db.session.query(Attraction).filter(Attraction.id == id).one()
        return render_template("information/detail/detail-attraction.html",attraction = object)
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/accommodation/detail/<id>")
def detail_accommodation(id):
    if current_user.role == 1:
        object = db.session.query(Accommodation).filter(Accommodation.id == id).one()
        reservations = db.session.query(Reservation_Accommodation).filter(Reservation_Accommodation.accommodation_id == id).all()
        print(reservations,"Resss")
        return render_template("information/detail/detail-accommodation.html",accommodation = object,reservations = reservations)
    return render_template("alert.html")

# Ajax send information to js to show graphs
@login_required
@wp_4.route("/admin/destination/detail/<id>/coord",methods = ['POST'])
def send_detail_coord_dest(id):
    dest = db.session.query(Destination).filter(Destination.id == id).one()
    name = dest.name
    latlang = dest.coord
    print(latlang)
    return jsonify({'name':name,'coord':latlang})

@login_required
@wp_4.route("/admin/supervise",methods = ['POST','GET'])
def show_supervise_page():
    if current_user.role == 1:
        return render_template("information/staff_supervise.html")
    return render_template("alert.html")

@login_required
@wp_4.route("/admin/upload_destination",methods = ['POST','GET'])
def upload_destination():
    if current_user.role == 1:
        if request.method == 'POST':
            print(request.form.get("destination_name"))
            destination = Destination()
        return render_template("information/add_destination.html")
    return render_template("alert.html")