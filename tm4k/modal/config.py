__all__ = ['setModalRoot', 'getRoot']

_root = None


def setModalRoot(root):
    _root = root


def getRoot():
    return _root
