from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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

parser_update_args = reqparse.RequestParser()
parser_update_args.add_argument("name", type=str, help="name of the user is required")
parser_update_args.add_argument("age", type=int, help="age of the user is required")
parser_update_args.add_argument("gender", type=str, help="gender of the user is required")


# fields provides an easy way to control what data you actually render in the response as input payload. this module helps to use any objects want in the Resource
resource_fields = {
    "_id": fields.Integer, 
    "name": fields.String, 
    "age": fields.Integer, 
    "gender": fields.String, 
}


class Main(Resource):
    @marshal_with(resource_fields)
    def get(self, main):
        result = DbModel.query.filter_by(_id=main).first()
        if not result:
            abort(404, message="Couldn't find this ID on the database")
        return result
            
    @marshal_with(resource_fields)
    def put(self, main):
        args = parser.parse_args()
        result = DbModel.query.filter_by(_id=main).first()
        if result:
            abort(409, message='Already Assigned!')
        
        model = DbModel(
            _id=main, name=args['name'],
            age=args['age'],
            gender=args['gender']
        )
        db.session.add(model)
        db.session.commit()
        return model, 201
    
    @marshal_with(resource_fields)
    def patch(self, main):    # patch is a HTTP method for update
        args = parser_update_args.parse_args()
        result = DbModel.query.filter_by(_id=main).first()
        if not result:
            abort(404, message="Doesn't exist, Cannot Update")
        
        if args['name']:
            result.name = args['name']
        if args['age']:
            result.age = args['age']
        if args['gender']:
            result.gender = args['gender']
            
        db.session.commit()
        return result
            
api.add_resource(Main, "/main/<int:main>")



if __name__ == "__main__":
    app.run(debug=True, port=5000)    


# Flask-RESTful’s request parsing interface, reqparse, is modeled after the argparse interface. It’s designed to provide simple and uniform access to any variable on the flask.request object in Flask.

# request.method -> request gives us info that we sent

# request.form : the key/value pairs in the body, from a HTML post form, or JavaScript request that isn't JSON encoded. request. files : the files in the body, which Flask keeps separate from form