from flask import Request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models.user import User

# Resource for user registration
class RegisterResource(Resource):
    def post(self):
        data = Request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
# Check if the username, password, and email are provided
        if not username or not password or not email:
            return {'message': 'Username, email, and password are required'}, 400
# Check if the username or email already exists in the database
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

# jwt_token = create_access_token(identity=new_user.id)
        access_token = create_access_token(identity=new_user.id)
        return {'message': 'User registered successfully',
                 'access_token': access_token,
                    'user': new_user.to_dict()
                 }, 201



class LoginResource(Resource):
    def post(self):
        data = request.get_json() or {}
        username_or_email = data.get('username') or data.get('email')
        password = data.get('password')

        if not username_or_email or not password:
            return {"error": "Credentials and password required"}, 400

        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()

        if not user or not user.check_password(password):
            return {"error": "Invalid username or password"}, 401

        access_token = create_access_token(identity=str(user.id))
        return {
            "access_token": access_token,
            "user": user.to_dict()
        }, 200


class MeResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200