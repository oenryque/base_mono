"""
Schemas Marshmallow para autenticação
"""
from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app.domain.dtos import UserRole, UserStatus

class LoginSchema(Schema):
    """Schema para login"""
    email = fields.Email(required=True, error_messages={'required': 'Email é obrigatório'})
    password = fields.Str(required=True, min_length=6, error_messages={
        'required': 'Senha é obrigatória',
        'min_length': 'Senha deve ter pelo menos 6 caracteres'
    })

class RegisterSchema(Schema):
    """Schema para registro"""
    email = fields.Email(required=True, error_messages={'required': 'Email é obrigatório'})
    password = fields.Str(required=True, min_length=8, error_messages={
        'required': 'Senha é obrigatória',
        'min_length': 'Senha deve ter pelo menos 8 caracteres'
    })
    name = fields.Str(required=True, min_length=2, error_messages={
        'required': 'Nome é obrigatório',
        'min_length': 'Nome deve ter pelo menos 2 caracteres'
    })
    role = fields.Str(validate=validate.OneOf(['admin', 'developer']), 
                     missing='developer', error_messages={
        'validator_failed': 'Role deve ser admin ou developer'
    })

class ChangePasswordSchema(Schema):
    """Schema para mudança de senha"""
    current_password = fields.Str(required=True, error_messages={
        'required': 'Senha atual é obrigatória'
    })
    new_password = fields.Str(required=True, min_length=8, error_messages={
        'required': 'Nova senha é obrigatória',
        'min_length': 'Nova senha deve ter pelo menos 8 caracteres'
    })
    confirm_password = fields.Str(required=True, error_messages={
        'required': 'Confirmação de senha é obrigatória'
    })
    
    @validates_schema
    def validate_passwords(self, data, **kwargs):
        """Valida se as senhas coincidem"""
        if data.get('new_password') != data.get('confirm_password'):
            raise ValidationError('Senhas não coincidem', 'confirm_password')

class RefreshTokenSchema(Schema):
    """Schema para refresh token"""
    refresh_token = fields.Str(required=True, error_messages={
        'required': 'Refresh token é obrigatório'
    })

class UserResponseSchema(Schema):
    """Schema para resposta de usuário"""
    id = fields.Int()
    email = fields.Email()
    name = fields.Str()
    role = fields.Str()
    status = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_login = fields.DateTime(allow_none=True)
    login_count = fields.Int(allow_none=True)
    last_ip = fields.Str(allow_none=True)

class TokenResponseSchema(Schema):
    """Schema para resposta de token"""
    access_token = fields.Str()
    refresh_token = fields.Str()
    token_type = fields.Str()
    expires_in = fields.Int()

class ErrorSchema(Schema):
    """Schema para erro"""
    error = fields.Str()
    message = fields.Str()
    details = fields.Dict(allow_none=True)
    status_code = fields.Int()

class SuccessSchema(Schema):
    """Schema para sucesso"""
    success = fields.Bool()
    message = fields.Str(allow_none=True)
    data = fields.Raw(allow_none=True)
