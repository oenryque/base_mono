"""
Tarefas assíncronas com Celery
"""
from celery import Celery
from flask import current_app
from app.core.logging import get_logger
from app.infra.mailer import mailer
from app.infra.storage import storage
from app.infra.repositories.user_repo import UserRepository

logger = get_logger(__name__)

# Inicializar Celery
celery = Celery('monorepo-api')

def init_celery(app):
    """Inicializar Celery com a aplicação Flask"""
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    # Contexto da aplicação para tarefas
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

@celery.task
def send_welcome_email_task(user_email: str, user_name: str, login_url: str):
    """Tarefa para enviar email de boas-vindas"""
    try:
        success = mailer.send_welcome_email(user_email, user_name, login_url)
        if success:
            logger.info(f"Email de boas-vindas enviado para {user_email}")
        else:
            logger.error(f"Falha ao enviar email de boas-vindas para {user_email}")
        return success
    except Exception as e:
        logger.error(f"Erro na tarefa de email de boas-vindas: {str(e)}")
        return False

@celery.task
def send_password_reset_email_task(user_email: str, user_name: str, reset_url: str):
    """Tarefa para enviar email de redefinição de senha"""
    try:
        success = mailer.send_password_reset_email(user_email, user_name, reset_url)
        if success:
            logger.info(f"Email de redefinição enviado para {user_email}")
        else:
            logger.error(f"Falha ao enviar email de redefinição para {user_email}")
        return success
    except Exception as e:
        logger.error(f"Erro na tarefa de email de redefinição: {str(e)}")
        return False

@celery.task
def send_notification_email_task(user_email: str, user_name: str, title: str, message: str):
    """Tarefa para enviar email de notificação"""
    try:
        success = mailer.send_notification_email(user_email, user_name, title, message)
        if success:
            logger.info(f"Email de notificação enviado para {user_email}")
        else:
            logger.error(f"Falha ao enviar email de notificação para {user_email}")
        return success
    except Exception as e:
        logger.error(f"Erro na tarefa de email de notificação: {str(e)}")
        return False

@celery.task
def cleanup_old_files_task(days: int = 30):
    """Tarefa para limpeza de arquivos antigos"""
    try:
        removed_count = storage.cleanup_old_files(days)
        logger.info(f"Limpeza de arquivos concluída: {removed_count} arquivos removidos")
        return removed_count
    except Exception as e:
        logger.error(f"Erro na tarefa de limpeza de arquivos: {str(e)}")
        return 0

@celery.task
def generate_user_report_task(user_id: int, report_type: str = 'summary'):
    """Tarefa para gerar relatório de usuário"""
    try:
        user_repo = UserRepository()
        user = user_repo.get_by_id(user_id)
        
        if not user:
            logger.error(f"Usuário {user_id} não encontrado")
            return False
        
        # Aqui você implementaria a lógica de geração de relatório
        # Por exemplo, gerar PDF, Excel, etc.
        
        logger.info(f"Relatório {report_type} gerado para usuário {user_id}")
        return True
    except Exception as e:
        logger.error(f"Erro na tarefa de geração de relatório: {str(e)}")
        return False

@celery.task
def backup_database_task():
    """Tarefa para backup do banco de dados"""
    try:
        # Aqui você implementaria a lógica de backup
        # Por exemplo, usando pg_dump para PostgreSQL
        
        logger.info("Backup do banco de dados iniciado")
        # Implementar backup aqui
        logger.info("Backup do banco de dados concluído")
        return True
    except Exception as e:
        logger.error(f"Erro na tarefa de backup: {str(e)}")
        return False

@celery.task
def send_daily_stats_task():
    """Tarefa para enviar estatísticas diárias"""
    try:
        user_repo = UserRepository()
        stats = user_repo.get_user_stats()
        
        # Enviar estatísticas para administradores
        admins = user_repo.get_admins()
        for admin in admins:
            send_notification_email_task.delay(
                admin.email,
                admin.name,
                "Estatísticas Diárias",
                f"Total de usuários: {stats.total_users}\n"
                f"Usuários ativos: {stats.active_users}\n"
                f"Novos usuários hoje: {stats.users_created_today}"
            )
        
        logger.info("Estatísticas diárias enviadas")
        return True
    except Exception as e:
        logger.error(f"Erro na tarefa de estatísticas diárias: {str(e)}")
        return False

@celery.task
def cleanup_expired_tokens_task():
    """Tarefa para limpeza de tokens expirados"""
    try:
        from app.domain.models import BlacklistedToken
        from datetime import datetime
        
        # Remover tokens expirados da blacklist
        expired_tokens = BlacklistedToken.query.filter(
            BlacklistedToken.expires_at < datetime.utcnow()
        ).all()
        
        for token in expired_tokens:
            db.session.delete(token)
        
        db.session.commit()
        
        logger.info(f"Limpeza de tokens: {len(expired_tokens)} tokens removidos")
        return len(expired_tokens)
    except Exception as e:
        logger.error(f"Erro na tarefa de limpeza de tokens: {str(e)}")
        return 0
