"""
Additional low-level functions to the one provided by cppyy
"""
# pylint: disable=C0303

from cppyy.ll import __all__
from cppyy.ll import *
from .lib import lib

__all__ = list(__all__) + [
    "make_shared",
    "to_pointer",
]

make_shared = lib.make_shared


def to_pointer(ptr: int, ctype: str = "void *", size: int = None):
    "Casts integer to void pointer"
    ptr = cast[ctype](ptr)
    if size is not None:
        ptr.reshape((size,))
    return ptr
