from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


names = {
    "bruce": {"age": 20, "gender": "male"},
    "thomas": {"age": 40, "gender": "male"}
}

class Names(Resource):  # Resource gives multiple acess to HTTP methods just by defining methods on ur resource
    def get(self, main):   # name has inserted in here because of <string:name>. let the user enter a string.
    # age -> <int:test>
        return names[main]
    
api.add_resource(Names, "/names/<string:main>")

if __name__ == "__main__":
    app.run(debug=True)