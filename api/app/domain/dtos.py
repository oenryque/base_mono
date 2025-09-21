"""
Data Transfer Objects (DTOs) da aplicação
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """Roles de usuário"""
    ADMIN = "admin"
    DEVELOPER = "developer"
    USER = "user"

class UserStatus(str, Enum):
    """Status de usuário"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"

@dataclass
class UserDTO:
    """DTO para usuário"""
    id: int
    email: str
    name: str
    role: UserRole
    status: UserStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    login_count: Optional[int] = None
    last_ip: Optional[str] = None
    
    @classmethod
    def from_model(cls, user, include_sensitive=False):
        """Cria DTO a partir do modelo"""
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            role=UserRole(user.role),
            status=UserStatus(user.status),
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login if include_sensitive else None,
            login_count=user.login_count if include_sensitive else None,
            last_ip=user.last_ip if include_sensitive else None
        )
    
    def to_dict(self):
        """Converte para dicionário"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role.value,
            'status': self.status.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if self.last_login:
            data['last_login'] = self.last_login.isoformat()
        if self.login_count is not None:
            data['login_count'] = self.login_count
        if self.last_ip:
            data['last_ip'] = self.last_ip
        
        return data

@dataclass
class LoginRequestDTO:
    """DTO para requisição de login"""
    email: str
    password: str

@dataclass
class RegisterRequestDTO:
    """DTO para requisição de registro"""
    email: str
    password: str
    name: str
    role: UserRole = UserRole.DEVELOPER

@dataclass
class ChangePasswordRequestDTO:
    """DTO para requisição de mudança de senha"""
    current_password: str
    new_password: str
    confirm_password: str

@dataclass
class TokenResponseDTO:
    """DTO para resposta de token"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int

@dataclass
class UserQueryDTO:
    """DTO para query de usuários"""
    page: int = 1
    per_page: int = 10
    search: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"

@dataclass
class UserStatsDTO:
    """DTO para estatísticas de usuários"""
    total_users: int
    active_users: int
    inactive_users: int
    pending_users: int
    suspended_users: int
    admin_users: int
    developer_users: int
    user_users: int
    users_created_today: int
    users_created_this_week: int
    users_created_this_month: int
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'total_users': self.total_users,
            'active_users': self.active_users,
            'inactive_users': self.inactive_users,
            'pending_users': self.pending_users,
            'suspended_users': self.suspended_users,
            'admin_users': self.admin_users,
            'developer_users': self.developer_users,
            'user_users': self.user_users,
            'users_created_today': self.users_created_today,
            'users_created_this_week': self.users_created_this_week,
            'users_created_this_month': self.users_created_this_month
        }

@dataclass
class PaginationDTO:
    """DTO para paginação"""
    page: int
    per_page: int
    total: int
    pages: int
    has_prev: bool
    has_next: bool
    prev_num: Optional[int]
    next_num: Optional[int]
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'page': self.page,
            'per_page': self.per_page,
            'total': self.total,
            'pages': self.pages,
            'has_prev': self.has_prev,
            'has_next': self.has_next,
            'prev_num': self.prev_num,
            'next_num': self.next_num
        }

@dataclass
class UserListResponseDTO:
    """DTO para resposta de lista de usuários"""
    users: List[UserDTO]
    pagination: PaginationDTO
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'users': [user.to_dict() for user in self.users],
            'pagination': self.pagination.to_dict()
        }

@dataclass
class ErrorDTO:
    """DTO para erro"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    status_code: int = 400
    
    def to_dict(self):
        """Converte para dicionário"""
        data = {
            'error': self.error,
            'message': self.message,
            'status_code': self.status_code
        }
        if self.details:
            data['details'] = self.details
        return data

@dataclass
class SuccessDTO:
    """DTO para sucesso"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
    
    def to_dict(self):
        """Converte para dicionário"""
        data = {'success': self.success}
        if self.message:
            data['message'] = self.message
        if self.data is not None:
            data['data'] = self.data
        return data
