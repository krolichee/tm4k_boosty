__all__ = ['setModalRoot', 'getRoot']

_root = None


def setModalRoot(root):
    global _root
    _root = root


def getRoot():
    global _root
    return _root
