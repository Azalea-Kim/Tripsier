
import string
from datetime import datetime

import flask_mail
from flask import *
from models import *
from extension import mail
from main import db
from flask_sqlalchemy import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

wp_5 = Blueprint("WP5_Blue",__name__)

@login_required
@wp_5.route('/cancel_notice_accommodation/<id>', methods=["POST","GET"])
def sendCancelMail_Acc(id):
    if current_user.role == 1:
        reservation = db.session.query(Reservation_Accommodation).filter(Reservation_Accommodation.id == id).one()
        email = reservation.user.email
        place = reservation.accommodation.name
        date = reservation.date
        db.session.delete(reservation)
        db.session.commit()
        if email:  # if the email address is not empty
            # send the email
            message = flask_mail.Message(
                subject="[Room of Requirement] Cancel Notification",
                recipients=[email],
                body=f"[Web Tripsier]: Dear customer, we are sorry to tell you that your trip to {place} on {date} has been canceled due to some reasons"
            )
            mail.send(message)
            return redirect("/admin/edit")
        else:  # if the email address is empty
            return make_response(
                jsonify({"code": 400, "message": "Something wrong with the cancel"}))  # return the error message
    return render_template("alert.html")

@login_required
@wp_5.route('/cancel_notice_attraction/<id>', methods=["POST","GET"])
def sendCancelMail_Attr(id):
    if current_user.role == 1:
        reservation = db.session.query(Reservation_Attraction).filter(Reservation_Attraction.id == id).one()
        email = reservation.user.email
        place = reservation.attraction.name
        date = reservation.date
        db.session.delete(reservation)
        db.session.commit()
        if email:  # if the email address is not empty
            # send the email
            message = flask_mail.Message(
                subject="[Room of Requirement] Cancel Notification",
                recipients=[email],
                body=f"[Web Tripsier]: Dear customer, we are sorry to tell you that your trip to {place} on {date} has been canceled due to some reasons"
            )
            mail.send(message)
            return redirect("/admin/edit")
        else:  # if the email address is empty
            return make_response(
                jsonify({"code": 400, "message": "Something wrong with the cancel"}))  # return the error message
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/plan_supervise', methods=["POST","GET"])
def supervise_page():
    if current_user.role == 1:
        reservation_attr = db.session.query(Reservation_Attraction).all()
        reservation_acc = db.session.query(Reservation_Accommodation).all()
        return render_template("information/staff_supervise.html",reservation_acc = reservation_acc,reservation_attr = reservation_attr)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/edit/attr', methods=["POST","GET"])
def edit_page_attr():
    if current_user.role == 1:
        reservation_attr = db.session.query(Reservation_Attraction).all()
        return render_template("information/staff_cancel_attraction_reservation.html",reservation_attr = reservation_attr)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/edit/acc', methods=["POST","GET"])
def edit_page_acc():
    if current_user.role == 1:
        reservation_acc = db.session.query(Reservation_Accommodation).all()
        return render_template("information/staff_cancel_accommodation_reservation.html", reservation_acc = reservation_acc)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/edit/acc/<start_date>/<end_date>', methods=["POST","GET"])
def edit_page_date_acc(start_date,end_date):
    if current_user.role == 1:
        start_date = start_date.replace("-","/")
        end_date = end_date.replace("-", "/")
        start_date = datetime.strptime(start_date,'%Y/%m/%d')
        end_date = datetime.strptime(end_date, '%Y/%m/%d')
        reservation_acc = db.session.query(Reservation_Accommodation).filter((Reservation_Accommodation.date).between(start_date,end_date)).all()
        return render_template("information/staff_cancel_attraction_reservation.html", reservation_acc = reservation_acc)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/edit/attr/<start_date>/<end_date>', methods=["POST","GET"])
def edit_page_date_attr(start_date,end_date):
    if current_user.role == 1:
        start_date = start_date.replace("-","/")
        end_date = end_date.replace("-", "/")
        start_date = datetime.strptime(start_date,'%Y/%m/%d')
        end_date = datetime.strptime(end_date, '%Y/%m/%d')
        reservation_attr = db.session.query(Reservation_Attraction).filter((Reservation_Attraction.date).between(start_date,end_date)).all()
        return render_template("information/staff_cancel_attraction_reservation.html", reservation_attr = reservation_attr)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/get_destination/attr',methods = ['POST'])
def get_destination_attr():
    if current_user.role == 1:
        res = []
        destination_name = request.form.get('destination')
        destination_object = db.session.query(Destination).filter(Destination.name == destination_name).one()
        attractions = db.session.query(Attraction.name).filter(Attraction.destination_id == destination_object.id).all()
        for name in attractions:
            res.append(name[0])
        print(res)
        return jsonify(res)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/get_destination/acc',methods = ['POST'])
def get_destination_acc():
    if current_user.role == 1:
        res = []
        destination_name = request.form.get('destination')
        destination_object = db.session.query(Destination).filter(Destination.name == destination_name).one()
        accommodations = db.session.query(Accommodation.name).filter(Accommodation.destination_id == destination_object.id).all()
        for name in accommodations:
            res.append(name[0])
        print(res)
        return jsonify(res)
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/edit_reservation_accommodation/<id>',methods = ['POST'])
def edit_reservation_accommodation(id):
    if current_user.role == 1:
        if  request.method == 'POST':
            name = request.form.get('name')
            date = request.form.get('date')
            date = datetime.strptime(date,"%Y-%m-%d")
            reservation = db.session.query(Reservation_Accommodation).filter(Reservation_Accommodation.id == id).one()
            accommodation = db.session.query(Accommodation).filter(Accommodation.name == name).one()
            reservation.date = date
            reservation.accommodation_id = accommodation.id
            db.session.add(reservation)
            db.session.commit()
            return redirect("/admin/edit/")
    return render_template("alert.html")

@login_required
@wp_5.route('/admin/edit_reservation_attraction/<id>',methods = ['POST'])
def edit_reservation_attraction(id):
    if current_user.role == 1:
        if  request.method == 'POST':
            name = request.form.get('name')
            date = request.form.get('date')
            date = datetime.strptime(date,"%Y-%m-%d")
            reservation = db.session.query(Reservation_Attraction).filter(Reservation_Attraction.id == id).one()
            attraction = db.session.query(Attraction).filter(Attraction.name == name).one()
            reservation.date = date
            reservation.attraction = attraction.id
            db.session.add(reservation)
            db.session.commit()
            return redirect("/admin/edit/")
    return render_template("alert.html")
