import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except KeyError:
    __version__ = 'unknown'
