from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from .middleware.request_verification import RequestVerificationMiddleware

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
#     middleware = RequestVerificationMiddleware(app)

# # Apply the middleware to the Flask application
#     app.wsgi_app = middleware

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.user.routes import user_bp
    from app.article.routes import article_bp

    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(article_bp, url_prefix='/api/v1')

    # app.wsgi_app = RequestVerificationMiddleware(app)


    return app
