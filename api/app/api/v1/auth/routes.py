"""
Rotas de autenticação
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.api.v1.auth.schemas import (
    LoginSchema, RegisterSchema, ChangePasswordSchema, 
    RefreshTokenSchema, UserResponseSchema, TokenResponseSchema,
    ErrorSchema, SuccessSchema
)
from app.api.v1.auth.service import AuthService
from app.domain.dtos import LoginRequestDTO, RegisterRequestDTO, ChangePasswordRequestDTO
from app.core.exceptions import ValidationError, AuthenticationError, ConflictError, NotFoundError
from app.core.utils import get_client_ip
from app.core.logging import get_logger

logger = get_logger(__name__)

# Blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

# Schemas
login_schema = LoginSchema()
register_schema = RegisterSchema()
change_password_schema = ChangePasswordSchema()
refresh_token_schema = RefreshTokenSchema()
user_response_schema = UserResponseSchema()
token_response_schema = TokenResponseSchema()
error_schema = ErrorSchema()
success_schema = SuccessSchema()

# Serviço
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de desenvolvedor/administrador"""
    try:
        # Validar dados de entrada
        data = login_schema.load(request.json)
        
        # Criar DTO
        login_dto = LoginRequestDTO(
            email=data['email'],
            password=data['password']
        )
        
        # Obter IP do cliente
        ip_address = get_client_ip()
        
        # Realizar login
        result = auth_service.login(login_dto, ip_address)
        
        return jsonify({
            'success': True,
            'message': 'Login realizado com sucesso',
            'data': result
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': e.message,
            'details': e.payload
        }), 400
        
    except AuthenticationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthenticationError',
            'message': e.message
        }), 401
        
    except Exception as e:
        logger.error(f"Erro no endpoint de login: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registro de desenvolvedor/administrador"""
    try:
        # Validar dados de entrada
        data = register_schema.load(request.json)
        
        # Criar DTO
        from app.domain.dtos import UserRole
        register_dto = RegisterRequestDTO(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            role=UserRole(data['role'])
        )
        
        # Obter IP do cliente
        ip_address = get_client_ip()
        
        # Realizar registro
        result = auth_service.register(register_dto, ip_address)
        
        return jsonify({
            'success': True,
            'message': 'Usuário registrado com sucesso',
            'data': result
        }), 201
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': e.message,
            'details': e.payload
        }), 400
        
    except ConflictError as e:
        return jsonify({
            'success': False,
            'error': 'ConflictError',
            'message': e.message
        }), 409
        
    except Exception as e:
        logger.error(f"Erro no endpoint de registro: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obtém dados do usuário atual"""
    try:
        user_id = get_jwt_identity()
        result = auth_service.get_current_user(user_id)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except Exception as e:
        logger.error(f"Erro no endpoint de usuário atual: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Altera senha do usuário atual"""
    try:
        # Validar dados de entrada
        data = change_password_schema.load(request.json)
        
        # Criar DTO
        change_password_dto = ChangePasswordRequestDTO(
            current_password=data['current_password'],
            new_password=data['new_password'],
            confirm_password=data['confirm_password']
        )
        
        # Obter ID do usuário
        user_id = get_jwt_identity()
        
        # Alterar senha
        auth_service.change_password(user_id, change_password_dto)
        
        return jsonify({
            'success': True,
            'message': 'Senha alterada com sucesso'
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': e.message,
            'details': e.payload
        }), 400
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except Exception as e:
        logger.error(f"Erro no endpoint de mudança de senha: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Renova access token"""
    try:
        # Validar dados de entrada
        data = refresh_token_schema.load(request.json)
        
        # Renovar token
        result = auth_service.refresh_token(data['refresh_token'])
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': e.message
        }), 400
        
    except AuthenticationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthenticationError',
            'message': e.message
        }), 401
        
    except Exception as e:
        logger.error(f"Erro no endpoint de renovação de token: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout do usuário"""
    try:
        # Obter informações do token
        user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        
        # Realizar logout
        auth_service.logout(user_id, jti)
        
        return jsonify({
            'success': True,
            'message': 'Logout realizado com sucesso'
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no endpoint de logout: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500
