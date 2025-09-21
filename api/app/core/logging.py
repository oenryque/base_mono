"""
Sistema de logging da aplicação
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import current_app

def setup_logging(app):
    """Configura o sistema de logging"""
    
    if not app.debug and not app.testing:
        # Criar diretório de logs se não existir
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configurar arquivo de log
        file_handler = RotatingFileHandler(
            app.config.get('LOG_FILE', 'logs/api.log'),
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('API iniciada')

def get_logger(name):
    """Obtém um logger específico"""
    return logging.getLogger(name)
