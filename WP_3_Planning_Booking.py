import base64
from datetime import datetime

from flask import *
import models
from main import db,current_user
from models import *
from tools import date_calculator

wp_3 = Blueprint("WP3_Blue",__name__)

@wp_3.route("/plan")
def plan_drop_page():
    return render_template("drag_drop.html")

@wp_3.route("/earth")
def show_3d_earth():
    return render_template("3dearth.html")

@wp_3.route("/earth/<code>")
def show_3d_earth_test(code):
    #code "1&2&3&4" city:id=1,id=2,id=3,id=4
    ids = code.split("&")
    cities = []
    for id in ids:
        id = int(id)
        destination = db.session.query(Destination).filter(Destination.id == id).one()
        locations = destination.coord.split(",")
        cities.append([destination,locations[0],locations[1]])

    return render_template("3dearth.html",cities = cities,length = len(cities))

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


@wp_3.route("/tabs", methods=["POST", "GET"])
def tabs():
    "2023/3/12,2023/3/15||acc1,attr2||acc1,attr3,attr4||acc2,attr5,attr6,attr7"
    text = request.form.get("text")
    text = text.replace("-","/")
    print("Text: ",text)
    text_split = text.split("||")
    date_part = text_split[0]
    date_list = date_calculator(date_part.split(",")[0],date_part.split(",")[1])
    print(date_list)

    for i in range(1,len(text_split)):
        package_content = text_split[i].split(",")
        if("" in package_content):
            package_content.remove("")
        # ["acc1","attr2"]
        date = datetime.strptime(date_list[i-1], '%Y-%m-%d')
        for obj in package_content:
            if("attr" in obj):
                attraction_reservation = Reservation_Attraction(user_id=current_user.id, date=date,
                                                                attraction_id=int(obj[-1]))
                db.session.add(attraction_reservation)
            elif("acc" in obj):
                acc_reservation = Reservation_Accommodation(user_id = current_user.id,date = date,accommodation_id = int(obj[-1]))
                db.session.add(acc_reservation)
        db.session.commit()

    print("Receive:", text)
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
        attractions = Attraction.query.filter_by(destination_id = desid).all()
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
