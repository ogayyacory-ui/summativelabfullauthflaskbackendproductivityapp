from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models.user import User

class RegisterResource(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {"error": "Username, email, and password are required"}, 400

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {"error": "Username or email already registered"}, 409

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return user.to_dict(), 



class LoginResource(Resource):
    def post(self):
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200

class MeResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user.to_dict(), 200
