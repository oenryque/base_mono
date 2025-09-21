"""
Factory da aplicação Flask
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

def create_app(config_name=None):
    """Factory da aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config.from_object('app.config.Config')
    
    # Configurar CORS
    CORS(app, origins=[app.config.get('FRONTEND_URL', 'http://localhost:5173')])
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    
    # Configurar JWT
    from app.core.security import jwt_config
    jwt_config(app)
    
    # Registrar blueprints
    from app.api.health import health_bp
    from app.api.v1.auth import auth_bp
    from app.api.v1.users import users_bp
    
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    
    # Error handlers
    from app.core.exceptions import register_error_handlers
    register_error_handlers(app)
    
    # CLI commands
    from app.cli import register_commands
    register_commands(app)
    
    return app
