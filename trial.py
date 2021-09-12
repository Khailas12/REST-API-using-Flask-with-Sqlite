from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class DbModel(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f"Main(name={name}, age={age}, gender={gender})"

# reqparse -> it parses arguments from an incoming request and uses them as inputs to invoke the corresponding controller method
parser = reqparse.RequestParser()

parser.add_argument("name", type=str, help="Name of the user is required", required=True)
parser.add_argument("age", type=int, help="Age of the user is required", required=True)
parser.add_argument("gender", type=str, help="Gender the of user is required", required=True)
# required=True -> this will never leave the output as None in the place we didn't assigned anything. despite shows a message to add things 

entry = {}

# to avoid crash if we assign non existing value
def abort_if_value_doesnt_exist(main):
    if main not in entry:
        abort(404, message="Value doesn't exist!")

def abort_if_value_exists(main):
    if main in entry:
        abort(409, message="Value already exists!")


class Main(Resource):
    def get(self, main):
        abort_if_value_doesnt_exist(main)
        return entry[main]
    
    def put(self, main):
        abort_if_value_exists(main)
        args = parser.parse_args()
        entry[main] = args
        return entry[main], 201
    
    def delete(self, main):
        abort_if_value_doesnt_exist(main)
        del entry[main]
        return "", 204  # 204 -> deleted succesfully
    
api.add_resource(Main, "/main/<int:main>")


if __name__ == "__main__":
    app.run(debug=True)    

# Flask-RESTful’s request parsing interface, reqparse, is modeled after the argparse interface. It’s designed to provide simple and uniform access to any variable on the flask.request object in Flask.

# request.method -> request gives us info that we sent

# request.form : the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded. request. files : the files in the body, which Flask keeps separate from form