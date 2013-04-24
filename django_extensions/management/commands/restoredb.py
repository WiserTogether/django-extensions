__author__ = 'erik'

"""
 Command for restoring a database
"""

import os

from optparse import make_option

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backup database. Only Mysql and Postgresql engines are implemented"

    option_list = BaseCommand.option_list + (
        make_option('--sudo', action='store_true', dest='as_superuser',
                    help='Restore the database as a superuser'),
    )

    def handle(self, *args, **options):
        from ... import settings

        sql_filepath = os.path.join(settings.BACKUP_LOCATION, "%s.sql" % (settings.BACKUP_BASENAME))

        if not settings.BACKUP_RESTORE_ENABLED:
            print 'restore not enabled, set settings.EXTENSIONS_BACKUP_RESTORE_ENABLED=True to enable'
            return

        if settings.BACKUP_COMPRESSION:
            compressed_file_path = "%s.gz" % (sql_filepath)
            print "Decompressing %s to %s" % (compressed_file_path, sql_filepath)
            os.system('cat %s | gzip -d > "%s"' % (compressed_file_path, sql_filepath))

        if 'mysql' in settings.DB_ENGINE:
            print 'Doing Mysql restore of database %s from %s' % (settings.DB_NAME, sql_filepath)
            self.do_mysql_restore(sql_filepath)
        elif 'postgres' in settings.DB_ENGINE:
            print 'Doing Postgresql restore of database %s from %s' % (settings.DB_NAME, sql_filepath)
            if options['as_superuser']:
                self.do_sudo_postgresql_restore(sql_filepath)
            else:
                self.do_postgresql_restore(sql_filepath)
        else:
            print 'Backup in %s engine not implemented' % settings.DB_ENGINE

        if settings.BACKUP_COMPRESSION:
            os.unlink(sql_filepath)

    def do_mysql_restore(self, infile):
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

        os.system('mysql %s < %s' % (' '.join(args), infile))

    def do_postgresql_restore(self, infile):
        from ... import settings
        args = []
        if settings.DB_USER:
            args += ["--username=\"%s\"" % settings.DB_USER]
        if settings.DB_HOST:
            args += ["--host=%s" % settings.DB_HOST]
        if settings.DB_PORT:
            args += ["--port=%s" % settings.DB_PORT]
        if settings.DB_NAME:
            args += [settings.DB_NAME]

        cmd = 'PGPASSWORD=%s psql -c "drop schema public cascade; create schema public; alter schema public owner to \\\"%s\\\"" %s' % (
            settings.DB_PASSWD,
            settings.DB_USER,
            ' '.join(args))
        os.system(cmd)
        os.system('PGPASSWORD=%s psql %s < %s' % (settings.DB_PASSWD, ' '.join(args), infile))

    def do_sudo_postgresql_restore(self, infile):
        """
        This command doesn't work since creating the tables as postgres sets owner to postgres
        and DB user is then unable to make changes to the table
        """
        self.do_postgresql_restore(infile)

        from ... import settings

        for extension_name in ['hstore', 'uuid-ossp']:
            print 'Loading postgres extension %s for DB %s' % (extension_name, settings.DB_NAME)
            print 'Postgres version %s specified' % settings.DB_VERSION
            if settings.DB_VERSION == '9.0':
                extension_path = os.path.join(settings.BACKUP_LOCATION, 'extensions', '%s.sql' % extension_name)
                if os.path.exists(extension_path):
                    load_extension_cmd = 'sudo -u postgres psql %s < %s' % (settings.DB_NAME, extension_path)
                    os.system(load_extension_cmd)
                else:
                    print 'Could not find extension file at %s' % extension_path
            elif settings.DB_VERSION == '9.2':
                load_extension_cmd = 'sudo -u postgres psql %s -c "create extension \\\"%s\\\""' % (settings.DB_NAME, extension_name)
                os.system(load_extension_cmd)
