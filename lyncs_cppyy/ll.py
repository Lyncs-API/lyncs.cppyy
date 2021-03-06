"""
Additional low-level functions to the one provided by cppyy
"""
# pylint: disable=C0303

from itertools import product
from deprecated import deprecated
from cppyy.ll import __all__

# patch
if "set_signals_as_exceptionFatalErrorBusError" in __all__:
    __all__.remove("set_signals_as_exceptionFatalErrorBusError")

from cppyy.ll import *
from cppyy import cppdef, gbl, sizeof

from .numpy import char_map

__all__ = list(__all__) + [
    "array_to_pointers",
    "to_pointer",
    "assign",
]


class PointersArray:
    "Auxiliary class for managing arrays of pointers"

    def __init__(self, ptr, shape, dtype, delete=False):
        self.ptr = ptr
        self.shape = shape
        self.dtype = dtype
        self.view = cast[(self.dtype if len(shape) == 1 else "void") + "*"](ptr)
        self.view.reshape((self.shape[0],))
        self.delete = delete

    def __del__(self):
        if self.delete:
            array_delete(self.view)

    def __getitem__(self, key):
        if len(self.shape) == 1:
            return self.view[key]
        return PointersArray(self.view[key], self.shape[1:], self.dtype)

    def __setitem__(self, key, value):
        self.view[key] = value


def array_to_pointers(arr):
    """
    Returns a pointer to a list of pointer that can be used
    for accessing array elements as `ptr[i][j][k]` depending
    on the shape of the array
    """
    size = 0
    shape = arr.shape
    itemsize = arr.dtype.itemsize
    ctype = char_map[arr.dtype.char]
    ptr = arr.__array_interface__["data"][0]
    for i in range(len(shape) - 1):
        if i == 0:
            size = shape[0]
        else:
            size *= shape[i] + 1
    if size == 0:
        return PointersArray(ptr, shape, ctype)
    res = PointersArray(addressof(array_new["void**"](size)), shape, ctype, delete=True)
    skip = shape[0]
    ranges = []
    for i in range(len(shape) - 1):
        ranges.append(range(shape[i]))
        for idxs in product(*ranges):
            tmp = res
            inn = 0
            for j, idx in enumerate(idxs[:-1]):
                tmp = tmp[idx]
                inn = (inn + idx) * shape[j + 1]
            if i < len(shape) - 2:
                tmp[idxs[-1]] = res.ptr + (
                    skip + (inn + idxs[-1]) * shape[i + 1]
                ) * sizeof("void*")
            else:
                tmp[idxs[-1]] = ptr + ((inn + idxs[-1]) * shape[i + 1]) * itemsize
        skip *= shape[i + 1] + 1
    return res


def to_pointer(ptr: int, ctype: str = "void *", size: int = 1):
    "Casts integer to void pointer"
    ptr = cast[ctype](ptr)
    try:
        ptr.reshape((size,))
    except AttributeError:
        pass
    return ptr


@deprecated(
    version="0.1", reason="This function will be removed or changed in a future"
)
def assign(ptr, val):
    "Assigns value to pointer"
    try:
        return gbl._assign(ptr, val)
    except AttributeError:
        cppdef(
            """
            template<typename T1,typename T2>
            void _assign( T1* ptr, T2&& val ) {
              *ptr = val;
            }
            """
        )
        return assign(ptr, val)
