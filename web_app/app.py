
import os
from dotenv import load_dotenv

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from web_app.models import db, User, Tweet, migrate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

def create_app():
    app = Flask(__name__)
    app.config["CUSTOM_VAR"] = 5 # just an example of app config :-D
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_app_200.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    #
    # ROUTING
    #

    @app.route("/")
    def index():
        #return "Hello World!"
        return render_template("homepage.html")

    @app.route("/about")
    def about():
        return "About Me"

    @app.route("/users")
    @app.route("/users.json")
    def users():
        #users = [
        #    {"id":1, "name": "First User"},
        #    {"id":2, "name": "Second User"},
        #    {"id":3, "name": "Third User"},
        #]
        #return jsonify(users)

        users = User.query.all() # returns a list of <class 'alchemy.User'>
        print(type(users))
        print(type(users[0]))
        #print(len(users))

        users_response = []
        for u in users:
            user_dict = u.__dict__
            del user_dict["_sa_instance_state"]
            users_response.append(user_dict)

        return jsonify(users_response)



    @app.route("/users/create", methods=["POST"])
    def create_user():
        print("CREATING A NEW USER...")
        print("FORM DATA:", dict(request.form))
        # todo: create a new user
        #return jsonify({"message": "CREATED OK (TODO)"})
        if "name" in request.form:
            name = request.form["name"]
            print(name)
            db.session.add(User(name=name))
            db.session.commit()
            return jsonify({"message": "CREATED OK", "name": name})
        else:
            return jsonify({"message": "OOPS PLEASE SPECIFY A NAME!"})




    # GET /hello
    # GET /hello?name=Polly
    @app.route("/hello")
    def hello(name=None):
        print("VISITING THE HELLO PAGE")
        print("REQUEST PARAMS:", dict(request.args))

        if "name" in request.args:
            name = request.args["name"]
            message = f"Hello, {name}"
        else:
            message = "Hello World"

        #return message
        return render_template("hello.html", message=message)

    return app
