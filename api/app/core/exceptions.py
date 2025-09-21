"""
Exceções customizadas da aplicação
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from app.core.exceptions import ValidationError, AuthenticationError, AuthorizationError, NotFoundError

class APIException(Exception):
    """Exceção base da API"""
    status_code = 500
    message = "Erro interno do servidor"
    
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

class ValidationError(APIException):
    """Erro de validação"""
    status_code = 400
    message = "Dados inválidos"

class AuthenticationError(APIException):
    """Erro de autenticação"""
    status_code = 401
    message = "Não autenticado"

class AuthorizationError(APIException):
    """Erro de autorização"""
    status_code = 403
    message = "Acesso negado"

class NotFoundError(APIException):
    """Recurso não encontrado"""
    status_code = 404
    message = "Recurso não encontrado"

class ConflictError(APIException):
    """Conflito de recursos"""
    status_code = 409
    message = "Conflito de recursos"

def register_error_handlers(app):
    """Registra handlers de erro"""
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        """Handler para exceções da API"""
        response = {
            'error': error.__class__.__name__,
            'message': error.message,
            'status_code': error.status_code
        }
        if error.payload:
            response['details'] = error.payload
        return jsonify(response), error.status_code
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handler para exceções HTTP"""
        response = {
            'error': error.__class__.__name__,
            'message': error.description,
            'status_code': error.code
        }
        return jsonify(response), error.code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handler para erros de validação"""
        response = {
            'error': 'ValidationError',
            'message': error.message,
            'status_code': 400
        }
        if error.payload:
            response['details'] = error.payload
        return jsonify(response), 400
    
    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        """Handler para erros de autenticação"""
        response = {
            'error': 'AuthenticationError',
            'message': error.message,
            'status_code': 401
        }
        return jsonify(response), 401
    
    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):
        """Handler para erros de autorização"""
        response = {
            'error': 'AuthorizationError',
            'message': error.message,
            'status_code': 403
        }
        return jsonify(response), 403
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """Handler para erros de não encontrado"""
        response = {
            'error': 'NotFoundError',
            'message': error.message,
            'status_code': 404
        }
        return jsonify(response), 404
    
    @app.errorhandler(ConflictError)
    def handle_conflict_error(error):
        """Handler para erros de conflito"""
        response = {
            'error': 'ConflictError',
            'message': error.message,
            'status_code': 409
        }
        return jsonify(response), 409
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handler para erros internos"""
        response = {
            'error': 'InternalServerError',
            'message': 'Erro interno do servidor',
            'status_code': 500
        }
        return jsonify(response), 500
