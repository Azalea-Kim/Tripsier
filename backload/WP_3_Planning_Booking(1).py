import base64
import time
from datetime import datetime
import datetime
from flask import *
import logging
from flask_login import current_user, user_logged_in

from models import *
from tools import date_calculator
import sys

wp_3 = Blueprint("WP3_Blue", __name__, url_prefix='/')


@wp_3.route("/plan")
def plan_drop_page():
    if user_logged_in:
        carts, carts_total, carts_num = get_cart()
        logger = logging.getLogger('flask.app')
        logger.info('loging')
        logger.warning('plan log')
    return render_template("drag_drop.html", carts=carts, carts_total=carts_total, carts_num=len(carts))


@wp_3.route("/earth")
def show_3d_earth():
    return render_template("3dearth.html")


@wp_3.route("/earth/<code>")
def show_3d_earth_test(code):
    # code "1&2&3&4" city:id=1,id=2,id=3,id=4
    ids = code.split("&")
    cities = []
    for id in ids:
        if (id != ''):
            id = int(id)
            destination = db.session.query(Destination).filter(Destination.id == id).one()
            locations = destination.coord.split(",")
            cities.append([destination, locations[0], locations[1]])

    return render_template("3dearth.html", cities=cities, length=len(cities))


@wp_3.route('/planning', methods=["POST", "GET"])
def planning():
    if request.method == "GET":
        return "Type the time your plan may cost"
    else:
        daily_plan = {
            "destination": "",
            "attraction": "",
            "accommodation": ""
        }
        time = int(request.args.get("time"))
        page = request.args.get("page")
        destination = request.args.get("destination")
        attractions = request.args.get("attractions")
        accommodation = request.args.get("accommodation")

        plan = session.get("plan")
        if not plan:
            plan = {}
            timer = 0
            while timer < time:
                plan["day" + str(timer)] = daily_plan.copy()
                timer += 1
        if destination:
            plan["day" + str(page)]["destination"] = destination
            destination = Destination.query.filter_by(name=destination).first()
            if attractions:
                plan["day" + str(page)]["attraction"] = attractions
                if accommodation:
                    plan["day" + str(page)]["accommodation"] = accommodation
                    session['plan'] = plan
                    return plan
                else:
                    accommodations = Accommodation.query.filter_by(destination_id=destination.id).all()
                    all_accommodation = []
                    for a in accommodations:
                        all_accommodation.append({
                            "name": a.name,
                            "info": a.info
                        })
                    session['plan'] = plan
                    return [plan, all_accommodation]
            else:
                attractions = Attraction.query.filter_by(destination_id=destination.id).all()
                all_attraction = []
                for a in attractions:
                    all_attraction.append({
                        "name": a.name,
                        "info": a.info
                    })
                session['plan'] = plan
                return [plan, all_attraction]
        else:
            destinations = Destination.query.all()
            all_destination = []
            for a in destinations:
                all_destination.append({
                    "name": a.name,
                    "info": a.info
                })
            session['plan'] = plan
            return [plan, all_destination]

g = ["hi"]
@wp_3.route("/a", methods=["POST", "GET"])
def a():
    return render_template("a.html", pp = g)

@wp_3.route("/tabs", methods=["POST", "GET"])
def tabs():
    "2023/3/12,2023/3/15||acc1,attr2||acc1,attr3,attr4||acc2,attr5,attr6,attr7"
    text = request.form.get("text")
    text = text.replace("-", "/")
    print("Text: ", text)
    '2023/05/13,2023/05/14||attr3,||attr7,||'
    g.append(text)
    text_split = text.split("||")
    date_part = text_split[0]
    date_list = date_calculator(date_part.split(",")[0], date_part.split(",")[1])
    g.append(date_list)

    #
    # pln = Planning(user_id=current_user.id, encoded_content=date_list)
    # db.session.add(pln)
    # db.session.commit()

    dates = []
    # nowTime = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S")

    nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
    print(type(nowTime))
    print(nowTime)
    g.append("now")
    print(date_list)
    for i in range(1, len(text_split)-1):
        g.append("hi")
        package_content = text_split[i].split(",")
        if ("" in package_content):
            package_content.remove("")
        # ["acc1","attr2"]
        print("i")
        print(i)
        date = datetime.strptime(date_list[i - 1], '%Y-%m-%d')
        dates.append(date)
        order = 0
        for obj in package_content:
            g.append("in")
            if ("attr" in obj):
                attraction_reservation = Reservation_Attraction(user_id=current_user.id, date=date,
                                                                attraction_id=int(obj[-1]), order=order,
                                                                book_date=nowTime)
                db.session.add(attraction_reservation)
                db.session.commit()

                res = Reservations(user_id=current_user.id, date=date,
                                   a_id=int(obj[-1]), order=order,
                                   book_date=nowTime, type=1)
                db.session.add(res)
                db.session.commit()

                order += 1
            elif ("acc" in obj):
                acc_reservation = Reservation_Accommodation(user_id=current_user.id, date=date,
                                                            accommodation_id=int(obj[-1]), order=order,
                                                            book_date=nowTime)
                db.session.add(acc_reservation)
                db.session.commit()
                res = Reservations(user_id=current_user.id, date=date,
                                   a_id=int(obj[-1]), order=order,
                                   book_date=nowTime, type=0)
                db.session.add(res)
                db.session.commit()
                order += 1
            print("order")
            print(order)

    p = Plan(user_id=current_user.id, start_date=dates[0], end_date=dates[len(dates) - 1], book_date=nowTime)
    db.session.add(p)
    db.session.commit()


    print("Receive:", text)
    g.append("receive")
    return redirect("/")


@wp_3.route("/destInfo", methods=["POST"])
def destInfo():
    command = request.form.get("command")
    if command == "Get destinations":
        destinations = Destination.query.all()
        destination_list = []
        for destination in destinations:
            destination_detail = [
                destination.name,
                destination.avatar,
                destination.info,
                # destination.score,
                destination.id,
                destination.country
            ]
            destination_list.append(destination_detail)
        return jsonify({
            "destinations": destination_list
        })
    elif command == "Get attractions":
        desid = request.form.get("destination")
        print(desid)
        destination = Destination.query.filter_by(id=int(desid)).first()
        # attractions = Attraction.query.filter_by(destination=request.form.get("destination")).all()
        attractions = Attraction.query.filter_by(destination_id=desid).all()
        attraction_list = []
        for attraction in attractions:
            attraction_detail = [
                attraction.name,
                attraction.avatar,
                attraction.info,
                attraction.score,
                attraction.price,
                attraction.id,
                attraction.destination.country
            ]
            attraction_list.append(attraction_detail)
        return jsonify({
            "attractions": attraction_list
        })


def get_cart():
    carts = []
    carts_total = 0
    carts_num = 0
    cart_ac = db.session.query(Cart_Accommodation).filter(Cart_Accommodation.user_id == current_user.id).all()
    cart_at = db.session.query(Cart_Attraction).filter(Cart_Attraction.user_id == current_user.id).all()

    for c in cart_at:
        attraction_obj = db.session.query(Attraction).filter(Attraction.id == c.attraction_id).one()
        carts.append(attraction_obj)
        print(int(attraction_obj.price[0:-1]))
        carts_total += int(attraction_obj.price[0:-1])
        carts_num += 1
    for c in cart_ac:
        accommodation_obj = db.session.query(Accommodation).filter(Accommodation.id == c.accommodation_id).one()
        carts.append(accommodation_obj)
        carts_total += int(accommodation_obj.price[0:-1])
        carts_num += 1

    return carts, carts_total, carts_num


def get_plans():
    t1 = 613
    t2 = 614

    t11 = 51301

    "%Y-%m-%d%H%M%S"
    # p = Plan(user_id=1, start_date=t1, end_date=t2, book_date=t11)
    # db.session.add(p)
    # db.session.commit()

    #
    #
    # #
    # resn = Reservations(user_id =1, a_id = 7, type = 1,date=t1,book_date=t11,order=1)
    # db.session.add(resn)
    # db.session.commit()
    #
    # resn = Reservations(user_id=1, a_id=6, type=0, date=t1, book_date=t11, order=2)
    # db.session.add(resn)
    # db.session.commit()
    #
    # resn = Reservations(user_id=1, a_id=8, type=1, date=t1, book_date=t11, order=3)
    # db.session.add(resn)
    # db.session.commit()
    #
    #
    #
    # resn = Reservations(user_id=1, a_id=5, type=0, date=t1, book_date=t11, order=4)
    # db.session.add(resn)
    # db.session.commit()
    #
    #
    # resn = Reservations(user_id=1, a_id=1, type=1, date=t2, book_date=t11, order=1)
    # db.session.add(resn)
    # db.session.commit()
    # resn = Reservations(user_id=1, a_id=2, type=1, date=t2, book_date=t11, order=2)
    # db.session.add(resn)
    # db.session.commit()
    # resn = Reservations(user_id=1, a_id=3, type=1, date=t2, book_date=t11, order=3)
    # db.session.add(resn)
    # db.session.commit()

    t1 = 712
    t2 = 713
    t3 = 714

    t11 = 51302
    #
    # p = Plan(user_id=1, start_date=t1, end_date=t3, book_date=t11)
    # db.session.add(p)
    # db.session.commit()
    # resn = Reservations(user_id=1, a_id=7, type=1, date=t1, book_date=t11, order=1)
    # db.session.add(resn)
    # db.session.commit()
    # resn = Reservations(user_id=1, a_id=8, type=1, date=t1, book_date=t11, order=2)
    # db.session.add(resn)
    # db.session.commit()
    #
    # resn = Reservations(user_id=1, a_id=1, type=1, date=t2, book_date=t11, order=1)
    # db.session.add(resn)
    # db.session.commit()
    # resn = Reservations(user_id=1, a_id=2, type=1, date=t2, book_date=t11, order=2)
    # db.session.add(resn)
    # db.session.commit()
    #
    # resn = Reservations(user_id=1, a_id=9 ,type=1, date=t3, book_date=t11, order=1)
    # db.session.add(resn)
    # db.session.commit()
    # resn = Reservations(user_id=1, a_id=10, type=1, date=t3, book_date=t11, order=2)
    # db.session.add(resn)
    # db.session.commit()

    plans = {}

    P = db.session.query(Plan).filter_by(user_id=current_user.id).all()

    for i in P:
        plans[i.book_date] = [i.start_date, i.end_date]

    Res = db.session.query(Reservations).order_by(Reservations.book_date.desc()).all()
    # Reservation_Att = db.session.query(Reservation_Attraction).order_by(Reservation_Attraction.book_date.desc()).all()
    rs = []  # filter current user
    print(len(Res))
    for r in Res:
        if r.user_id == current_user.id:
            rs.append(r)

    date = rs[0].book_date
    d = rs[0].date
    current_plan = {}
    current_plan[date] = {}
    current_plan[date][d] = {}

    for i in rs:
        if i.book_date == date:  # 同一个plan
            if i.date == d:  # 同一天

                if i.type == 1:
                    attract_object = db.session.query(Attraction).filter(Attraction.id == i.a_id).one()
                    current_plan[date][d][i.order] = attract_object
                else:
                    acc_object = db.session.query(Accommodation).filter(Accommodation.id == i.a_id).one()
                    current_plan[date][d][i.order] = acc_object

            else:
                sort_cp = dict(sorted(current_plan[date][d].items(), key=lambda x: x[0], reverse=False))
                current_plan[date][d] = sort_cp

                d = i.date  # 新一天第一个
                if i.type == 1:
                    attract_object = db.session.query(Attraction).filter(Attraction.id == i.a_id).one()
                    current_plan[date][d] = {i.order: attract_object}
                else:
                    acc_object = db.session.query(Accommodation).filter(Accommodation.id == i.a_id).one()
                    current_plan[date][d] = {i.order: acc_object}

        else:
            sort_cp = dict(sorted(current_plan[date].items(), key=lambda x: x[0], reverse=False))
            current_plan[date] = sort_cp

            date = i.book_date
            d = i.date
            # sort_cp = dict(sorted(current_plan.items(), key=lambda x: x[0], reverse=False))
            # cp = []
            # for k, v in sort_cp.items():
            #     cp.append(v)
            # plans.append(cp)
            if i.type == 1:
                attract_object = db.session.query(Attraction).filter(Attraction.id == i.a_id).one()
                current_plan[date] = {d: {i.order: attract_object}}
            else:
                acc_object = db.session.query(Accommodation).filter(Accommodation.id == i.a_id).one()
                current_plan[date] = {d: {i.order: acc_object}}

    return current_plan, plans


@wp_3.route("/mytours", methods=["POST", "GET"])
def reservations():
    if user_logged_in:
        carts, carts_total, carts_num = get_cart()
    print("plans")
    current_plan, plans = get_plans()
    return render_template("reservation.html", carts=carts, carts_total=carts_total, carts_num=len(carts),
                           plan=current_plan, p=plans)
