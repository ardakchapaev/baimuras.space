
"""Задачи для резервного копирования."""

import os
import subprocess
import gzip
import shutil
from datetime import datetime
from automation.celery_app import celery_app

@celery_app.task
def daily_database_backup():
    """Ежедневное резервное копирование базы данных."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.environ.get('BACKUP_DIR', '/tmp/backups')
        
        # Создание директории для бэкапов если не существует
        os.makedirs(backup_dir, exist_ok=True)
        
        # Параметры подключения к БД
        db_url = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/baimuras')
        
        if db_url.startswith('postgresql://'):
            # PostgreSQL backup
            backup_file = f"{backup_dir}/baimuras_backup_{timestamp}.sql"
            compressed_file = f"{backup_file}.gz"
            
            # Выполнение pg_dump
            cmd = [
                'pg_dump',
                db_url,
                '-f', backup_file,
                '--no-owner',
                '--no-privileges'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Сжатие файла
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Удаление несжатого файла
                os.remove(backup_file)
                
                # Удаление старых бэкапов (старше 7 дней)
                cleanup_old_backups(backup_dir, days=7)
                
                return {
                    'status': 'success',
                    'backup_file': compressed_file,
                    'size': os.path.getsize(compressed_file)
                }
            else:
                return {
                    'status': 'error',
                    'message': result.stderr
                }
        
        else:
            return {
                'status': 'error',
                'message': 'Unsupported database type'
            }
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def backup_uploaded_files():
    """Резервное копирование загруженных файлов."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        source_dir = os.environ.get('UPLOAD_DIR', '/app/uploads')
        backup_dir = os.environ.get('BACKUP_DIR', '/tmp/backups')
        
        if not os.path.exists(source_dir):
            return {'status': 'error', 'message': 'Upload directory not found'}
        
        # Создание архива
        archive_name = f"files_backup_{timestamp}"
        archive_path = f"{backup_dir}/{archive_name}"
        
        # Создание tar.gz архива
        shutil.make_archive(archive_path, 'gztar', source_dir)
        
        return {
            'status': 'success',
            'archive_file': f"{archive_path}.tar.gz",
            'size': os.path.getsize(f"{archive_path}.tar.gz")
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def cleanup_old_backups(backup_dir: str, days: int = 7):
    """Удаление старых файлов резервных копий."""
    try:
        cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)
        
        for filename in os.listdir(backup_dir):
            file_path = os.path.join(backup_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time < cutoff_time:
                    os.remove(file_path)
                    print(f"Removed old backup: {filename}")
                    
    except Exception as e:
        print(f"Error cleaning up old backups: {str(e)}")

@celery_app.task
def full_system_backup():
    """Полное резервное копирование системы."""
    try:
        # Резервное копирование БД
        db_backup = daily_database_backup()
        
        # Резервное копирование файлов
        files_backup = backup_uploaded_files()
        
        return {
            'status': 'success',
            'database_backup': db_backup,
            'files_backup': files_backup,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
