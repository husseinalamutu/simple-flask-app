from flask import Flask
from flask_jwt_extended import JWTManager
from views import auth_bp
from config import Config

app = Flask(__name__)
jwt = JWTManager(app)
app.secret_key = Config.JWT_SECRET_KEY

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=False)
