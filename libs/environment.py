import os


def getenv(var_name, default=None):
    """ Read `var_name` from the environment, returning a default
    if it is not set.

    If a default is not provided and `var_name` is not found, raises
    an AttributeError.

    Args:
        var_name (str) - environment variable name
        default (optional) - default value to return
    """
    if var_name in os.environ:
        return os.environ[var_name]
    else:
        if default:
            return default
    raise AttributeError('Environment Variable {} is required but not configured'.format(var_name))
