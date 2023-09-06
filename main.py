from flask import Flask, request
from pymongo import MongoClient
from faker import Faker
from pymongo.server_api import ServerApi
from bson import json_util
import json

app = Flask(__name__)
fake = Faker()
username = "ahbar1234"
password = "BrCNr7bAJqpOmTDR"
uri = f"mongodb+srv://{username}:{password}@cluster0.q9uushk.mongodb.net/?retryWrites=true&w=majority"
mongo = MongoClient(uri, server_api=ServerApi('1'))    
# get user collection
User = mongo["Flask"]["User"]

user_attributes = ["id", "name", "email", "password"]


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        all_users = User.find()
        return [json.loads(json_util.dumps(user)) for user in all_users]

    elif request.method == "POST":
        user = {}
        for attr in user_attributes:
            user[attr] = request.form.get(attr, None)
        User.insert_one(user)
        return {"message": "success"}
    # else 
    return {"message": "error: only GET and POST methods available on this url"}

@app.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def user(id):
    if request.method == "GET":
        user= User.find_one({"id": id})
        if user is None:
            return {"message": "not found"}
        return json.loads(json_util.dumps(user))

    elif request.method == "PUT":
        new_attr = User.find_one({"id": id})
        if new_attr is None:
            return {"message": "not found"}
        for attr in user_attributes:
            if attr in request.form:
                new_attr[attr] = request.form[attr]
        result = User.update_one({"id": id}, {'$set': new_attr})
        if result.modified_count == 1:
            return {"message": "success"}
        return {"message": "failed to update record with given data"}
    
    elif request.method == "DELETE":
        result = User.delete_one({"id": id})
        if result.deleted_count == 1:
            return {"message": "success"}
        return {"message": "failed to delete record with given data"}

    return {"message": "error: only GET, PUT and DELETE methods available on this url"}

if __name__ == '__main__':
    while True:
        try: 
            mongo.admin.command("ping")
            print("Connected to mongodb")
            break
        except Exception as e:
            print(e)

    if User.estimated_document_count() == 0:
        # insert 100 fake records
        User.insert_many([
                    {
                        "id": fake.unique.ssn(), 
                        "name": fake.name(), 
                        "email": fake.email(), 
                        "password": fake.password()
                    } for _ in range(100)])

    app.run(debug=True) 
    
