"""
Utilitários gerais da aplicação
"""
import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from flask import current_app

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password: str) -> Dict[str, Any]:
    """Valida força da senha"""
    errors = []
    
    if len(password) < 8:
        errors.append("Senha deve ter pelo menos 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Senha deve conter pelo menos uma letra maiúscula")
    
    if not re.search(r'[a-z]', password):
        errors.append("Senha deve conter pelo menos uma letra minúscula")
    
    if not re.search(r'\d', password):
        errors.append("Senha deve conter pelo menos um número")
    
    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }

def sanitize_string(text: str) -> str:
    """Sanitiza string removendo caracteres perigosos"""
    if not text:
        return ""
    
    # Remover caracteres de controle
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Remover espaços extras
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def format_datetime(dt: datetime, format_str: str = None) -> str:
    """Formata datetime para string"""
    if not dt:
        return None
    
    if format_str is None:
        format_str = '%Y-%m-%d %H:%M:%S'
    
    return dt.strftime(format_str)

def parse_datetime(date_str: str, format_str: str = None) -> Optional[datetime]:
    """Converte string para datetime"""
    if not date_str:
        return None
    
    if format_str is None:
        format_str = '%Y-%m-%d %H:%M:%S'
    
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None

def get_client_ip() -> str:
    """Obtém IP do cliente"""
    from flask import request
    
    # Verificar headers de proxy
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def get_user_agent() -> str:
    """Obtém User-Agent do cliente"""
    from flask import request
    return request.headers.get('User-Agent', '')

def create_response(data: Any = None, message: str = None, status_code: int = 200) -> Dict[str, Any]:
    """Cria resposta padronizada"""
    response = {
        'success': status_code < 400,
        'status_code': status_code
    }
    
    if message:
        response['message'] = message
    
    if data is not None:
        response['data'] = data
    
    return response

def paginate_response(items: List[Any], page: int, per_page: int, total: int) -> Dict[str, Any]:
    """Cria resposta paginada"""
    pages = (total + per_page - 1) // per_page  # Ceiling division
    
    return {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages,
            'has_prev': page > 1,
            'has_next': page < pages,
            'prev_num': page - 1 if page > 1 else None,
            'next_num': page + 1 if page < pages else None
        }
    }

def mask_email(email: str) -> str:
    """Mascara email para logs"""
    if not email or '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    if len(local) <= 2:
        masked_local = local[0] + '*' * (len(local) - 1)
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    return f"{masked_local}@{domain}"

def mask_phone(phone: str) -> str:
    """Mascara telefone para logs"""
    if not phone:
        return phone
    
    # Manter apenas os últimos 4 dígitos
    if len(phone) <= 4:
        return '*' * len(phone)
    
    return '*' * (len(phone) - 4) + phone[-4:]
