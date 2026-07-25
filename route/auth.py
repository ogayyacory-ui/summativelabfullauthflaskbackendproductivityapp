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

        return {'message': 'User registered successfully'}, 201