from flask import Flask
from config import Config
from views.users_view import user_app  # Import the user views app
# from example_blueprint import example_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.register_blueprint(user_app)

if __name__ == '__main__':
    app.run(debug=True)
