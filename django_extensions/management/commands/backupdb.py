"""
 Command for backup database
"""

import os, time
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"

    def handle(self, *args, **options):
        from django.db import connection
        from ... import settings

        if not os.path.isdir(settings.BACKUP_LOCATION):
            os.makedirs(settings.BACKUP_LOCATION)
        outfile = os.path.join(settings.BACKUP_LOCATION, "%s.sql" %(settings.BACKUP_BASENAME))

        if 'mysql' in settings.DB_ENGINE:
            print 'Doing Mysql backup to database %s into %s' % (settings.DB_NAME, outfile)
            self.do_mysql_backup(outfile)
        elif 'postgres' in settings.DB_ENGINE:
            print 'Doing Postgresql backup to database %s into %s' % (settings.DB_NAME, outfile)
            self.do_postgresql_backup(outfile)
        else:
            print 'Backup in %s engine not implemented' % settings.DB_ENGINE

        if settings.BACKUP_CREATE_ARCHIVE:
            archive_dir = os.path.join(settings.BACKUP_ARCHIVE_LOCATION, time.strftime('%Y-%m'), settings.BACKUP_BASENAME)
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            archive_file = os.path.join(archive_dir, '%s-%s.sql.gz' % (settings.BACKUP_BASENAME, time.strftime('%Y-%m-%dT%H')))
            print "Compressing %s to archive file %s" %(outfile, archive_file)
            os.system('cat %s | gzip > "%s"' (outfile, archive_file))

        if settings.BACKUP_COMMIT_PUSH and os.path.isdir(os.path.join(settings.BACKUP_LOCATION, '.git')):
            os.system('cd %s && git add %s' %(settings.BACKUP_LOCATION, "%s.sql" %(settings.BACKUP_BASENAME)))
            os.system('cd %s && git commit -m "database backup for %s"' %(settings.BACKUP_LOCATION, settings.BACKUP_BASENAME))
            os.system('cd %s && git push %s %s' %(settings.BACKUP_LOCATION, settings.GIT_REMOTE, settings.GIT_BRANCH))

    def do_mysql_backup(self, outfile):
        from ... import settings
        args = []
        if settings.DB_USER:
            args += ["--user=%s" % settings.DB_USER]
        if settings.DB_PASSWD:
            args += ["--password=%s" % settings.DB_PASSWD]
        if settings.DB_HOST:
            args += ["--host=%s" % settings.DB_HOST]
        if settings.DB_PORT:
            args += ["--port=%s" % settings.DB_PORT]
        args += [settings.DB_NAME]

        os.system('mysqldump %s > %s' % (' '.join(args), outfile))

    def do_postgresql_backup(self, outfile):
        from ... import settings
        args = []
        if settings.DB_USER:
            args += ["--username=%s" % settings.DB_USER]
        if settings.DB_HOST:
            args += ["--host=%s" % settings.DB_HOST]
        if settings.DB_PORT:
            args += ["--port=%s" % settings.DB_PORT]
        if settings.DB_NAME:
            args += [settings.DB_NAME]
        os.system('PGPASSWORD=%s pg_dump --no-password --clean --no-owner %s > %s' % (settings.DB_PASSWD, ' '.join(args), outfile))
