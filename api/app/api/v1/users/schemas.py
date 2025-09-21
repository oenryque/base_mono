"""
Schemas Marshmallow para usuários
"""
from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app.domain.dtos import UserRole, UserStatus

class CreateUserSchema(Schema):
    """Schema para criação de usuário"""
    email = fields.Email(required=True, error_messages={'required': 'Email é obrigatório'})
    password = fields.Str(required=True, min_length=8, error_messages={
        'required': 'Senha é obrigatória',
        'min_length': 'Senha deve ter pelo menos 8 caracteres'
    })
    name = fields.Str(required=True, min_length=2, error_messages={
        'required': 'Nome é obrigatório',
        'min_length': 'Nome deve ter pelo menos 2 caracteres'
    })
    role = fields.Str(validate=validate.OneOf(['admin', 'developer', 'user']), 
                     missing='developer', error_messages={
        'validator_failed': 'Role deve ser admin, developer ou user'
    })
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'pending', 'suspended']), 
                       missing='active', error_messages={
        'validator_failed': 'Status deve ser active, inactive, pending ou suspended'
    })

class UpdateUserSchema(Schema):
    """Schema para atualização de usuário"""
    email = fields.Email(error_messages={'invalid': 'Email inválido'})
    name = fields.Str(min_length=2, error_messages={
        'min_length': 'Nome deve ter pelo menos 2 caracteres'
    })
    role = fields.Str(validate=validate.OneOf(['admin', 'developer', 'user']), 
                     error_messages={
        'validator_failed': 'Role deve ser admin, developer ou user'
    })
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'pending', 'suspended']), 
                       error_messages={
        'validator_failed': 'Status deve ser active, inactive, pending ou suspended'
    })

class UserQuerySchema(Schema):
    """Schema para query de usuários"""
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=10, validate=validate.Range(min=1, max=100))
    search = fields.Str(allow_none=True)
    role = fields.Str(validate=validate.OneOf(['admin', 'developer', 'user']), 
                     allow_none=True, error_messages={
        'validator_failed': 'Role deve ser admin, developer ou user'
    })
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'pending', 'suspended']), 
                       allow_none=True, error_messages={
        'validator_failed': 'Status deve ser active, inactive, pending ou suspended'
    })
    sort_by = fields.Str(missing='created_at', 
                        validate=validate.OneOf(['id', 'name', 'email', 'created_at', 'updated_at']),
                        error_messages={
        'validator_failed': 'Campo de ordenação inválido'
    })
    sort_order = fields.Str(missing='desc', 
                           validate=validate.OneOf(['asc', 'desc']),
                           error_messages={
        'validator_failed': 'Ordem deve ser asc ou desc'
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

class UserListResponseSchema(Schema):
    """Schema para resposta de lista de usuários"""
    users = fields.List(fields.Nested(UserResponseSchema))
    pagination = fields.Dict()

class UserStatsSchema(Schema):
    """Schema para estatísticas de usuários"""
    total_users = fields.Int()
    active_users = fields.Int()
    inactive_users = fields.Int()
    pending_users = fields.Int()
    suspended_users = fields.Int()
    admin_users = fields.Int()
    developer_users = fields.Int()
    user_users = fields.Int()
    users_created_today = fields.Int()
    users_created_this_week = fields.Int()
    users_created_this_month = fields.Int()

class ActivateUserSchema(Schema):
    """Schema para ativação de usuário"""
    user_id = fields.Int(required=True, validate=validate.Range(min=1), 
                        error_messages={'required': 'ID do usuário é obrigatório'})

class DeactivateUserSchema(Schema):
    """Schema para desativação de usuário"""
    user_id = fields.Int(required=True, validate=validate.Range(min=1), 
                        error_messages={'required': 'ID do usuário é obrigatório'})

class ResetPasswordSchema(Schema):
    """Schema para redefinição de senha"""
    user_id = fields.Int(required=True, validate=validate.Range(min=1), 
                        error_messages={'required': 'ID do usuário é obrigatório'})
    new_password = fields.Str(required=True, min_length=8, error_messages={
        'required': 'Nova senha é obrigatória',
        'min_length': 'Nova senha deve ter pelo menos 8 caracteres'
    })

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
