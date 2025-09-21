"""
Rotas de usuários
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.users.schemas import (
    CreateUserSchema, UpdateUserSchema, UserQuerySchema,
    UserResponseSchema, UserListResponseSchema, UserStatsSchema,
    ActivateUserSchema, DeactivateUserSchema, ResetPasswordSchema,
    ErrorSchema, SuccessSchema
)
from app.api.v1.users.service import UserService
from app.domain.dtos import (
    UserQueryDTO, CreateUserRequestDTO, UpdateUserRequestDTO,
    UserRole, UserStatus
)
from app.core.exceptions import ValidationError, ConflictError, NotFoundError, AuthorizationError
from app.core.security import require_admin, require_dev_or_admin
from app.core.logging import get_logger

logger = get_logger(__name__)

# Blueprint de usuários
users_bp = Blueprint('users', __name__)

# Schemas
create_user_schema = CreateUserSchema()
update_user_schema = UpdateUserSchema()
user_query_schema = UserQuerySchema()
user_response_schema = UserResponseSchema()
user_list_response_schema = UserListResponseSchema()
user_stats_schema = UserStatsSchema()
activate_user_schema = ActivateUserSchema()
deactivate_user_schema = DeactivateUserSchema()
reset_password_schema = ResetPasswordSchema()
error_schema = ErrorSchema()
success_schema = SuccessSchema()

# Serviço
user_service = UserService()

@users_bp.route('/', methods=['GET'])
@jwt_required()
@require_dev_or_admin()
def get_users():
    """Lista usuários (apenas para devs/admins)"""
    try:
        # Validar parâmetros de query
        query_data = user_query_schema.load(request.args)
        
        # Criar DTO
        query_dto = UserQueryDTO(
            page=query_data['page'],
            per_page=query_data['per_page'],
            search=query_data.get('search'),
            role=UserRole(query_data['role']) if query_data.get('role') else None,
            status=UserStatus(query_data['status']) if query_data.get('status') else None,
            sort_by=query_data['sort_by'],
            sort_order=query_data['sort_order']
        )
        
        # Buscar usuários
        result = user_service.get_users(query_dto)
        
        return jsonify({
            'success': True,
            'data': result.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': e.message,
            'details': e.payload
        }), 400
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de listar usuários: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/', methods=['POST'])
@jwt_required()
@require_admin()
def create_user():
    """Cria novo usuário (apenas para admins)"""
    try:
        # Validar dados de entrada
        data = create_user_schema.load(request.json)
        
        # Criar DTO
        create_dto = CreateUserRequestDTO(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            role=UserRole(data['role']),
            status=UserStatus(data['status'])
        )
        
        # Criar usuário
        result = user_service.create_user(create_dto)
        
        return jsonify({
            'success': True,
            'message': 'Usuário criado com sucesso',
            'data': result.to_dict()
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
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de criar usuário: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@require_dev_or_admin()
def get_user(user_id):
    """Obtém usuário por ID"""
    try:
        result = user_service.get_user_by_id(user_id)
        
        return jsonify({
            'success': True,
            'data': result.to_dict()
        }), 200
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de obter usuário: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_admin()
def update_user(user_id):
    """Atualiza usuário (apenas para admins)"""
    try:
        # Validar dados de entrada
        data = update_user_schema.load(request.json)
        
        # Criar DTO
        update_dto = UpdateUserRequestDTO(
            email=data.get('email'),
            name=data.get('name'),
            role=UserRole(data['role']) if data.get('role') else None,
            status=UserStatus(data['status']) if data.get('status') else None
        )
        
        # Atualizar usuário
        result = user_service.update_user(user_id, update_dto)
        
        return jsonify({
            'success': True,
            'message': 'Usuário atualizado com sucesso',
            'data': result.to_dict()
        }), 200
        
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
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de atualizar usuário: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_admin()
def delete_user(user_id):
    """Remove usuário (apenas para admins)"""
    try:
        success = user_service.delete_user(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Usuário removido com sucesso'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'InternalServerError',
                'message': 'Erro ao remover usuário'
            }), 500
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de remover usuário: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/<int:user_id>/activate', methods=['POST'])
@jwt_required()
@require_admin()
def activate_user(user_id):
    """Ativa usuário (apenas para admins)"""
    try:
        success = user_service.activate_user(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Usuário ativado com sucesso'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'InternalServerError',
                'message': 'Erro ao ativar usuário'
            }), 500
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de ativar usuário: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/<int:user_id>/deactivate', methods=['POST'])
@jwt_required()
@require_admin()
def deactivate_user(user_id):
    """Desativa usuário (apenas para admins)"""
    try:
        success = user_service.deactivate_user(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Usuário desativado com sucesso'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'InternalServerError',
                'message': 'Erro ao desativar usuário'
            }), 500
        
    except NotFoundError as e:
        return jsonify({
            'success': False,
            'error': 'NotFoundError',
            'message': e.message
        }), 404
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de desativar usuário: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_admin()
def get_user_stats():
    """Obtém estatísticas de usuários (apenas para admins)"""
    try:
        result = user_service.get_user_stats()
        
        return jsonify({
            'success': True,
            'data': result.to_dict()
        }), 200
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de estatísticas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500

@users_bp.route('/search', methods=['GET'])
@jwt_required()
@require_dev_or_admin()
def search_users():
    """Busca usuários por termo"""
    try:
        search_term = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'ValidationError',
                'message': 'Termo de busca é obrigatório'
            }), 400
        
        result = user_service.search_users(search_term, limit)
        
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in result]
        }), 200
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': 'ValidationError',
            'message': e.message
        }), 400
        
    except AuthorizationError as e:
        return jsonify({
            'success': False,
            'error': 'AuthorizationError',
            'message': e.message
        }), 403
        
    except Exception as e:
        logger.error(f"Erro no endpoint de busca: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor'
        }), 500
