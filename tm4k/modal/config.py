__all__ = ['setRoot', 'getRoot']

_root = None


def setRoot(root):
    _root = root


def getRoot():
    return _root
