from flask import Flask, jsonify, redirect, send_from_directory
from flask_restful import Api, MethodNotAllowed, NotFound
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.jwt_errors import jwt
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from app.config import Config
from app.util.common import domain, port, prefix, build_swagger_config_json
from flask_swagger_ui import get_swaggerui_blueprint
from app.resources.swaggerConfig import SwaggerConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
    app.config['MAIL_PORT'] = 587 
    app.config['MAIL_USE_TLS'] = True 
    app.config['MAIL_USERNAME'] = 'francissteven1@gmail.com' 
    app.config['MAIL_PASSWORD'] = 'qekxlvlqhsfvkigk' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    # Enable CORS
    CORS(app)

    # Initialize API
    api = Api(app, prefix=prefix, catch_all_404s=True)

    # Initialize Swagger
    build_swagger_config_json()
    swaggerui_blueprint = get_swaggerui_blueprint(
        prefix,
        # f'{domain}:{port}{prefix}/swagger-config',
        f'https://agrieco-connect-be.azurewebsites.net{prefix}/swagger-config',
        config={
            'app_name': "Agrieco Connect API",
            "layout": "BaseLayout",
            "docExpansion": "none"
        },
    )

    app.register_blueprint(swaggerui_blueprint)
    
    # Register blueprints
    from .routes import api_routes, auth_routes, topic_routes, market_routes, event_routes, community_routes, user_routes, appointment_routes
    app.register_blueprint(api_routes.bp, url_prefix=prefix)
    app.register_blueprint(auth_routes.bp, url_prefix=prefix)
    app.register_blueprint(topic_routes.bp, url_prefix=prefix)
    app.register_blueprint(market_routes.bp, url_prefix=prefix)
    app.register_blueprint(event_routes.bp, url_prefix=prefix)
    app.register_blueprint(community_routes.bp, url_prefix=prefix)
    app.register_blueprint(user_routes.bp, url_prefix=prefix)
    app.register_blueprint(appointment_routes.bp, url_prefix=prefix)

    api.add_resource(SwaggerConfig, '/swagger-config')

    # Error handlers
    @app.errorhandler(NotFound)
    def handle_method_not_found(e):
        response = jsonify({"message": str(e)})
        response.status_code = 404
        return response
    
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed_error(e):
        response = jsonify({"message": str(e)})
        response.status_code = 405
        return response
    
    @app.route('/')
    def redirect_to_prefix():
        if app.config['PREFIX'] != '':
            return redirect(app.config['PREFIX'])
        
    
    return app
