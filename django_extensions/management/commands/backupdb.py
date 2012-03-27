"""
 Command to backup database
"""

import os, time, shutil

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"

    def handle(self, *args, **options):
        from django.db import connection
        from ... import settings

        if not os.path.isdir(settings.BACKUP_LOCATION):
            os.makedirs(settings.BACKUP_LOCATION)

        backup_file = "%s.sql" %(settings.BACKUP_BASENAME)
        backup_file_path = os.path.join(settings.BACKUP_LOCATION, backup_file)

        if 'mysql' in settings.DB_ENGINE:
            print 'Doing Mysql backup to database %s into %s' % (settings.DB_NAME, backup_file_path)
            self.do_mysql_backup(backup_file_path)
        elif 'postgres' in settings.DB_ENGINE:
            print 'Doing Postgresql backup to database %s into %s' % (settings.DB_NAME, backup_file_path)
            self.do_postgresql_backup(backup_file_path)
        else:
            print 'Backup in %s engine not implemented' % settings.DB_ENGINE

        backup_file = "%s.sql" %(settings.BACKUP_BASENAME)
        if settings.BACKUP_COMPRESSION:
            compressed_file = "%s.sql.gz" %(settings.BACKUP_BASENAME)
            compressed_file_path = os.path.join(settings.BACKUP_LOCATION, compressed_file)
            print "Compressing %s to %s" %(backup_file_path, compressed_file_path)
            os.system('cat %s | gzip > "%s"' %(backup_file_path, compressed_file_path))
            os.unlink(backup_file_path)
            backup_file = compressed_file
            backup_file_path = compressed_file_path

        if settings.BACKUP_CREATE_ARCHIVE:
            archive_dir = os.path.join(settings.BACKUP_ARCHIVE_LOCATION,
                time.strftime('%Y-%m'), settings.BACKUP_BASENAME)
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)
            archive_file = os.path.join(archive_dir, '%s-%s.sql.gz' % (
                settings.BACKUP_BASENAME, time.strftime('%Y-%m-%dT%H')))
            shutil.copyfile(backup_file, archive_file)

        if settings.BACKUP_GIT_COMMIT and os.path.isdir(os.path.join(settings.BACKUP_LOCATION, '.git')):
            os.system('cd %s && git add %s' %(
                settings.BACKUP_LOCATION, backup_file))
            os.system('cd %s && git commit -m "database backup for %s"' %(
                settings.BACKUP_LOCATION, settings.BACKUP_BASENAME))

            if settings.BACKUP_GIT_PUSH:
                os.system('cd %s && git push %s %s' %(settings.BACKUP_LOCATION,
                                                      settings.BACKUP_GIT_REMOTE,
                                                      settings.BACKUP_GIT_BRANCH))

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
