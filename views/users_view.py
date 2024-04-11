# views.py
from flask import Blueprint
# from flask import Flask
from controllers.users_controller import create_user, login, reset_password, update_user, get_user, get_all_users, logout
# from config import Config

user_app = Blueprint('example_blueprint', __name__)

@user_app.route('/')
def index():
    return "This is an example app"


# Route to create new user
@user_app.route('/user', methods=['POST'])
def create_user_route():
    return create_user()

# Route for user login
@user_app.route('/login', methods=['POST'])
def login_route():
    return login()

# Route for user logout
@user_app.route('/logout', methods=['POST'])
def logout_route():
    return logout()

# Route for password reset
@user_app.route('/reset-password', methods=['POST'])
def reset_password_route():
    return reset_password()

# Route for updating user information by username
@user_app.route('/update-user/<username>', methods=['PUT'])
def update_user_route(username):
    return update_user(username)

# Route for getting user details by username
@user_app.route('/user/<username>', methods=['GET'])
def get_user_route(username):
    return get_user(username)

# Route for getting all user details
@user_app.route('/users', methods=['GET'])
def get_all_users_route():
    return get_all_users()
