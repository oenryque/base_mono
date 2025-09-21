"""
Utilitários de paginação
"""
from flask import request
from math import ceil

class Pagination:
    """Classe para paginação"""
    
    def __init__(self, page=1, per_page=10, total=0):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = ceil(total / per_page) if per_page > 0 else 0
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1 if self.has_prev else None
        self.next_num = page + 1 if self.has_next else None
    
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

def get_pagination_params():
    """Obtém parâmetros de paginação da requisição"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Validar parâmetros
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > 100:  # Limite máximo
        per_page = 100
    
    return page, per_page

def paginate_query(query, page=None, per_page=None):
    """Pagina uma query do SQLAlchemy"""
    if page is None or per_page is None:
        page, per_page = get_pagination_params()
    
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return Pagination(page=page, per_page=per_page, total=total), items

def paginate_list(items, page=None, per_page=None):
    """Pagina uma lista"""
    if page is None or per_page is None:
        page, per_page = get_pagination_params()
    
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]
    
    return Pagination(page=page, per_page=per_page, total=total), paginated_items
