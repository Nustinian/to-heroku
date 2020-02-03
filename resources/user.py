import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="'username' field cannot be left blank")
    parser.add_argument('password', required=True, help="'password' field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 201
        else:
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        msg = ""
        query = "SELECT * FROM users"
        for row in cursor.execute(query):
            msg += str(row)
        connection.close()
        return {"message": f"{msg}"}, 200