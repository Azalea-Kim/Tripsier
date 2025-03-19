import string

import flask_mail
from flask import *
from flask_babel import Babel
from flask_babel import refresh
from flask_login import *
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room, leave_room

from WP_2_1_Review_Sending import wp_2_review
from WP_2_2_Information_Providing import wp_2
from WP_3_Planning_Booking import wp_3
from WP_4_Information_Managing import wp_4
from WP_5_Reservation_Managing import wp_5
from WP_6_EXTRA_Recommened import *
from WP_Tool_InserSQL_NEW import *
from config import Config
from dispatch import staff_logged, staff_out
from extension import mail
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)

app.register_blueprint(wp_2_review)
app.register_blueprint(wp_2)
app.register_blueprint(wp_4)
app.register_blueprint(wp_3)
app.register_blueprint(wp_5)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
loginManager.login_message_category = "info"

socket_io = SocketIO()
socket_io.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'
users = []

babel = Babel(app)
checkCaptcha = ""


@babel.localeselector
def get_locale():
    cookie = request.cookies.get('locale')
    print("Cookie:", cookie)
    if cookie in ['zh_CN', 'en']:
        if cookie == 'zh_CN':
            app.config['LANGUAGE'] = 'CHI'
        else:
            app.config['LANGUAGE'] = 'ENG'
        return cookie
    if request.accept_languages.best_match(['zh', 'en']) == 'zh':
        app.config['LANGUAGE'] = 'CHI'
    else:
        app.config['LANGUAGE'] = 'ENG'
    return request.accept_languages.best_match(['zh', 'en'])


@app.context_processor
def inject_global_vars():
    return {'user': current_user, 'message': 'Welcome to my site!', 'is_logged': current_user.is_authenticated,
            'language': app.config['LANGUAGE']}


@app.route('/switch_language')
def language_switched():
    resp = make_response(redirect("/"))
    if app.config['LANGUAGE'] == 'ENG':
        app.config['LANGUAGE'] = 'CHI'
        refresh()
        resp.set_cookie('locale', 'zn_CN')
    elif app.config['LANGUAGE'] == 'CHI':
        app.config['LANGUAGE'] = 'ENG'
        refresh()
        resp.set_cookie('locale', 'en')
    return resp

@app.route('/switch_language/admin')
def language_switched_admin():
    resp = make_response(redirect("/admin"))
    if app.config['LANGUAGE'] == 'ENG':
        app.config['LANGUAGE'] = 'CHI'
        refresh()
        resp.set_cookie('locale', 'zn_CN')
    elif app.config['LANGUAGE'] == 'CHI':
        app.config['LANGUAGE'] = 'ENG'
        refresh()
        resp.set_cookie('locale', 'en')
    return resp


@app.route('/push')
def push_once():
    event_name = 'dcenter'
    broadcasted_data = {'data': "test messages", 'user': "Tenrin"}
    socket_io.emit(event_name, broadcasted_data, namespace=name_space)
    return 'done'


@socket_io.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')


@socket_io.on('disconnect')
def disconnect():
    if 'username' in session:
        username = session['username']
        users.remove(username)
        leave_room(username)
        emit('user_disconnected', {'username': username, 'users': users}, broadcast=True)


@socket_io.on('my_event', namespace=name_space)
def mtest_message(message):
    emit('my_response',
         {'data': message['data'], 'count': 1})


@socket_io.on('private_message', namespace=name_space)
def private_message(message):
    data = message['data']
    socket_io.emit('private_message', {'data': data, 'user': current_user.name}, namespace=name_space,
                   include_self=False)

@login_required
@app.route('/a')
def index():
    if(current_user.role == 0):
        chat_role = "Staff"
    elif(current_user.role == 1):
        chat_role = "Customer"
    return render_template("chat_room.html",chat_role = chat_role)


@socket_io.on('join', namespace=name_space)
def on_join(data):
    print("User join the room")
    print(data)
    username = data['username']
    session['username'] = username
    session.permanent = True
    print(session)
    room = int(data['room'])
    join_room(room)
    socket_io.emit('get_room', {'room': room}, namespace=name_space)


@app.route('/test', methods=['POST', 'GET'])
def login_chat_room():
    return render_template("login_chat.html")


@app.route('/specific_test', methods=['POST', 'GET'])
def specific_test():
    return render_template("specificDestination.html")


@app.route('/', methods=['POST', 'GET'])
def index_test():
    socket_io.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
    cities = db.session.query(Destination).all()
    rec_list = []

    carts = []
    carts_total = 0
    carts_num = 0
    accommodations = []
    attractions = []

    for i in range(0, 3):
        city = cities[random.randint(0, len(cities) - 1)]
        cities.remove(city)
        rec_list.append(city)

    if current_user.is_authenticated:  # 如果用户已经登陆了
        accommodations, attractions = recommend()
        carts, carts_total, carts_num = get_cart()
    else:  # 如果没有登陆的话
        accommodations_query = db.session.query(Accommodation).all()
        attractions_query = db.session.query(Attraction).all()
        for i in range(0, 6):
            acc_add = accommodations_query[random.randint(0, len(accommodations_query) - 1)]
            attr_add = attractions_query[random.randint(0, len(attractions_query) - 1)]
            accommodations_query.remove(acc_add)
            attractions_query.remove(attr_add)
            accommodations.append(acc_add)
            attractions.append(attr_add)

        # cart_ac = db.session.query(Cart_Accommodation).filter(Cart_Accommodation.user_id == current_user.id).all()
        # cart_at = db.session.query(Cart_Attraction).filter(Cart_Attraction.user_id == current_user.id).all()
        #
        #
        # for c in cart_at:
        #     attraction_obj = db.session.query(Attraction).filter(Attraction.id == c.attraction_id).one()
        #     carts.append(attraction_obj)
        #     print(int(attraction_obj.price[0:-1]))
        #     carts_total += int(attraction_obj.price[0:-1])
        #     carts_num +=1
        # for c in cart_ac:
        #     accommodation_obj = db.session.query(Accommodation).filter(Accommodation.id == c.accommodation_id).one()
        #     carts.append(accommodation_obj)
        #     carts_total += int(accommodation_obj.price[0:-1])
        #     carts_num += 1

    return render_template("index-03-new.html", rec_list=rec_list, rec_list_accommodation=accommodations[:6],
                           rec_list_attraction=attractions[:6], carts=carts, carts_total=carts_total,
                           carts_num=len(carts))


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


# @app.route('/delete/<item_name>',methods=["GET","POST"])
# def delete_cart(item_name):
#
#     cart_ac = db.session.query(Cart_Accommodation).filter(Cart_Accommodation.user_id == current_user.id).all()
#     cart_at = db.session.query(Cart_Attraction).filter(Cart_Attraction.user_id == current_user.id).all()
#
#     carts = []
#     for c in cart_at:
#         attraction_obj = db.session.query(Attraction).filter(Attraction.id == c.attraction_id).one()
#         carts.append(attraction_obj)
#     for c in cart_ac:
#         accommodation_obj = db.session.query(Accommodation).filter(Accommodation.id == c.accommodation_id).one()
#         carts.append(accommodation_obj)
#
#     for i in carts:
#         if i.name == item_name:
#             try:
#                 db.session.delete(i)
#                 db.session.commit()
#                 flash('Successfully')
#             except Exception as e:
#                 flash('Not successful')


# return redirect(url_for(index_test))
@app.route('/sendCaptcha', methods=["POST"])
def sendCaptcha():
    letters = string.ascii_letters + string.digits  # get the letters and digits
    captcha = "".join(random.sample(letters, 6))  # get the captcha
    global checkCaptcha
    checkCaptcha = captcha

    email = request.form.get("email")  # get the email address
    print(captcha)
    if email:  # if the email address is not empty
        # send the email
        message = flask_mail.Message(
            subject="[Tripsier] Registration Verification",
            recipients=[email],
            body=f"[WELCOME!]: Your captcha code is {captcha}, please complete the verification within 10 "
                 "minutes "
        )
        mail.send(message)
        resp = make_response(jsonify({"code": 200}))
        resp.set_cookie("captcha", generate_password_hash(captcha), max_age=600)

        return resp
    else:  # if the email address is empty
        return make_response(
            jsonify({"code": 400, "message": "Please enter your email address"}))  # return the error message


@app.route('/register', methods=["POST"])
def register():
    register_form = request.form
    username = register_form.get("username")
    email = register_form.get("email")
    captcha = register_form.get("captcha")
    cookie = request.cookies.get("captcha")
    password = register_form.get("password")
    check = register_form.get("check")
    role = register_form.get("role")
    role = int(role)

    if username and email and captcha and password and check and (role in [0, 1]):
        if not cookie:
            return jsonify({
                "emsg": "You haven't got captcha or your captcha has over due"
            })
        if password != check:
            return jsonify({
                "emsg": "The two passwords are inconsistent!"
            })
        if len(password) < 6:
            return jsonify({
                "emsg": "The should have at least 6 letters/numbers!"
            })
        if not check_password_hash(cookie, captcha):
            return jsonify({
                "emsg": "The captcha is incorrect!"
            })
        new_user = User(name=username, email=email, password=generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()
        print("AKLSDJKLAJDKLASJDLKASJD")
        return render_template("login.html", loginMsg="You have successfully registered. Please login",
                               form=LoginForm(request.form))
    else:
        return jsonify({
            "emsg": "Please complete all information"
        })


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    emsg = None

    if request.method == "POST":
        if form.validate():
            email = form.email.data
            password = form.password.data
            user_info = User.query.filter_by(email=email).first()
            if not user_info:
                emsg = "Wrong Username or Password"
            else:
                if user_info.verify_password(password):
                    login_user(user_info, remember=True)
                    if user_info.role == 0:
                        return redirect("/")
                    elif user_info.role == 1:
                        staff_logged(current_user.id)
                        return redirect("/admin")
                else:
                    emsg = "Wrong Username or Password"

    return render_template('login.html', form=form, emsg=emsg)


@loginManager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(int(user_id))


@app.route("/test111", methods=["POST", "GET"])
def test111():
    return render_template("else/1.html")


@app.route('/logout')
@login_required
def logout():
    if current_user.role == 1:
        staff_out(current_user.id)

    logout_user()

    return redirect("/")


@app.route('/recommend')
@login_required
def recommend_page():
    recommend()
    return "1"


@app.route("/aboutus", methods=["POST", "GET"])
def aboutus():
    if user_logged_in:
        carts, carts_total, carts_num = get_cart()
    return render_template("about-us.html")


@app.route("/attractions", methods=["POST", "GET"])
def attractions():
    if user_logged_in:
        carts, carts_total, carts_num = get_cart()

    attr_list = db.session.query(Attraction).all()
    dict = {}
    for a in attr_list:
        destination_object = db.session.query(Destination).filter(Destination.id == a.destination_id).one()
        dict[a] = destination_object
    return render_template("all_attractions.html", attr_list=attr_list, dict=dict, carts=carts, carts_total=carts_total,
                           carts_num=len(carts))


@app.route("/accommodations", methods=["POST", "GET"])
def accommodations():
    if user_logged_in:
        carts, carts_total, carts_num = get_cart()
    acco_list = db.session.query(Accommodation).all()
    dict = {}
    for a in acco_list:
        destination_object = db.session.query(Destination).filter(Destination.id == a.destination_id).one()
        dict[a] = destination_object
    return render_template("all_acco.html", attr_list=acco_list, dict=dict, carts=carts, carts_total=carts_total,
                           carts_num=len(carts))


if __name__ == "__main__":
    app.run()
