"""
Script de gerenciamento da aplicação Flask
"""
import os
import click
from flask.cli import FlaskGroup
from app import create_app, db
from app.domain.models import User
from app.core.security import hash_password

# Criar aplicação Flask
app = create_app()
cli = FlaskGroup(create_app=lambda: app)

@cli.command()
def init_db():
    """Inicializa o banco de dados"""
    click.echo("Inicializando banco de dados...")
    db.create_all()
    click.echo("Banco de dados inicializado!")

@cli.command()
def drop_db():
    """Remove todas as tabelas do banco de dados"""
    if click.confirm("Tem certeza que deseja remover todas as tabelas?"):
        click.echo("Removendo tabelas...")
        db.drop_all()
        click.echo("Tabelas removidas!")

@cli.command()
def reset_db():
    """Remove e recria todas as tabelas"""
    if click.confirm("Tem certeza que deseja resetar o banco de dados?"):
        click.echo("Resetando banco de dados...")
        db.drop_all()
        db.create_all()
        click.echo("Banco de dados resetado!")

@cli.command()
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

@cli.command()
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

@cli.command()
def run():
    """Executa a aplicação em modo de desenvolvimento"""
    click.echo("Iniciando servidor de desenvolvimento...")
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

if __name__ == "__main__":
    cli()
