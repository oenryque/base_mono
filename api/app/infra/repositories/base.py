"""
Repositório base com operações CRUD genéricas
"""
from typing import Type, TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from app import db
from app.domain.models import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    """Repositório base com operações CRUD"""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def create(self, **kwargs) -> T:
        """Cria um novo registro"""
        instance = self.model_class(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Busca registro por ID"""
        return self.model_class.query.get(id)
    
    def get_by_field(self, field: str, value: Any) -> Optional[T]:
        """Busca registro por campo específico"""
        return self.model_class.query.filter(getattr(self.model_class, field) == value).first()
    
    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        """Busca todos os registros"""
        query = self.model_class.query
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Atualiza registro por ID"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
        return instance
    
    def delete(self, id: int) -> bool:
        """Remove registro por ID"""
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False
    
    def count(self) -> int:
        """Conta total de registros"""
        return self.model_class.query.count()
    
    def exists(self, **kwargs) -> bool:
        """Verifica se registro existe"""
        return self.model_class.query.filter_by(**kwargs).first() is not None
    
    def filter_by(self, **kwargs) -> List[T]:
        """Filtra registros por campos"""
        return self.model_class.query.filter_by(**kwargs).all()
    
    def filter_by_conditions(self, conditions: List) -> List[T]:
        """Filtra registros por condições SQLAlchemy"""
        return self.model_class.query.filter(and_(*conditions)).all()
    
    def search(self, search_term: str, fields: List[str]) -> List[T]:
        """Busca por termo em campos específicos"""
        conditions = []
        for field in fields:
            conditions.append(getattr(self.model_class, field).ilike(f'%{search_term}%'))
        return self.model_class.query.filter(or_(*conditions)).all()
    
    def paginate(self, page: int = 1, per_page: int = 10, order_by: Optional[str] = None, 
                order_direction: str = 'asc') -> tuple[List[T], int]:
        """Pagina registros"""
        query = self.model_class.query
        
        # Ordenação
        if order_by and hasattr(self.model_class, order_by):
            if order_direction.lower() == 'desc':
                query = query.order_by(desc(getattr(self.model_class, order_by)))
            else:
                query = query.order_by(asc(getattr(self.model_class, order_by)))
        
        # Contar total
        total = query.count()
        
        # Aplicar paginação
        offset = (page - 1) * per_page
        items = query.offset(offset).limit(per_page).all()
        
        return items, total
    
    def bulk_create(self, items: List[Dict[str, Any]]) -> List[T]:
        """Cria múltiplos registros"""
        instances = [self.model_class(**item) for item in items]
        db.session.add_all(instances)
        db.session.commit()
        return instances
    
    def bulk_update(self, updates: List[Dict[str, Any]]) -> int:
        """Atualiza múltiplos registros"""
        count = 0
        for update in updates:
            id = update.pop('id')
            if self.update(id, **update):
                count += 1
        return count
    
    def bulk_delete(self, ids: List[int]) -> int:
        """Remove múltiplos registros"""
        count = 0
        for id in ids:
            if self.delete(id):
                count += 1
        return count
