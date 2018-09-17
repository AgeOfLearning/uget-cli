import os

from click import BadParameter


def get_unitypackage_filename(project_name, version, configuration):
    """ Formats unitypackage filename """
    return "{0}_{1}_{2}.unitypackage".format(project_name, version, configuration)


def dir_find_file_with_extension(path, extension):
    """ Finds file with extension in the provided directory """
    for filename in os.listdir(path):
        if filename.endswith(extension):
            return os.path.join(path, filename)
    return None


def validate_url_param(ctx, param, value):
    if validate_url(value):
        return value
    raise BadParameter('invalid url format')


def validate_url(url):
    """ Validates if URI is valid """
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
