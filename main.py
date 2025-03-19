import random
import string

import flask_mail
import flask_socketio
from flask import *
from flask_babel import Babel, refresh
from flask_sqlalchemy import *

import tools
from extension import db, mail,language
from config import Config
from forms import LoginForm
from models import *
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from WP_6_EXTRA_Recommened import *

from werkzeug.security import generate_password_hash, check_password_hash
from tools import img_to_blob
from PIL import Image

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
loginManager.login_message_category = "info"

socket_io = SocketIO()
socket_io.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'
users = []

babel = Babel(app)


@babel.localeselector
def get_locale():
    cookie = request.cookies.get('locale')
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
    return {'user': current_user, 'message': 'Welcome to my site!', 'is_logged': current_user.is_authenticated,'language':app.config['LANGUAGE']}

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
    print(message)
    emit('my_response',
         {'data': message['data'], 'count': 1})


@socket_io.on('private_message', namespace=name_space)
def private_message(message):
    print(message)
    data = message['data']
    # room = message['room']
    # send the message except my self
    # user_name  = session['username']
    socket_io.emit('private_message', {'data': data, 'user': current_user.name}, namespace=name_space, include_self=False)


@app.route('/a')
def index():
    return render_template("chat_room.html")


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
    # if request.method == 'POST':
    #     username = request.form['username']
    #     users.append(username)
    #     print(username,"Username")
    #     join_room(room = username,sid = username,namespace = name_space)#加入自己的房间
    #     emit('user_connected', {'username': username, 'users': users}, broadcast=True)
    #     return redirect("/")
    return render_template("login_chat.html")

# @app.route('/chat', methods=['POST', 'GET'])
# def chat_room():
#     join_room(room = current_user.name,sid = request.namespace.socket.sid,namespace = name_space)#加入自己的房间
#     emit('user_connected', {'username': current_user.name, 'users': users}, broadcast=True)
#     return render_template("chat_room.html")


@app.route('/specific_test', methods=['POST', 'GET'])
def specific_test():
    return render_template("specificDestination.html")

@app.route('/', methods=['POST', 'GET'])
def index_test():
    bej = db.session.query(Destination).filter(Destination.id == 1).one()
    chq = db.session.query(Destination).filter(Destination.id == 3).one()
    shn = db.session.query(Destination).filter(Destination.id == 2).one()
    rec_list = [bej, chq, shn]
    if(current_user.is_authenticated):
        accommodations, attractions = recommend()
    else:
        accommodations = []
        attractions = []
    return render_template("index-03-new.html",rec_list = rec_list,rec_list_accommodation = accommodations[:3],rec_list_attraction = attractions[:3])


@app.route('/sendCaptcha', methods=["POST"])
def sendCaptcha():
    letters = string.ascii_letters + string.digits  # get the letters and digits
    captcha = "".join(random.sample(letters, 6))  # get the captcha

    email = request.form.get("email")  # get the email address
    print(captcha)
    if email:  # if the email address is not empty
        # send the email
        message = flask_mail.Message(
            subject="[Room of Requirement] Registration Verification",
            recipients=[email],
            body=f"[Web Shopping]: Your captcha code is {captcha}, please complete the verification within 10 "
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
    role = register_form.get("role")
    role = int(role)
    email = register_form.get("email")
    password = register_form.get("password")
    captcha = register_form.get("captcha")
    cookie = request.cookies.get("captcha")
    if cookie:
        if check_password_hash(cookie, captcha):
            new_user = User(name=username, email=email, password=generate_password_hash(password),role = role)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        else:
            return redirect("/")


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
                    if(user_info.role == 0):
                        return redirect("/")
                    elif (user_info.role == 1):
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
    if (current_user.role==1):
        staff_out(current_user.id)

    logout_user()

    return redirect("/")

@app.route('/recommend')
@login_required
def recommend_page():
    recommend()
    return "1"

if __name__ == "__main__":
    from WP_Tool_InserSQL import *
    from WP_Tool_InserSQL_NEW import *
    from dispatch import init_load_table, staff_logged, staff_out, get_suitable_staff_id

    with app.app_context():
        # creat a db setting with models.
        db.drop_all()
        db.create_all()
        insert_test_destinations()
        insert_test_attractions()
        insert_test_accommodations()
        insert_user()
        insert_reviews()
        init_load_table()
        insert_reservations()
        insert_test_accommodations_ch1_ch2()
        insert_test_attractions_ch1_ch2()
        # # translate_database()
        pass

    from WP_2_2_Information_Providing import wp_2
    from WP_2_1_Review_Sending import wp_2_review
    from WP_4_Information_Managing import wp_4
    from WP_3_Planning_Booking import wp_3
    from WP_5_Reservation_Managing import wp_5


    app.register_blueprint(wp_2_review)
    app.register_blueprint(wp_2)
    app.register_blueprint(wp_4)
    app.register_blueprint(wp_3)
    app.register_blueprint(wp_5)
    socket_io.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
