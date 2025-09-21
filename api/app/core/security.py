"""
Utilitários de segurança
"""
import bcrypt
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from flask import current_app
from app.domain.models import User

def hash_password(password: str) -> str:
    """Hash de senha usando bcrypt"""
    salt = bcrypt.gensalt(rounds=current_app.config.get('BCRYPT_ROUNDS', 12))
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verifica senha usando bcrypt"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_tokens(user: User) -> dict:
    """Cria access e refresh tokens para o usuário"""
    # Dados do usuário para o token
    user_data = {
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active
    }
    
    # Criar tokens
    access_token = create_access_token(
        identity=user.id,
        additional_claims=user_data,
        expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    )
    
    refresh_token = create_refresh_token(
        identity=user.id,
        additional_claims=user_data,
        expires_delta=current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
    )
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
    }

def jwt_config(app):
    """Configura JWT para a aplicação"""
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Verifica se o token está na blacklist"""
        # Implementar verificação de blacklist se necessário
        return False
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handler para token expirado"""
        return {
            'error': 'TokenExpiredError',
            'message': 'Token expirado',
            'status_code': 401
        }, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handler para token inválido"""
        return {
            'error': 'InvalidTokenError',
            'message': 'Token inválido',
            'status_code': 401
        }, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handler para token ausente"""
        return {
            'error': 'MissingTokenError',
            'message': 'Token de autorização ausente',
            'status_code': 401
        }, 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        """Handler para token não fresco"""
        return {
            'error': 'TokenNotFreshError',
            'message': 'Token não é fresco',
            'status_code': 401
        }, 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handler para token revogado"""
        return {
            'error': 'TokenRevokedError',
            'message': 'Token foi revogado',
            'status_code': 401
        }, 401

def require_roles(*roles):
    """Decorator para verificar roles do usuário"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            from flask_jwt_extended import get_jwt_identity, get_jwt
            from app.core.exceptions import AuthorizationError
            
            current_user_id = get_jwt_identity()
            if not current_user_id:
                raise AuthorizationError("Usuário não autenticado")
            
            user_claims = get_jwt()
            user_role = user_claims.get('role')
            
            if user_role not in roles:
                raise AuthorizationError(f"Acesso negado. Roles necessários: {', '.join(roles)}")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin():
    """Decorator para verificar se o usuário é admin"""
    return require_roles('admin')

def require_dev_or_admin():
    """Decorator para verificar se o usuário é dev ou admin"""
    return require_roles('admin', 'developer')
