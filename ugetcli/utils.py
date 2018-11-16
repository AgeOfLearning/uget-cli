import contextlib
import os
import sys
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


def escape_exe_path(executable_path):
    """
    Escapes executable path to be runnable using subprocess.Popen with Shell=True
    :param path: Path to escape
    :return: Escaped path
    """
    if sys.platform == 'win32' and " " in executable_path:
        return '"' + executable_path + '"'
    else:
        return executable_path


def copy_replace_directory(src_dir, dst_dir):
    """
    Walks over the directory tree and copies one directory
    over to another, replacing existing files
    :param src_dir: Source directory path
    :param dst_dir: Destination directory path
    :return:
    """
    for src_dir, dirs, files in os.walk(src_dir):
        dst_dir = src_dir.replace(src_dir, dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def create_empty_file(path):
    with open(path, 'w'):
        pass
