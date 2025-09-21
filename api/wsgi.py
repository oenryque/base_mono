"""
WSGI Entry Point para a API Flask
"""
import os
from app import create_app

# Criar aplicação Flask
application = create_app()

if __name__ == "__main__":
    # Para desenvolvimento local
    application.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        debug=os.environ.get("FLASK_ENV") == "development"
    )
