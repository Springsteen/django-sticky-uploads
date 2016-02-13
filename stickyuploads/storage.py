import os
import tempfile

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class TempFileSystemStorage(FileSystemStorage):
    """Storage class to store files in the system /tmp."""

    def __init__(self):
        super(TempFileSystemStorage, self).__init__(
            location=tempfile.gettempdir(), base_url=None)

    def get_prefix(self):
        """Return prefix for easy recognition of project tmp folders"""
        if settings.FILE_UPLOAD_TEMP_DIR:
            return settings.FILE_UPLOAD_TEMP_DIR
        return ''

    def url(self, name):
        """Files are not accessable via url."""
        raise NotImplementedError()

    def get_available_name(self, name, max_length=None):
        """Return relative path to name placed in random directory"""
        tempdir = tempfile.mkdtemp(prefix=self.get_prefix(), dir=self.base_location)
        name = os.path.join(
            os.path.basename(tempdir),
            os.path.basename(name),
        )
        method = super(TempFileSystemStorage, self).get_available_name
        try:
            return method(name, max_length=max_length)
        except TypeError:
            # Django < 1.8
            return method(name)
