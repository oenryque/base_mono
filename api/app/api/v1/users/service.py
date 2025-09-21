"""
Serviços de usuários
"""
from typing import List, Dict, Any, Tuple
from app.domain.dtos import (
    UserQueryDTO, UserStatsDTO, UserDTO, UserListResponseDTO, 
    PaginationDTO, CreateUserRequestDTO, UpdateUserRequestDTO,
    UserRole, UserStatus
)
from app.infra.repositories.user_repo import UserRepository
from app.core.security import hash_password, verify_password
from app.core.exceptions import ValidationError, ConflictError, NotFoundError, AuthorizationError
from app.core.utils import validate_password_strength, mask_email
from app.core.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)

class UserService:
    """Serviço de usuários"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def get_users(self, query_dto: UserQueryDTO) -> UserListResponseDTO:
        """Lista usuários com paginação e filtros"""
        try:
            # Buscar usuários
            users, total = self.user_repo.get_users_with_pagination(query_dto)
            
            # Converter para DTOs
            user_dtos = [UserDTO.from_model(user, include_sensitive=True) for user in users]
            
            # Criar paginação
            pages = (total + query_dto.per_page - 1) // query_dto.per_page
            pagination = PaginationDTO(
                page=query_dto.page,
                per_page=query_dto.per_page,
                total=total,
                pages=pages,
                has_prev=query_dto.page > 1,
                has_next=query_dto.page < pages,
                prev_num=query_dto.page - 1 if query_dto.page > 1 else None,
                next_num=query_dto.page + 1 if query_dto.page < pages else None
            )
            
            return UserListResponseDTO(users=user_dtos, pagination=pagination)
            
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {str(e)}")
            raise ValidationError("Erro interno ao listar usuários")
    
    def get_user_by_id(self, user_id: int) -> UserDTO:
        """Obtém usuário por ID"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            return UserDTO.from_model(user, include_sensitive=True)
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao obter usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao obter usuário")
    
    def create_user(self, create_dto: CreateUserRequestDTO) -> UserDTO:
        """Cria novo usuário"""
        try:
            # Verificar se email já existe
            if self.user_repo.find_by_email(create_dto.email):
                raise ConflictError("Email já está em uso")
            
            # Validar força da senha
            password_validation = validate_password_strength(create_dto.password)
            if not password_validation['is_valid']:
                raise ValidationError("Senha não atende aos critérios de segurança", 
                                    details={'password_errors': password_validation['errors']})
            
            # Criar usuário
            user_data = {
                'email': create_dto.email,
                'password_hash': hash_password(create_dto.password),
                'name': create_dto.name,
                'role': create_dto.role.value,
                'status': create_dto.status.value,
                'is_active': create_dto.status == UserStatus.ACTIVE
            }
            
            user = self.user_repo.create(**user_data)
            
            logger.info(f"Usuário criado: {mask_email(user.email)}")
            
            return UserDTO.from_model(user, include_sensitive=True)
            
        except (ConflictError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise ValidationError("Erro interno ao criar usuário")
    
    def update_user(self, user_id: int, update_dto: UpdateUserRequestDTO) -> UserDTO:
        """Atualiza usuário"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            # Verificar se email já existe (se estiver sendo alterado)
            if update_dto.email and update_dto.email != user.email:
                if self.user_repo.find_by_email(update_dto.email):
                    raise ConflictError("Email já está em uso")
            
            # Preparar dados para atualização
            update_data = {}
            if update_dto.email:
                update_data['email'] = update_dto.email
            if update_dto.name:
                update_data['name'] = update_dto.name
            if update_dto.role:
                update_data['role'] = update_dto.role.value
            if update_dto.status:
                update_data['status'] = update_dto.status.value
                update_data['is_active'] = update_dto.status == UserStatus.ACTIVE
            
            # Atualizar usuário
            self.user_repo.update(user_id, **update_data)
            
            # Buscar usuário atualizado
            updated_user = self.user_repo.get_by_id(user_id)
            
            logger.info(f"Usuário atualizado: {mask_email(updated_user.email)}")
            
            return UserDTO.from_model(updated_user, include_sensitive=True)
            
        except (NotFoundError, ConflictError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao atualizar usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao atualizar usuário")
    
    def delete_user(self, user_id: int) -> bool:
        """Remove usuário"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            # Não permitir que o usuário se delete
            # (implementar verificação se necessário)
            
            success = self.user_repo.delete(user_id)
            
            if success:
                logger.info(f"Usuário removido: {mask_email(user.email)}")
            
            return success
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao remover usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao remover usuário")
    
    def activate_user(self, user_id: int) -> bool:
        """Ativa usuário"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            success = self.user_repo.activate_user(user_id)
            
            if success:
                logger.info(f"Usuário ativado: {mask_email(user.email)}")
            
            return success
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao ativar usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao ativar usuário")
    
    def deactivate_user(self, user_id: int) -> bool:
        """Desativa usuário"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            success = self.user_repo.deactivate_user(user_id)
            
            if success:
                logger.info(f"Usuário desativado: {mask_email(user.email)}")
            
            return success
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao desativar usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao desativar usuário")
    
    def suspend_user(self, user_id: int) -> bool:
        """Suspende usuário"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            success = self.user_repo.suspend_user(user_id)
            
            if success:
                logger.info(f"Usuário suspenso: {mask_email(user.email)}")
            
            return success
            
        except NotFoundError:
            raise
        except Exception as e:
            logger.error(f"Erro ao suspender usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao suspender usuário")
    
    def reset_user_password(self, user_id: int, new_password: str) -> bool:
        """Redefine senha do usuário"""
        try:
            user = self.user_repo.get_by_id(user_id)
            if not user:
                raise NotFoundError("Usuário não encontrado")
            
            # Validar nova senha
            password_validation = validate_password_strength(new_password)
            if not password_validation['is_valid']:
                raise ValidationError("Senha não atende aos critérios de segurança", 
                                    details={'password_errors': password_validation['errors']})
            
            # Atualizar senha
            new_password_hash = hash_password(new_password)
            self.user_repo.update(user_id, password_hash=new_password_hash)
            
            logger.info(f"Senha redefinida para usuário: {mask_email(user.email)}")
            
            return True
            
        except (NotFoundError, ValidationError):
            raise
        except Exception as e:
            logger.error(f"Erro ao redefinir senha do usuário {user_id}: {str(e)}")
            raise ValidationError("Erro interno ao redefinir senha")
    
    def get_user_stats(self) -> UserStatsDTO:
        """Obtém estatísticas de usuários"""
        try:
            return self.user_repo.get_user_stats()
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            raise ValidationError("Erro interno ao obter estatísticas")
    
    def search_users(self, search_term: str, limit: int = 10) -> List[UserDTO]:
        """Busca usuários por termo"""
        try:
            users = self.user_repo.search_users(search_term)
            return [UserDTO.from_model(user, include_sensitive=True) for user in users[:limit]]
        except Exception as e:
            logger.error(f"Erro ao buscar usuários: {str(e)}")
            raise ValidationError("Erro interno ao buscar usuários")
