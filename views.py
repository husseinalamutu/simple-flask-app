from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def home():
    return render_template('base.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'USER')

        if not username or not password:
            return render_template('register.html', message='Username and password are required')

        if User.find_by_username(username):
            return render_template('register.html', message='Username already exists')

        User.create(username, password, role)
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            return render_template('login.html', message='Username and password are required')

        user = User.find_by_username(username)
        if not user or not check_password_hash(user["password"], password):
            return render_template('login.html', message='Invalid username or password')

        if user["role"] == 'USER':
            access_token = create_access_token(identity=username)
            session['token'] = access_token
            session['user_role'] = 'user'  # Add user role to session
            return redirect(url_for('auth.dashboard', token=access_token))
        else:
            access_token = create_access_token(identity=username)
            session['token'] = access_token
            return redirect(url_for('auth.admin', token=access_token))

    return render_template('login.html')

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        if not username or not new_password:
            return render_template('reset_password.html', message='Username and new password are required')

        user = User.find_by_username(username)
        if not user:
            return render_template('reset_password.html', message='User not found')

        hashed_password = generate_password_hash(new_password)
        User.update(user["_id"], {"password": hashed_password})

        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

@auth_bp.route('/update', methods=['GET', 'POST'])
def update_user_by_username():
    if request.method == 'POST':
        username = request.form['username']

        if not username:
            return render_template('update_user.html', message='Username is required')

        user = User.find_by_username(username)

        if not user:
            return render_template('update_user.html', message='User not found')

        update_data = {}
        if request.form['new_password'] and request.form['new_password'] != '':
            hashed_password = generate_password_hash(request.form['new_password'])
            update_data["password"] = hashed_password
        if request.form['role'] and request.form['role'] != '':
            update_data["role"] = request.form['role']

        if update_data:
            User.update(user['username'], update_data)
            return redirect(url_for('auth.login'))

    return render_template('update_user.html')


@auth_bp.route('/logout')
def logout():
    # You can implement any logout logic here, such as clearing JWT tokens or session data
    return redirect(url_for('auth.login'))

# Other routes and functions go here...
@auth_bp.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.get_all()
    return render_template('all_users.html', all_users=all_users)

@auth_bp.route('/user/username', methods=['POST'])
def get_user_by_username():
    username = request.form.get('username')

    if not username:
        return render_template('error.html', message='Username is required'), 400

    user = User.find_by_username(username)

    if not user:
        return render_template('no_users.html')  # User not found

    return render_template('user.html', user=user)

@auth_bp.route('/dashboard')
def dashboard():
    token = request.args.get('token') or session.pop('token', None)  # Get token from args or session
    if token:
        return render_template('dashboard.html', token=token)  # , is_super=is_super
    else:
        return redirect(url_for('auth.login'))

@auth_bp.route('/admin')
def admin():
    token = request.args.get('token')
    if token:
        return render_template('admin.html', token=token)  # , is_super=is_super
    else:
        return redirect(url_for('auth.login'))

