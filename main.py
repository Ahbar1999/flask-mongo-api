from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from pymongo import MongoClient
from faker import Faker
from pymongo.server_api import ServerApi
from bson import json_util
import json
import os, sys

app = Flask(__name__)
fake = Faker()
username = os.environ.get("USERNAME", None)
password = os.environ.get("PASSWORD", None)
if not username or not password: 
    print("couldnt fetch username or password from env") 
    sys.exit(1) 
 
uri = f"mongodb+srv://{username}:{password}@cluster0.q9uushk.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(uri, server_api=ServerApi('1'))    
# get user collection
db = mongo["Flask"]
Users = db["User"]
api = Api(app)

user_attributes = ["id", "name", "email", "password"]
# add arguments to the parser for validation purposes
parser = reqparse.RequestParser()
for attr in user_attributes:
    parser.add_argument(attr, location='form')

def abort_if_not_found(id):
    return abort(404, message=f"User with id: {id} does not exist")

# retrieve all  records/post a new record
class UserList(Resource):
    def get(self):
        all_users = Users.find()
        if all_users is None:
            abort(404, message="No record exists")
        return [json.loads(json_util.dumps(user)) for user in all_users]

    def post(self):
        args = parser.parse_args()
        new_user = {}
        for attr in user_attributes:
            if args[attr] is None:
                abort(404, message= f"error: value for {attr} missing from submitted data") 
            new_user[attr] = args[attr]
        Users.insert_one(new_user)
        return {"message": "success"}

# retrieve/manipulate singular records
class User(Resource):
    def get(self, id):
        user= Users.find_one({"id": id})
        if user is None:
            abort_if_not_found(id)      
        # serialize/deserialize; bson -> json 
        return json.loads(json_util.dumps(user))
    
    def delete(self, id):
        result = Users.delete_one({"id": id})
        if result.deleted_count == 1:
            return {"message": "success"}
        return abort_if_not_found(id)

    def put(self, id):
        args = parser.parse_args()
       
        new_attr = Users.find_one({"id": id})
        if new_attr is None:
            abort_if_not_found(id) 
        for attr in user_attributes:
            if args[attr] is not None:
                new_attr[attr] = args[attr]
        result = Users.update_one({"id": id}, {'$set': new_attr})
        if result.modified_count == 1:
            return {"message": "success"}
        abort(404, message="failed to update record with given data")

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<id>')
    
if __name__ == '__main__':
    while True:
        try: 
            mongo.admin.command("ping")
            print("Connected to mongodb")
            break
        except Exception as e:
            print(e)

    if Users.estimated_document_count() == 0:
        # insert 100 fake records
        Users.insert_many([
                    {
                        "id": fake.unique.ssn(), 
                        "name": fake.name(), 
                        "email": fake.email(), 
                        "password": fake.password()
                    } for _ in range(100)])
   
    app.run(debug=True) 
    
