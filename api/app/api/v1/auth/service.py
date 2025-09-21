"""
Serviços de autenticação
"""
from typing import Optional, Dict, Any
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from app.domain.models import User, BlacklistedToken
from app.domain.dtos import LoginRequestDTO, RegisterRequestDTO, ChangePasswordRequestDTO, TokenResponseDTO, UserDTO
from app.infra.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password, create_tokens
from app.core.exceptions import ValidationError, AuthenticationError, ConflictError, NotFoundError
from app.core.utils import get_client_ip, mask_email
from app.core.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)

class AuthService:
    """Serviço de autenticação"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def login(self, login_dto: LoginRequestDTO, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """Realiza login do usuário"""
        try:
            # Buscar usuário por email
            user = self.user_repo.find_active_by_email(login_dto.email)
            if not user:
                logger.warning(f"Tentativa de login com email inexistente: {mask_email(login_dto.email)}")
                raise AuthenticationError("Credenciais inválidas")
            
            # Verificar senha
            if not verify_password(login_dto.password, user.password_hash):
                logger.warning(f"Tentativa de login com senha incorreta: {mask_email(login_dto.email)}")
                raise AuthenticationError("Credenciais inválidas")
            
            # Verificar se usuário pode acessar o sistema
            if not user.can_access_admin():
                logger.warning(f"Tentativa de login de usuário sem acesso: {mask_email(login_dto.email)}")
                raise AuthenticationError("Acesso negado")
            
            # Atualizar informações de login
            self.user_repo.update_last_login(user.id, ip_address)
            
            # Criar tokens
            tokens = create_tokens(user)
            
            # Criar DTO do usuário
            user_dto = UserDTO.from_model(user, include_sensitive=True)
            
            logger.info(f"Login realizado com sucesso: {mask_email(user.email)}")
            
            return {
                'tokens': tokens,
                'user': user_dto.to_dict()
            }
            
        except Exception as e:
            if isinstance(e, (AuthenticationError, ValidationError)):
                raise
            logger.error(f"Erro no login: {str(e)}")
            raise AuthenticationError("Erro interno no login")
    
    def register(self, register_dto: RegisterRequestDTO, ip_address: Optional[str] = None) -> Dict[str, Any]:
        """Registra novo usuário"""
        try:
            # Verificar se email já existe
            if self.user_repo.find_by_email(register_dto.email):
                raise ConflictError("Email já está em uso")
            
            # Validar força da senha
            from app.core.utils import validate_password_strength
            password_validation = validate_password_strength(register_dto.password)
            if not password_validation['is_valid']:
                raise ValidationError("Senha não atende aos critérios de segurança", 
                                    details={'password_errors': password_validation['errors']})
            
            # Criar usuário
            user_data = {
                'email': register_dto.email,
                'password_hash': hash_password(register_dto.password),
                'name': register_dto.name,
                'role': register_dto.role.value,
                'is_active': True,
                'status': 'active'
            }
            
            user = self.user_repo.create(**user_data)
            
            # Criar tokens
            tokens = create_tokens(user)
            
            # Criar DTO do usuário
            user_dto = UserDTO.from_model(user, include_sensitive=True)
            
            logger.info(f"Usuário registrado com sucesso: {mask_email(user.email)}")
            
            # Enviar email de boas-vindas (assíncrono)
            try:
                from app.infra.tasks import send_welcome_email_task
                login_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:5173')}/login"
                send_welcome_email_task.delay(user.email, user.name, login_url)
            except Exception as e:
                logger.warning(f"Erro ao agendar email de boas-vindas: {str(e)}")
            
            return {
                'tokens': tokens,
                'user': user_dto.to_dict()
            }
            
        except Exception as e:
            if isinstance(e, (ConflictError, ValidationError)):
                raise
            logger.error(f"Erro no registro: {str(e)}")
            raise ValidationError("Erro interno no registro")
    
    def change_password(self, user_id: int, change_password_dto: ChangePasswordRequestDTO) -> bool:
        """Altera senha do usuário"""
        try:
            # Buscar usuário
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            # Verificar senha atual
            if not verify_password(change_password_dto.current_password, user.password_hash):
                raise ValidationError("Senha atual incorreta")
            
            # Validar nova senha
            from app.core.utils import validate_password_strength
            password_validation = validate_password_strength(change_password_dto.new_password)
            if not password_validation['is_valid']:
                raise ValidationError("Nova senha não atende aos critérios de segurança", 
                                    details={'password_errors': password_validation['errors']})
            
            # Atualizar senha
            user.password_hash = hash_password(change_password_dto.new_password)
            self.user_repo.update(user.id, password_hash=user.password_hash)
            
            logger.info(f"Senha alterada com sucesso para usuário: {mask_email(user.email)}")
            
            return True
            
        except Exception as e:
            if isinstance(e, (NotFoundError, ValidationError)):
                raise
            logger.error(f"Erro na mudança de senha: {str(e)}")
            raise ValidationError("Erro interno na mudança de senha")
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Renova access token"""
        try:
            from flask_jwt_extended import decode_token
            
            # Decodificar refresh token
            decoded_token = decode_token(refresh_token)
            user_id = decoded_token.get('sub')
            
            if not user_id:
                raise AuthenticationError("Token inválido")
            
            # Buscar usuário
            user = self.user_repo.get_by_id(user_id)
            if not user or not user.is_active:
                raise AuthenticationError("Usuário não encontrado ou inativo")
            
            # Criar novo access token
            user_data = {
                'user_id': user.id,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active
            }
            
            access_token = create_access_token(
                identity=user.id,
                additional_claims=user_data,
                expires_delta=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
            )
            
            logger.info(f"Token renovado para usuário: {mask_email(user.email)}")
            
            return {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds())
            }
            
        except Exception as e:
            if isinstance(e, AuthenticationError):
                raise
            logger.error(f"Erro na renovação de token: {str(e)}")
            raise AuthenticationError("Erro interno na renovação de token")
    
    def logout(self, user_id: int, jti: str) -> bool:
        """Realiza logout do usuário"""
        try:
            # Adicionar token à blacklist
            from datetime import datetime, timedelta
            
            # Obter informações do token atual
            current_jwt = get_jwt()
            token_type = current_jwt.get('type', 'access')
            exp = current_jwt.get('exp', 0)
            expires_at = datetime.utcfromtimestamp(exp)
            
            # Adicionar à blacklist
            BlacklistedToken.add_to_blacklist(
                jti=jti,
                token_type=token_type,
                user_id=user_id,
                expires_at=expires_at
            )
            
            logger.info(f"Logout realizado para usuário: {user_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro no logout: {str(e)}")
            return False
    
    def get_current_user(self, user_id: int) -> Dict[str, Any]:
        """Obtém dados do usuário atual"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            user_dto = UserDTO.from_model(user, include_sensitive=True)
            
            return user_dto.to_dict()
            
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise
            logger.error(f"Erro ao obter usuário atual: {str(e)}")
            raise NotFoundError("Erro interno ao obter usuário")
