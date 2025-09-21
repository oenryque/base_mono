"""
Comandos CLI da aplicação
"""
import click
from flask import current_app
from app import db
from app.domain.models import User
from app.core.security import hash_password
from app.core.logging import get_logger

logger = get_logger(__name__)

def register_commands(app):
    """Registra comandos CLI"""
    
    @app.cli.command()
    def init_db():
        """Inicializa o banco de dados"""
        click.echo("Inicializando banco de dados...")
        db.create_all()
        click.echo("Banco de dados inicializado!")
    
    @app.cli.command()
    def drop_db():
        """Remove todas as tabelas do banco de dados"""
        if click.confirm("Tem certeza que deseja remover todas as tabelas?"):
            click.echo("Removendo tabelas...")
            db.drop_all()
            click.echo("Tabelas removidas!")
    
    @app.cli.command()
    def reset_db():
        """Remove e recria todas as tabelas"""
        if click.confirm("Tem certeza que deseja resetar o banco de dados?"):
            click.echo("Resetando banco de dados...")
            db.drop_all()
            db.create_all()
            click.echo("Banco de dados resetado!")
    
    @app.cli.command()
    def create_admin():
        """Cria um usuário administrador"""
        email = click.prompt("Email do administrador")
        password = click.prompt("Senha", hide_input=True)
        name = click.prompt("Nome do administrador")
        
        # Verificar se usuário já existe
        if User.query.filter_by(email=email).first():
            click.echo("Usuário já existe!")
            return
        
        # Criar usuário administrador
        admin = User(
            email=email,
            password_hash=hash_password(password),
            name=name,
            role="admin",
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        
        click.echo(f"Administrador {name} criado com sucesso!")
    
    @app.cli.command()
    def create_dev():
        """Cria um usuário desenvolvedor"""
        email = click.prompt("Email do desenvolvedor")
        password = click.prompt("Senha", hide_input=True)
        name = click.prompt("Nome do desenvolvedor")
        
        # Verificar se usuário já existe
        if User.query.filter_by(email=email).first():
            click.echo("Usuário já existe!")
            return
        
        # Criar usuário desenvolvedor
        dev = User(
            email=email,
            password_hash=hash_password(password),
            name=name,
            role="developer",
            is_active=True
        )
        
        db.session.add(dev)
        db.session.commit()
        
        click.echo(f"Desenvolvedor {name} criado com sucesso!")
    
    @app.cli.command()
    def list_users():
        """Lista todos os usuários"""
        users = User.query.all()
        
        if not users:
            click.echo("Nenhum usuário encontrado.")
            return
        
        click.echo(f"{'ID':<5} {'Nome':<20} {'Email':<30} {'Role':<12} {'Status':<10}")
        click.echo("-" * 80)
        
        for user in users:
            status = "Ativo" if user.is_active else "Inativo"
            click.echo(f"{user.id:<5} {user.name:<20} {user.email:<30} {user.role:<12} {status:<10}")
    
    @app.cli.command()
    def deactivate_user():
        """Desativa um usuário"""
        user_id = click.prompt("ID do usuário")
        
        try:
            user = User.query.get(int(user_id))
            if not user:
                click.echo("Usuário não encontrado!")
                return
            
            user.is_active = False
            user.status = "inactive"
            db.session.commit()
            
            click.echo(f"Usuário {user.name} desativado com sucesso!")
            
        except ValueError:
            click.echo("ID inválido!")
        except Exception as e:
            click.echo(f"Erro: {str(e)}")
    
    @app.cli.command()
    def activate_user():
        """Ativa um usuário"""
        user_id = click.prompt("ID do usuário")
        
        try:
            user = User.query.get(int(user_id))
            if not user:
                click.echo("Usuário não encontrado!")
                return
            
            user.is_active = True
            user.status = "active"
            db.session.commit()
            
            click.echo(f"Usuário {user.name} ativado com sucesso!")
            
        except ValueError:
            click.echo("ID inválido!")
        except Exception as e:
            click.echo(f"Erro: {str(e)}")
    
    @app.cli.command()
    def change_password():
        """Altera senha de um usuário"""
        user_id = click.prompt("ID do usuário")
        new_password = click.prompt("Nova senha", hide_input=True)
        
        try:
            user = User.query.get(int(user_id))
            if not user:
                click.echo("Usuário não encontrado!")
                return
            
            user.password_hash = hash_password(new_password)
            db.session.commit()
            
            click.echo(f"Senha alterada com sucesso para {user.name}!")
            
        except ValueError:
            click.echo("ID inválido!")
        except Exception as e:
            click.echo(f"Erro: {str(e)}")
    
    @app.cli.command()
    def run():
        """Executa a aplicação em modo de desenvolvimento"""
        click.echo("Iniciando servidor de desenvolvimento...")
        app.run(
            host="0.0.0.0",
            port=8000,
            debug=True
        )
