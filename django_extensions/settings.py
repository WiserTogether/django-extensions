__author__ = 'erik'
import os.path
from django.conf import settings

if hasattr(settings, 'DATABASES'):
    DB_ENGINE = settings.DATABASES['default']['ENGINE']
    DB_NAME = settings.DATABASES['default']['NAME']
    DB_USER = settings.DATABASES['default']['USER']
    DB_PASSWD = settings.DATABASES['default']['PASSWORD']
    DB_HOST = settings.DATABASES['default']['HOST']
    DB_PORT = settings.DATABASES['default']['PORT']
else:
    DB_ENGINE = settings.DATABASE_ENGINE
    DB_NAME = settings.DATABASE_NAME
    DB_USER = settings.DATABASE_USER
    DB_PASSWD = settings.DATABASE_PASSWORD
    DB_HOST = settings.DATABASE_HOST
    DB_PORT = settings.DATABASE_PORT

DB_VERSION = getattr(settings, 'DB_VERSION', '')

if hasattr(settings, 'PROJECT_NAME'):
    BACKUP_BASENAME = settings.PROJECT_NAME
else:
    BACKUP_BASENAME = DB_NAME

# only archive if requested specifically
if hasattr(settings, 'EXTENSIONS_BACKUP_ARCHIVE') and settings.EXTENSIONS_BACKUP_ARCHIVE:
    BACKUP_CREATE_ARCHIVE = True
else:
    BACKUP_CREATE_ARCHIVE = False

BACKUP_LOCATION = getattr(settings, 'EXTENSIONS_BACKUP_LOCATION', 'parts/database-backups')
BACKUP_ARCHIVE_LOCATION = getattr(settings, 'EXTENSIONS_BACKUP_ARCHIVE_LOCATION', 'archive')
BACKUP_GIT_COMMIT = getattr(settings, 'EXTENSOINS_BACKUP_COMMIT', False)
BACKUP_GIT_PUSH = getattr(settings, 'EXTENSIONS_BACKUP_PUSH', False)
BACKUP_GIT_REMOTE = getattr(settings, 'EXTENSIONS_BACKUP_GIT_REMOTE', 'origin')
BACKUP_GIT_BRANCH = getattr(settings, 'EXTENSIONS_BACKUP_GIT_BRANCH', 'master')
BACKUP_COMPRESSION = getattr(settings, 'EXTENSIONS_BACKUP_COMPRESSION', True)
BACKUP_RESTORE_ENABLED = getattr(settings, 'EXTENSIONS_BACKUP_RESTORE_ENABLED', False)
