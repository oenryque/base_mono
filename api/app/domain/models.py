"""
Modelos de domínio da aplicação
"""
from datetime import datetime
from app import db
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID
import uuid

class BaseModel(db.Model):
    """Modelo base com campos comuns"""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Converte modelo para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def update_from_dict(self, data):
        """Atualiza modelo a partir de dicionário"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

class User(BaseModel):
    """Modelo de usuário (Devs/Admins)"""
    __tablename__ = 'users'
    
    # Campos obrigatórios
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    
    # Campos de controle
    role = db.Column(db.String(50), nullable=False, default='developer')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    status = db.Column(db.String(50), default='active', nullable=False)
    
    # Campos opcionais
    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, default=0, nullable=False)
    last_ip = db.Column(db.String(45), nullable=True)  # IPv6 support
    
    # Relacionamentos
    # Adicionar relacionamentos aqui conforme necessário
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self, include_sensitive=False):
        """Converte usuário para dicionário"""
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'is_active': self.is_active,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_sensitive:
            data.update({
                'last_login': self.last_login.isoformat() if self.last_login else None,
                'login_count': self.login_count,
                'last_ip': self.last_ip,
            })
        
        return data
    
    @classmethod
    def find_by_email(cls, email):
        """Encontra usuário por email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Encontra usuário por ID"""
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def find_active_by_email(cls, email):
        """Encontra usuário ativo por email"""
        return cls.query.filter_by(email=email, is_active=True).first()
    
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.role == 'admin'
    
    def is_developer(self):
        """Verifica se o usuário é desenvolvedor"""
        return self.role == 'developer'
    
    def can_access_admin(self):
        """Verifica se o usuário pode acessar área administrativa"""
        return self.is_active and self.role in ['admin', 'developer']
    
    def update_login_info(self, ip_address=None):
        """Atualiza informações de login"""
        self.last_login = datetime.utcnow()
        self.login_count += 1
        if ip_address:
            self.last_ip = ip_address
        db.session.commit()

class BlacklistedToken(db.Model):
    """Modelo para tokens na blacklist"""
    __tablename__ = 'blacklisted_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False, index=True)  # JWT ID
    token_type = db.Column(db.String(10), nullable=False)  # access ou refresh
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Relacionamento
    user = db.relationship('User', backref='blacklisted_tokens')
    
    def __repr__(self):
        return f'<BlacklistedToken {self.jti}>'
    
    @classmethod
    def is_blacklisted(cls, jti):
        """Verifica se token está na blacklist"""
        token = cls.query.filter_by(jti=jti).first()
        if token and token.expires_at > datetime.utcnow():
            return True
        return False
    
    @classmethod
    def add_to_blacklist(cls, jti, token_type, user_id, expires_at):
        """Adiciona token à blacklist"""
        token = cls(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at
        )
        db.session.add(token)
        db.session.commit()
        return token

# Event listeners
@event.listens_for(User, 'before_insert')
def set_user_defaults(mapper, connection, target):
    """Define valores padrão antes de inserir usuário"""
    if not target.role:
        target.role = 'developer'
    if not target.status:
        target.status = 'active'

@event.listens_for(User, 'before_update')
def update_user_timestamp(mapper, connection, target):
    """Atualiza timestamp de modificação"""
    target.updated_at = datetime.utcnow()
