# Embedded file name: scripts/common/pydev/_pydev_bundle/fix_getpass.py


def fix_getpass():
    try:
        import getpass
    except ImportError:
        return

    import warnings
    fallback = getattr(getpass, 'fallback_getpass', None)
    if not fallback:
        fallback = getpass.default_getpass
    getpass.getpass = fallback
    if hasattr(getpass, 'GetPassWarning'):
        warnings.simplefilter('ignore', category=getpass.GetPassWarning)
    return