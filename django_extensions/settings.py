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

if hasattr(settings, 'PROJECT_NAME'):
    BACKUP_BASENAME = settings.PROJECT_NAME
else:
    BACKUP_BASENAME = DB_NAME

# only archive if requested specifically
if hasattr(settings, 'EXTENSIONS_BACKUP_ARCHIVE') and settings.EXTENSIONS_BACKUP_ARCHIVE:
    BACKUP_CREATE_ARCHIVE = True
else:
    BACKUP_CREATE_ARCHIVE = False

# push backups to git by default (if possible)
if hasattr(settings, 'EXTENSIONS_BACKUP_COMMIT_PUSH') and not settings.EXTENSIONS_BACKUP_COMMIT_PUSH:
    BACKUP_COMMIT_PUSH = False
else:
    BACKUP_COMMIT_PUSH = True

if hasattr(settings, 'EXTENSIONS_BACKUP_LOCATION'):
    BACKUP_LOCATION = settings.EXTENSIONS_BACKUP_LOCATION
else:
    BACKUP_LOCATION = 'parts/database-backups'


if hasattr(settings, 'EXTENSIONS_BACKUP_ARCHIVE_LOCATION'):
    BACKUP_ARCHIVE_LOCATION = settings.EXTENSIONS_BACKUP_ARCHIVE_LOCATION
else:
    BACKUP_ARCHIVE_LOCATION = os.path.join(BACKUP_LOCATION, 'archive')

if hasattr(settings, 'EXTENSIONS_GIT_REMOTE'):
    GIT_REMOTE = settings.EXTENSIONS_GIT_REMOTE
else:
    GIT_REMOTE = 'origin'

if hasattr(settings, 'EXTENSIONS_GIT_BRANCH'):
    GIT_BRANCH = settings.EXTENSIONS_GIT_BRANCH
else:
    GIT_BRANCH = 'master'

RESTORE_ENABLED = getattr(settings, 'EXTENSIONS_RESTORE_ENABLED', False)
