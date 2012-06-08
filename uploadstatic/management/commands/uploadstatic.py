from __future__ import with_statement

from optparse import make_option

from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.management.base import CommandError, NoArgsCommand
from django.utils.encoding import smart_str

from ...utils import get_files


class Command(NoArgsCommand):
    """
    Command that allows to copy or symlink static files from different
    locations to the settings.STATIC_ROOT.
    """
    option_list = NoArgsCommand.option_list + (
        make_option('--noinput',
            action='store_false', dest='interactive', default=True,
            help="Do NOT prompt the user for input of any kind."),
        make_option('--force',
            action='store_true', dest='force', default=False,
            help="Do NOT skip any files when uploading."),
        make_option('-i', '--ignore', action='append', default=[],
            dest='ignore_patterns', metavar='PATTERN',
            help="Ignore files or directories matching this glob-style "
                "pattern. Use multiple times to ignore more."),
        make_option('-n', '--dry-run',
            action='store_true', dest='dry_run', default=False,
            help="Do everything except modify the filesystem."),
        make_option('--no-default-ignore', action='store_false',
            dest='use_default_ignore_patterns', default=True,
            help="Don't ignore the common private glob-style patterns 'CVS', "
                "'.*' and '*~'."),
    )
    help = "Upload static files to S3."
    requires_model_validation = False

    def __init__(self, *args, **kwargs):
        super(NoArgsCommand, self).__init__(*args, **kwargs)
        self.uploaded_files = []
        self.skipped_files = []
        self.local_storage = get_storage_class('django.core.files.storage.FileSystemStorage')(
            location=getattr(settings, 'STATIC_ROOT', None),
            base_url=getattr(settings, 'STATIC_URL', None))
        self.remote_storage = get_storage_class('storages.backends.s3boto.S3BotoStorage')()

    def set_options(self, **options):
        """
        Set instance variables based on an options dict
        """
        self.interactive = options['interactive']
        self.verbosity = int(options.get('verbosity', 1))
        self.dry_run = options['dry_run']
        self.force = options['force']
        ignore_patterns = options['ignore_patterns']
        ignore_patterns.extend(getattr(settings, 'UPLOADSTATIC_IGNORE_PATTERNS', []))
        if options['use_default_ignore_patterns']:
            ignore_patterns += ['CVS', '.*', '*~']
        self.ignore_patterns = list(set(ignore_patterns))

    def upload_file(self, path):
        if self.dry_run:
            self.log(u"Pretending to upload '%s'" % path, level=1)
        else:
            if not self.force and self.remote_storage.exists(path):
                #local_modified = self.local_storage.modified_time(path)
                #remote_modified = self.remote_storage.modified_time(path)
                local_size = self.local_storage.size(path)
                remote_size = self.remote_storage.size(path)
                if remote_size == local_size:
                    self.log(u"Skipping '%s'" % path, level=2)
                    self.skipped_files.append(path)
                    return
            self.log(u"Uploading '%s'" % path, level=1)
            source_file = self.local_storage.open(path)
            try:
                self.remote_storage.save(path, source_file)
            finally:
                source_file.close()
        self.uploaded_files.append(path)

    def upload(self):
        """
        Perform the bulk of the work of uploadstatic.

        Split off from handle_noargs() to facilitate testing.
        """
        for f in get_files(self.local_storage, self.ignore_patterns):
            self.upload_file(f)

        return {
            'uploaded': self.uploaded_files,
            'skipped': self.skipped_files,
        }

    def handle_noargs(self, **options):
        self.set_options(**options)

        # Warn before doing anything more.
        if self.interactive:
            confirm = raw_input(u"""
You have requested to upload static files from
%s to your remote storage.

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: """ % (self.local_storage.location))
            if confirm != 'yes':
                raise CommandError("Collecting static files cancelled.")

        summary = self.upload()
        uploaded_count = len(summary['uploaded'])
        skipped_count = len(summary['skipped'])

        if self.verbosity >= 1:
            template = ("\n%(uploaded_count)s %(upload_identifier)s uploaded, "
                        "%(skipped_count)s %(skip_identifier)s skipped.\n")
            summary = template % {
                'uploaded_count': uploaded_count,
                'skipped_count': skipped_count,
                'upload_identifier': 'static file' + (uploaded_count != 1 and 's' or ''),
                'skip_identifier': 'static file' + (skipped_count != 1 and 's' or ''),
            }
            self.stdout.write(smart_str(summary))

    def log(self, msg, level=2):
        """
        Small log helper
        """
        msg = smart_str(msg)
        if not msg.endswith("\n"):
            msg += "\n"
        if self.verbosity >= level:
            self.stdout.write(msg)
