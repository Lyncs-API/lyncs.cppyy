"Utils for interfacing to numpy"

__all__ = [
    "get_ctype",
    "get_numpy_pointer",
    "array_to_pointers",
]

import numpy as np
from .ll import to_pointer
from .lib import lib

# NOTE: commented out cases that are not working
dtype_map = (
    (np.bool_, "bool"),
    # (np.byte, "signed char"),
    (np.ubyte, "unsigned char"),
    (np.short, "short"),
    (np.ushort, "unsigned short"),
    (np.intc, "int"),
    (np.uintc, "unsigned int"),
    (np.int_, "long"),
    (np.uint, "unsigned long"),
    (np.longlong, "long long"),
    (np.ulonglong, "unsigned long long"),
    # (np.half, ""),
    (np.single, "float"),
    (np.double, "double"),
    (np.longdouble, "long double"),
    (np.csingle, "std::complex<float>"),
    (np.cdouble, "std::complex<double>"),
    # (np.clongdouble, "std::complex<long double>"),
    # (np.int8, "int8_t"),
    (np.int16, "int16_t"),
    (np.int32, "int32_t"),
    (np.int64, "int64_t"),
    (np.uint8, "uint8_t"),
    (np.uint16, "uint16_t"),
    (np.uint32, "uint32_t"),
    (np.uint64, "uint64_t"),
    (np.intp, "intptr_t"),
    (np.uintp, "uintptr_t"),
    (np.float32, "float"),
    (np.float64, "double"),
    (np.complex64, "std::complex<float>"),
    (np.complex128, "std::complex<double>"),
)

char_map = {dtype(0).dtype.char: ctype for dtype, ctype in dtype_map}


def get_ctype(dtype):
    return char_map[np.dtype(dtype).char]


def get_numpy_pointer(arr):
    "Returns the pointer of a numpy array"
    ctype = get_ctype(arr.dtype)
    ptr = arr.__array_interface__["data"][0]
    return to_pointer(ptr, ctype + "*", arr.size)


def array_to_pointers(arr):
    """
    Returns a pointer to a list of pointers that can be used
    for accessing array elements as `ptr[i][j][k]` depending
    on the shape of the array
    """
    return lib.to_pointers(get_numpy_pointer(arr), *arr.shape)
