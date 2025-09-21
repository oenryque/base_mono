"""
Repositório específico para usuários
"""
from typing import List, Optional, Tuple
from sqlalchemy import and_, or_, desc, asc, func
from datetime import datetime, timedelta
from app.domain.models import User
from app.domain.dtos import UserQueryDTO, UserStatsDTO, UserRole, UserStatus
from .base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repositório para usuários"""
    
    def __init__(self):
        super().__init__(User)
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return self.get_by_field('email', email)
    
    def find_active_by_email(self, email: str) -> Optional[User]:
        """Busca usuário ativo por email"""
        return User.query.filter_by(email=email, is_active=True).first()
    
    def find_by_role(self, role: str) -> List[User]:
        """Busca usuários por role"""
        return self.filter_by(role=role)
    
    def find_active_users(self) -> List[User]:
        """Busca usuários ativos"""
        return self.filter_by(is_active=True)
    
    def find_inactive_users(self) -> List[User]:
        """Busca usuários inativos"""
        return self.filter_by(is_active=False)
    
    def search_users(self, search_term: str) -> List[User]:
        """Busca usuários por termo"""
        return self.search(search_term, ['name', 'email'])
    
    def get_users_with_pagination(self, query_dto: UserQueryDTO) -> Tuple[List[User], int]:
        """Busca usuários com paginação e filtros"""
        query = User.query
        
        # Filtros
        if query_dto.search:
            search_conditions = [
                User.name.ilike(f'%{query_dto.search}%'),
                User.email.ilike(f'%{query_dto.search}%')
            ]
            query = query.filter(or_(*search_conditions))
        
        if query_dto.role:
            query = query.filter(User.role == query_dto.role.value)
        
        if query_dto.status:
            query = query.filter(User.status == query_dto.status.value)
        
        # Ordenação
        if hasattr(User, query_dto.sort_by):
            if query_dto.sort_order.lower() == 'desc':
                query = query.order_by(desc(getattr(User, query_dto.sort_by)))
            else:
                query = query.order_by(asc(getattr(User, query_dto.sort_by)))
        
        # Contar total
        total = query.count()
        
        # Aplicar paginação
        offset = (query_dto.page - 1) * query_dto.per_page
        users = query.offset(offset).limit(query_dto.per_page).all()
        
        return users, total
    
    def get_user_stats(self) -> UserStatsDTO:
        """Obtém estatísticas de usuários"""
        now = datetime.utcnow()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Contagens básicas
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        inactive_users = User.query.filter_by(is_active=False).count()
        
        # Contagens por status
        pending_users = User.query.filter_by(status='pending').count()
        suspended_users = User.query.filter_by(status='suspended').count()
        
        # Contagens por role
        admin_users = User.query.filter_by(role='admin').count()
        developer_users = User.query.filter_by(role='developer').count()
        user_users = User.query.filter_by(role='user').count()
        
        # Contagens por período
        users_created_today = User.query.filter(
            func.date(User.created_at) == today
        ).count()
        
        users_created_this_week = User.query.filter(
            User.created_at >= week_ago
        ).count()
        
        users_created_this_month = User.query.filter(
            User.created_at >= month_ago
        ).count()
        
        return UserStatsDTO(
            total_users=total_users,
            active_users=active_users,
            inactive_users=inactive_users,
            pending_users=pending_users,
            suspended_users=suspended_users,
            admin_users=admin_users,
            developer_users=developer_users,
            user_users=user_users,
            users_created_today=users_created_today,
            users_created_this_week=users_created_this_week,
            users_created_this_month=users_created_this_month
        )
    
    def get_recent_logins(self, days: int = 7) -> List[User]:
        """Busca usuários que fizeram login recentemente"""
        since = datetime.utcnow() - timedelta(days=days)
        return User.query.filter(
            User.last_login >= since
        ).order_by(desc(User.last_login)).all()
    
    def get_users_by_creation_date(self, start_date: datetime, end_date: datetime) -> List[User]:
        """Busca usuários criados em um período"""
        return User.query.filter(
            and_(
                User.created_at >= start_date,
                User.created_at <= end_date
            )
        ).order_by(desc(User.created_at)).all()
    
    def activate_user(self, user_id: int) -> bool:
        """Ativa usuário"""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = True
            user.status = 'active'
            db.session.commit()
            return True
        return False
    
    def deactivate_user(self, user_id: int) -> bool:
        """Desativa usuário"""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            user.status = 'inactive'
            db.session.commit()
            return True
        return False
    
    def suspend_user(self, user_id: int) -> bool:
        """Suspende usuário"""
        user = self.get_by_id(user_id)
        if user:
            user.is_active = False
            user.status = 'suspended'
            db.session.commit()
            return True
        return False
    
    def update_user_role(self, user_id: int, role: str) -> bool:
        """Atualiza role do usuário"""
        user = self.get_by_id(user_id)
        if user:
            user.role = role
            db.session.commit()
            return True
        return False
    
    def update_last_login(self, user_id: int, ip_address: Optional[str] = None) -> bool:
        """Atualiza informações de último login"""
        user = self.get_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            user.login_count += 1
            if ip_address:
                user.last_ip = ip_address
            db.session.commit()
            return True
        return False
    
    def get_admins(self) -> List[User]:
        """Busca todos os administradores"""
        return self.find_by_role('admin')
    
    def get_developers(self) -> List[User]:
        """Busca todos os desenvolvedores"""
        return self.find_by_role('developer')
    
    def get_users_with_access(self) -> List[User]:
        """Busca usuários que podem acessar o sistema (devs e admins)"""
        return User.query.filter(
            and_(
                User.is_active == True,
                User.role.in_(['admin', 'developer'])
            )
        ).all()
