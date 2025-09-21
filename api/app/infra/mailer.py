"""
Sistema de email da aplicação
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from typing import List, Optional, Dict, Any
from app.core.logging import get_logger

logger = get_logger(__name__)

class Mailer:
    """Classe para envio de emails"""
    
    def __init__(self):
        self.smtp_server = current_app.config.get('MAIL_SERVER')
        self.smtp_port = current_app.config.get('MAIL_PORT', 587)
        self.use_tls = current_app.config.get('MAIL_USE_TLS', True)
        self.username = current_app.config.get('MAIL_USERNAME')
        self.password = current_app.config.get('MAIL_PASSWORD')
        self.from_email = current_app.config.get('MAIL_USERNAME')
    
    def send_email(self, to: str, subject: str, body: str, 
                   html_body: Optional[str] = None) -> bool:
        """Envia email simples"""
        try:
            if not self.smtp_server or not self.username or not self.password:
                logger.warning("Configurações de email não encontradas")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to
            msg['Subject'] = subject
            
            # Adicionar corpo do email
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)
            
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)
            
            # Conectar e enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email enviado para {to}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email para {to}: {str(e)}")
            return False
    
    def send_welcome_email(self, user_email: str, user_name: str, 
                          login_url: str) -> bool:
        """Envia email de boas-vindas"""
        subject = "Bem-vindo ao Sistema!"
        
        body = f"""
Olá {user_name},

Bem-vindo ao sistema! Sua conta foi criada com sucesso.

Você pode acessar o sistema em: {login_url}

Se você não solicitou esta conta, ignore este email.

Atenciosamente,
Equipe de Desenvolvimento
        """
        
        html_body = f"""
<html>
<body>
    <h2>Bem-vindo ao Sistema!</h2>
    <p>Olá {user_name},</p>
    <p>Bem-vindo ao sistema! Sua conta foi criada com sucesso.</p>
    <p>Você pode acessar o sistema em: <a href="{login_url}">{login_url}</a></p>
    <p>Se você não solicitou esta conta, ignore este email.</p>
    <br>
    <p>Atenciosamente,<br>Equipe de Desenvolvimento</p>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, body, html_body)
    
    def send_password_reset_email(self, user_email: str, user_name: str, 
                                 reset_url: str) -> bool:
        """Envia email de redefinição de senha"""
        subject = "Redefinição de Senha"
        
        body = f"""
Olá {user_name},

Você solicitou a redefinição de sua senha.

Clique no link abaixo para redefinir sua senha:
{reset_url}

Este link expira em 1 hora.

Se você não solicitou esta redefinição, ignore este email.

Atenciosamente,
Equipe de Desenvolvimento
        """
        
        html_body = f"""
<html>
<body>
    <h2>Redefinição de Senha</h2>
    <p>Olá {user_name},</p>
    <p>Você solicitou a redefinição de sua senha.</p>
    <p>Clique no link abaixo para redefinir sua senha:</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    <p>Este link expira em 1 hora.</p>
    <p>Se você não solicitou esta redefinição, ignore este email.</p>
    <br>
    <p>Atenciosamente,<br>Equipe de Desenvolvimento</p>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, body, html_body)
    
    def send_notification_email(self, user_email: str, user_name: str, 
                               title: str, message: str) -> bool:
        """Envia email de notificação"""
        subject = f"Notificação: {title}"
        
        body = f"""
Olá {user_name},

{message}

Atenciosamente,
Equipe de Desenvolvimento
        """
        
        html_body = f"""
<html>
<body>
    <h2>{title}</h2>
    <p>Olá {user_name},</p>
    <p>{message}</p>
    <br>
    <p>Atenciosamente,<br>Equipe de Desenvolvimento</p>
</body>
</html>
        """
        
        return self.send_email(user_email, subject, body, html_body)

# Instância global do mailer
mailer = Mailer()
