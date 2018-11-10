import contextlib
import os
import tempfile
import shutil
import ntpath


def get_unitypackage_filename(project_name, version, configuration):
    """Generates .unitypackage file name using project name, version and configuration
    :param project_name: Project name
    :param version: Project version
    :param configuration: Build configuration (Debug/Release)
    :return: Name for .unitypackage file
    """
    return "{0}_{1}_{2}.unitypackage".format(project_name, version, configuration)


def dir_find_file_with_extension(path, extension):
    """Finds file with specified extension in the provided directory
    :param path: Path to the directory
    :param extension: File extension
    :return: Filename if file with extension exists in the directory, otherwise None
    """
    for filename in os.listdir(path):
        if filename.endswith(extension):
            return os.path.join(path, filename)
    return None


def dir_empty(path):
    """Checks if directory is empty
    :param path: Path to the directory
    :return: True if directory is empty, otherwise false
    """
    return len(os.listdir(path=path)) == 0


def get_filename(path):
    """Returns filename from any Windows and Unix compatible path
    This method runs on any platform (i.e. can parse Windows path when run on Unix platform)
    :param path: Windows path: /a/b/c or C:\a\b\c
    :return: Filename
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


@contextlib.contextmanager
def temp_dir():
    """A context manager that creates a temporary folder """
    t = tempfile.mkdtemp()
    try:
        yield t
    finally:
        try:
            shutil.rmtree(t)
        except (OSError, IOError):
            pass


def validate_url(url):
    """Checks if URL is valid
    :param url: URL
    :return: True if URL is valid, otherwise false
    """
    try:
        # python2
        from urlparse import urlparse
    except:
        # python3
        from urllib.parse import urlparse
    try:
        result = urlparse(url)
        return result.scheme
    except:
        return False
