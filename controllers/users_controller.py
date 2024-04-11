from flask import jsonify, request
from functools import wraps
import jwt
from config import Config
from models.users import User
import bcrypt


# Role constants
SUPER = 'SUPER'
ADMIN = 'ADMIN'
USER = 'USER'

# Set to store invalidated tokens
token_blacklist = set()

# JWT token verification decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token.split(' ')[1], Config.SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

# Function to check if user is authorized
def is_authorized(role, allowed_roles):
    return role in allowed_roles

# Function to invalidate token
def invalidate_token(token):
    token_blacklist.add(token)

# Route to create new user
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role'] # SUPER, ADMIN, or USER

    User.create(username, password, role)

    return jsonify({'message': 'New user created successfully'}), 201

# Route for user login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username or password missing'}), 400

    user = User.find_by_username(username)
    if user:
        token = jwt.encode({'username': username, 'role': user['role']}, Config.SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# Route for user logout
def logout():
    token = request.headers.get('Authorization')
    # Invalidate token after logout
    invalidate_token(token)
    return jsonify({'message': 'Logged out successfully'}), 200

# Route for password reset
@token_required
def reset_password():
    data = request.get_json()
    new_password = data.get('new_password')

    # Get the token
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token.split(' ')[1], Config.SECRET_KEY, algorithms=["HS256"])
    username = decoded_token['username']

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    # Update password in MongoDB
    result = User.update(username, {'password': hashed_password})

    if result and result.modified_count == 1:
        return jsonify({'message': 'Password reset successful'}), 200
    else:
        return jsonify({'message': 'User not found or password not updated'}), 404

# Route for updating user information by username
@token_required
def update_user(username):
    data = request.get_json()

    # Extract updated user information from request body
    updated_username = data.get('username')
    updated_password = data.get('password')
    updated_role = data.get('role')

    # Get the token
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token.split(' ')[1], Config.SECRET_KEY, algorithms=["HS256"])
    role = decoded_token['role']

    # Check if the user has the necessary permissions
    if role in [SUPER, ADMIN, USER]:
        # Check if the user exists in the database
        user = User.find_by_username(username)
        if user is None:
            return jsonify({'message': 'User not found'}), 404

        # Update user information using User model
        update_data = {}
        if updated_username:
            update_data['username'] = updated_username
        if updated_password:
            # Hash the new password
            hashed_password = bcrypt.hashpw(updated_password.encode('utf-8'), bcrypt.gensalt())
            update_data['password'] = hashed_password
        if updated_role:
            update_data['role'] = updated_role

        # Update user's information using User model
        User.update(username, update_data)

        return jsonify({'message': 'User information updated successfully'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403

# Route for getting user details by username
@token_required
def get_user(username):
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token.split(' ')[1], Config.SECRET_KEY, algorithms=["HS256"])
    role = decoded_token['role']

    # Check if the user has the necessary permissions
    if role in [SUPER, ADMIN, USER]:
        # Retrieve user using User model
        user = User.find_by_username(username)
        if user:
            return jsonify({'username': user['username'], 'role': user['role']}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 403

# Route for getting all user details
@token_required
def get_all_users():
    token = request.headers.get('Authorization')
    decoded_token = jwt.decode(token.split(' ')[1], Config.SECRET_KEY, algorithms=["HS256"])
    role = decoded_token['role']

    if role == SUPER:
        all_users = []
        users = User.get_all()
        for user in users:
            all_users.append({'username': user['username'], 'role': user['role']})
        return jsonify(all_users), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 403
