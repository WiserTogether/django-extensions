import os

from django.core.management.base import BaseCommand
from django.db import connection

from ... import settings, logger

class Command(BaseCommand):
    help = "Create database. Only Mysql and Postgresql engines are implemented"

    def handle(self, *args, **options):

        if 'postgres' in settings.DB_ENGINE:
            print 'Creating postgresql database %s' % (settings.DB_NAME)
            self.do_postgresql_createdb(settings.DB_NAME)
        else:
            print 'Backup in %s engine not implemented' % settings.DB_ENGINE

    def do_postgresql_createdb(self, database_name=None):
        args = []
        if settings.DB_USER:
            args += ["--username=%s" % settings.DB_USER]
        if settings.DB_HOST:
            args += ["--host=%s" % settings.DB_HOST]
        if settings.DB_PORT:
            args += ["--port=%s" % settings.DB_PORT]
        if database_name:
            args += [database_name]
        elif settings.DB_NAME:
            args += [settings.DB_NAME]

        cmd = 'PGPASSWORD=%s createdb --no-password %s' % (settings.DB_PASSWD, ' '.join(args))
        logger.info(cmd)
        os.system('PGPASSWORD=%s createdb --no-password %s' % (settings.DB_PASSWD, ' '.join(args)))

