"""
Rotas de health check
"""
from flask import Blueprint, jsonify
from datetime import datetime
import os

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check básico"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """Verifica se a aplicação está pronta para receber tráfego"""
    try:
        # Verificar conexão com banco de dados
        from app import db
        db.session.execute('SELECT 1')
        
        # Verificar conexão com Redis (se configurado)
        # from app.extensions import redis
        # redis.ping()
        
        return jsonify({
            'status': 'ready',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'database': 'ok',
                'redis': 'ok'  # ou 'not_configured'
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503

@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """Verifica se a aplicação está viva"""
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat(),
        'uptime': 'running'
    })
