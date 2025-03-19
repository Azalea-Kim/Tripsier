import base64
import os
import random
import string

from flask import *
from config import Config
from models import *
from exts import db, mail
from flask_migrate import Migrate
import flask_mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user
from User import User
from forms import *

app = Flask(__name__)  # create a flask app
app.config.from_object(Config)  # load config

db.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login.html'

@app.route('/user', methods=["POST", "GET"])
def login_register():
    if request.method == "GET":
        return render_template("login_chat.html")
    else:
        action = request.form.get("action")
        if action == "LOGIN":
            return
        elif action == "REGISTER":
            return
        elif action == "FORGET_PASSWORD":
            return


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
    email = register_form.get("email")
    password = register_form.get("password")
    captcha = register_form.get("captcha")
    cookie = request.cookies.get("captcha")
    if cookie:
        if check_password_hash(cookie, captcha):
            new_user = UserModel(username=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 400})


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    emsg = None
    if form.validate():
        print(1)
        email = form.email.data
        password = form.password.data
        user_info = load_user(email)
        if not user_info:
            emsg = "Wrong Username or Password"
        else:
            if user_info.verify_password(password):
                login_user(user_info)
                return "OK"
            else:
                emsg = "Wrong Username or Password"
    return render_template('login_chat.html', form=form, emsg=emsg)


@loginManager.user_loader
def load_user(email):
    return User.get(email)

if __name__ == '__main__':
    # open("images/Thailand_flag.png")
    # print(os.path.exists("silicon_squad.db"))
    if not os.path.exists("../silicon_squad.db"):
        # print(12342134123412343)
        os.system("sh initDatabase.sh")
    app.run(debug=True, port=6060)
