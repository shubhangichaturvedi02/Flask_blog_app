from flask import Blueprint
from app.user.views import RegisterAPI, LoginAPI, ProfileAPI

user_bp = Blueprint('user', __name__)

register_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
profile_view = ProfileAPI.as_view('profile_api')

user_bp.add_url_rule('/register', view_func=register_view, methods=['POST'])
user_bp.add_url_rule('/login', view_func=login_view, methods=['POST'])
user_bp.add_url_rule('/get-profile', view_func=profile_view, methods=['GET'])
