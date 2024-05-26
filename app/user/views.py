from flask.views import MethodView
from flask import request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.decorators import request_verification_required


class RegisterAPI(MethodView):
    @request_verification_required 
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify(message="User Already Exists"), 400
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User registered successfully"), 201

class LoginAPI(MethodView):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'username': user.username, 'email': user.email})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(message="Invalid credentials"), 401

class ProfileAPI(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user['email']).first()
        user_data = {
            'username': user.username,
            'email': user.email
        }
        return jsonify(user_data), 200
