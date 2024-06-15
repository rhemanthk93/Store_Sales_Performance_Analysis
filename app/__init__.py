from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_cors import CORS

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)

    # Import and register blueprints
    from app.routes.routes import main as main_blueprint
    from app.routes.test_routes import test as test_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(test_blueprint, url_prefix='/test')

    return app
