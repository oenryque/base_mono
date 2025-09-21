"""
Sistema de armazenamento da aplicação
"""
import os
import uuid
from typing import Optional, BinaryIO
from flask import current_app
from werkzeug.utils import secure_filename
from app.core.logging import get_logger

logger = get_logger(__name__)

class StorageManager:
    """Gerenciador de armazenamento de arquivos"""
    
    def __init__(self):
        self.upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        self.max_file_size = current_app.config.get('MAX_FILE_SIZE', 16 * 1024 * 1024)  # 16MB
        self.allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {
            'images': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
            'documents': {'pdf', 'doc', 'docx', 'txt'},
            'archives': {'zip', 'rar', '7z'}
        })
    
    def _get_file_extension(self, filename: str) -> str:
        """Obtém extensão do arquivo"""
        return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    def _is_allowed_file(self, filename: str, file_type: str = 'images') -> bool:
        """Verifica se arquivo é permitido"""
        if not filename:
            return False
        
        extension = self._get_file_extension(filename)
        allowed = self.allowed_extensions.get(file_type, set())
        return extension in allowed
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Gera nome único para arquivo"""
        extension = self._get_file_extension(original_filename)
        unique_id = str(uuid.uuid4())
        
        if extension:
            return f"{unique_id}.{extension}"
        return unique_id
    
    def save_file(self, file: BinaryIO, filename: str, 
                  file_type: str = 'images', subfolder: str = '') -> Optional[str]:
        """Salva arquivo no sistema"""
        try:
            # Verificar se arquivo é permitido
            if not self._is_allowed_file(filename, file_type):
                logger.warning(f"Tipo de arquivo não permitido: {filename}")
                return None
            
            # Verificar tamanho do arquivo
            file.seek(0, 2)  # Ir para o final
            file_size = file.tell()
            file.seek(0)  # Voltar para o início
            
            if file_size > self.max_file_size:
                logger.warning(f"Arquivo muito grande: {file_size} bytes")
                return None
            
            # Criar diretório se não existir
            upload_path = os.path.join(self.upload_folder, file_type)
            if subfolder:
                upload_path = os.path.join(upload_path, subfolder)
            
            os.makedirs(upload_path, exist_ok=True)
            
            # Gerar nome único e salvar
            unique_filename = self._generate_unique_filename(filename)
            file_path = os.path.join(upload_path, unique_filename)
            
            file.save(file_path)
            
            # Retornar caminho relativo
            relative_path = os.path.relpath(file_path, self.upload_folder)
            logger.info(f"Arquivo salvo: {relative_path}")
            return relative_path
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo {filename}: {str(e)}")
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """Remove arquivo do sistema"""
        try:
            full_path = os.path.join(self.upload_folder, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                logger.info(f"Arquivo removido: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao remover arquivo {file_path}: {str(e)}")
            return False
    
    def get_file_url(self, file_path: str) -> str:
        """Obtém URL do arquivo"""
        return f"/uploads/{file_path}"
    
    def file_exists(self, file_path: str) -> bool:
        """Verifica se arquivo existe"""
        full_path = os.path.join(self.upload_folder, file_path)
        return os.path.exists(full_path)
    
    def get_file_size(self, file_path: str) -> Optional[int]:
        """Obtém tamanho do arquivo"""
        try:
            full_path = os.path.join(self.upload_folder, file_path)
            if os.path.exists(full_path):
                return os.path.getsize(full_path)
            return None
        except Exception as e:
            logger.error(f"Erro ao obter tamanho do arquivo {file_path}: {str(e)}")
            return None
    
    def list_files(self, file_type: str = 'images', subfolder: str = '') -> list:
        """Lista arquivos em diretório"""
        try:
            directory = os.path.join(self.upload_folder, file_type)
            if subfolder:
                directory = os.path.join(directory, subfolder)
            
            if not os.path.exists(directory):
                return []
            
            files = []
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    relative_path = os.path.relpath(file_path, self.upload_folder)
                    files.append({
                        'filename': filename,
                        'path': relative_path,
                        'size': os.path.getsize(file_path),
                        'url': self.get_file_url(relative_path)
                    })
            
            return files
        except Exception as e:
            logger.error(f"Erro ao listar arquivos: {str(e)}")
            return []
    
    def cleanup_old_files(self, days: int = 30) -> int:
        """Remove arquivos antigos"""
        import time
        from datetime import datetime, timedelta
        
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            removed_count = 0
            
            for root, dirs, files in os.walk(self.upload_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.getmtime(file_path) < cutoff_time:
                        os.remove(file_path)
                        removed_count += 1
                        logger.info(f"Arquivo antigo removido: {file_path}")
            
            logger.info(f"Limpeza concluída: {removed_count} arquivos removidos")
            return removed_count
        except Exception as e:
            logger.error(f"Erro na limpeza de arquivos: {str(e)}")
            return 0

# Instância global do storage
storage = StorageManager()
